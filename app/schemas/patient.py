from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PatientBase(BaseModel):
    name: str
    email: EmailStr | None = None
    pychologist_id: UUID


class PatientPublic(BaseModel):
    id: UUID
    name: str
    email: EmailStr | None = None
    pychologist_id: UUID
    date_created: datetime
    date_updated: datetime


class PatientList(BaseModel):
    patients: list[PatientPublic]
