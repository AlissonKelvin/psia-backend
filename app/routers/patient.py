from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.patient import Patient
from app.models.users import User
from app.schemas.patient import PatientBase, PatientList, PatientPublic
from app.security import get_password_hash

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
    rows = session.scalars(
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
