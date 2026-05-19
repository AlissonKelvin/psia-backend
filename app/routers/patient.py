from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.patient import Patient
from app.models.users import User
from app.schemas.patient import PatientBase, PatientList, PatientPublic
from app.security import get_password_hash
from app.models.journal_entry import JournalEntry
from app.models.journal_entry_analysis import JournalEntryAnalysis
from app.schemas.session_summary import SessionSummaryPublic

router = APIRouter(prefix='/patients', tags=['patients'])


@router.post('/', response_model=PatientPublic, status_code=HTTPStatus.CREATED)
def create_patient(
    patient: PatientBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    existing_user = session.scalar(
        select(User).where(User.email == patient.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User with this email already exists',
        )

    if current_user.role != 'psychologist':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only psychologists can create patients.',
        )

    patient_user = User(
        name=patient.name,
        email=patient.email,
        password_hash=get_password_hash(patient.password),
        role='patient',
    )

    session.add(patient_user)
    session.flush()

    db_patient = Patient(
        user_id=patient_user.id,
        psychologist_id=current_user.id,
    )

    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return {
        'id': db_patient.id,
        'user_id': patient_user.id,
        'name': patient_user.name,
        'email': patient_user.email,
        'psychologist_id': db_patient.psychologist_id,
        'date_created': db_patient.date_created,
        'date_updated': db_patient.date_updated,
    }


@router.get('/', response_model=PatientList)
def list_patients(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    rows = session.execute(
        select(Patient, User)
        .join(User, Patient.user_id == User.id)
        .where(Patient.psychologist_id == current_user.id)
    ).all()

    patients = [
        {
            'id': patient.id,
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'psychologist_id': patient.psychologist_id,
            'date_created': patient.date_created,
            'date_updated': patient.date_updated,
        }
        for patient, user in rows
    ]

    return {'patients': patients}


@router.get(
    '/{patient_id}/session-summary', response_model=SessionSummaryPublic
)
def get_patient_session_summary(
    patient_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    patient = session.scalar(
        select(Patient).where(
            Patient.id == patient_id,
            Patient.psychologist_id == current_user.id,
        )
    )
    if current_user.role != 'psychologist':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only psychologists can access patient session summaries.',
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

    entries = []
    main_emotions = set()
    triggers = set()
    cognitive_patterns = set()
    suggested_focus = set()

    for journal_entry, analysis in rows:
        if analysis:
            if analysis.main_emotion:
                main_emotions.add(analysis.main_emotion)
            if analysis.trigger:
                triggers.add(analysis.trigger)
            if analysis.cognitive_patterns:
                cognitive_patterns.add(analysis.cognitive_patterns)
            if analysis.suggested_focus:
                suggested_focus.add(analysis.suggested_focus)
        entries.append({
            'journal_entry_id': journal_entry.id,
            'content': journal_entry.content,
            'source_type': journal_entry.source_type,
            'date_created': journal_entry.date_created,
            'summary': analysis.summary if analysis else None,
            'main_emotion': analysis.main_emotion if analysis else None,
            'trigger': analysis.trigger if analysis else None,
            'intensity': analysis.intensity if analysis else None,
            'cognitive_patterns': analysis.cognitive_patterns
            if analysis
            else None,
            'behavior': analysis.behavior if analysis else None,
            'suggested_focus': analysis.suggested_focus if analysis else None,
        })

    return {
        'patient_id': patient.id,
        'total_entries': len(entries),
        'main_emotions': sorted(main_emotions),
        'triggers': sorted(triggers),
        'cognitive_patterns': sorted(cognitive_patterns),
        'suggested_focus': sorted(suggested_focus),
        'entries': entries,
    }
