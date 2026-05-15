from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JournalEntryBase(BaseModel):
    content: str
    source_type: str = 'text'


class JournalEntryPublic(BaseModel):
    id: UUID
    patient_id: UUID
    content: str
    source_type: str
    date_created: datetime
    date_updated: datetime


class JournalEntryList(BaseModel):
    journal_entries: list[JournalEntryPublic]
