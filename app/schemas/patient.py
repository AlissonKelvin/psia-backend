from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PatientBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class PatientPublic(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    email: EmailStr
    psychologist_id: UUID
    date_created: datetime
    date_updated: datetime


class PatientList(BaseModel):
    patients: list[PatientPublic]
