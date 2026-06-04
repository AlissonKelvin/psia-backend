import os
import tempfile
from http import HTTPStatus
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.journal_entry import JournalEntry
from app.models.journal_entry_analysis import JournalEntryAnalysis
from app.models.patient import Patient
from app.models.users import User
from app.schemas.journal_entry import (
    JournalEntryBase,
    JournalEntryList,
    JournalEntryPublic,
)
from app.schemas.journal_entry_analysis import (
    JournalEntryWithAnalysisList,
)
from app.models.journal_entry_analysis import JournalEntryAnalysis
from app.services.journal_analysis import PROMPT_VERSION, analyze_journal_entry
from app.settings import settings

from app.services.transcription import transcribe_audio

router = APIRouter(prefix='/journal-entries', tags=['journal entries'])


@router.post(
    '/', response_model=JournalEntryPublic, status_code=HTTPStatus.CREATED
)
def create_journal_entry(
    journal_entry: JournalEntryBase,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if current_user.role != 'patient':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only patients can create journal entries.',
        )
    patient = session.scalar(
        select(Patient).where(Patient.user_id == current_user.id)
    )

    if not patient:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Patient not found.'
        )

    db_journal_entry = JournalEntry(
        patient_id=patient.id,
        content=journal_entry.content,
        source_type=journal_entry.source_type,
    )

    session.add(db_journal_entry)
    session.commit()
    session.refresh(db_journal_entry)

    analysis_data = analyze_journal_entry(journal_entry.content)

    db_analysis = JournalEntryAnalysis(
        journal_entry_id=db_journal_entry.id,
        summary=analysis_data['summary'] or 'Resumo não disponível',
        main_emotion=analysis_data['main_emotion'] or 'Emoção não disponível',
        trigger=analysis_data.get('trigger'),
        intensity=analysis_data.get('intensity'),
        cognitive_patterns=analysis_data.get('cognitive_patterns'),
        behavior=analysis_data.get('behavior'),
        clinical_notes=analysis_data.get('clinical_notes'),
        suggested_focus=analysis_data.get('suggested_focus'),
        model_name=settings.GROQ_LLM_MODEL,
        prompt_version=PROMPT_VERSION,
    )

    session.add(db_analysis)
    session.commit()

    return db_journal_entry


@router.post(
    '/audio', response_model=JournalEntryPublic, status_code=HTTPStatus.CREATED
)
async def create_audio_journal_entry(
    audio: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.role != 'patient':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only patients can create journal entries.',
        )

    patient = session.scalar(
        select(Patient).where(Patient.user_id == current_user.id)
    )
    if not patient:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Patient not found.'
        )

    suffix = os.path.splitext(audio.filename or '')[1]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix
    ) as temp_audio:
        content = await audio.read()
        temp_audio.write(content)

        temp_file_path = temp_audio.name

    try:
        transcription = transcribe_audio(temp_file_path)

        db_journal_entry = JournalEntry(
            patient_id=patient.id,
            content=transcription,
            source_type='audio',
        )

        session.add(db_journal_entry)
        session.commit()
        session.refresh(db_journal_entry)

        analysis_data = analyze_journal_entry(db_journal_entry.content)

        db_analysis = JournalEntryAnalysis(
            journal_entry_id=db_journal_entry.id,
            summary=analysis_data['summary'] or 'Resumo não disponível',
            main_emotion=analysis_data['main_emotion'],
            trigger=analysis_data.get('trigger'),
            intensity=analysis_data.get('intensity'),
            cognitive_patterns=analysis_data.get('cognitive_patterns'),
            behavior=analysis_data.get('behavior'),
            clinical_notes=analysis_data.get('clinical_notes'),
            suggested_focus=analysis_data.get('suggested_focus'),
            model_name=settings.GROQ_LLM_MODEL,
            prompt_version=PROMPT_VERSION,
        )

        session.add(db_analysis)
        session.commit()

        return db_journal_entry
    finally:
        os.remove(temp_file_path)


@router.get('/', response_model=JournalEntryList)
def list_journal_entries(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if current_user.role == 'patient':
        patient = session.scalar(
            select(Patient).where(Patient.user_id == current_user.id)
        )
        if not patient:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Patient profile not found.',
            )
        journal_entries = session.scalars(
            select(JournalEntry).where(JournalEntry.patient_id == patient.id)
        ).all()

        return {'journal_entries': journal_entries}

    elif current_user.role == 'psychologist':
        journal_entries = session.scalars(
            select(JournalEntry)
            .join(Patient)
            .where(Patient.psychologist_id == current_user.id)
        ).all()
        return {'journal_entries': journal_entries}

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN, detail='Invalid user role.'
    )


@router.get(
    '/patient/{patient_id}', response_model=JournalEntryWithAnalysisList
)
def list_patient_journal_entries_with_analysis(
    patient_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if current_user.role != 'psychologist':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only psychologists can access patient journal entries.',
        )

    patient = session.scalar(
        select(Patient).where(
            Patient.id == patient_id,
            Patient.psychologist_id == current_user.id,
        )
    )
    if not patient:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Patient not found or not assigned to this psychologist.',
        )

    rows = session.execute(
        select(JournalEntry, JournalEntryAnalysis)
        .outerjoin(
            JournalEntryAnalysis,
            JournalEntryAnalysis.journal_entry_id == JournalEntry.id,
        )
        .where(JournalEntry.patient_id == patient.id)
        .order_by(JournalEntry.date_created.desc())
    ).all()

    journal_entries = [
        {
            'id': entry.id,
            'patient_id': entry.patient_id,
            'content': entry.content,
            'source_type': entry.source_type,
            'date_created': entry.date_created,
            'date_updated': entry.date_updated,
            'analysis': analysis,
        }
        for entry, analysis in rows
    ]

    return {'journal_entries': journal_entries}
