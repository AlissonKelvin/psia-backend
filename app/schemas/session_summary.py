from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionSummaryEntry(BaseModel):
    journal_entry_id: UUID
    content: str
    source_type: str
    date_created: datetime
    summary: str | None
    main_emotion: str | None
    trigger: str | None
    intensity: str | None
    cognitive_patterns: str | None
    behavior: str | None
    suggested_focus: str | None


class SessionSummaryPublic(BaseModel):
    patient_id: UUID
    total_entries: int
    main_emotions: list[str]
    triggers: list[str]
    cognitive_patterns: list[str]
    suggested_focus: list[str]
    entries: list[SessionSummaryEntry]


class SessionAISummary(BaseModel):
    patient_id: UUID
    summary: str
