from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JournalEntryAnalysisPublic(BaseModel):
    id: UUID
    journal_entry_id: UUID
    summary: str
    main_emotion: str
    trigger: str | None
    intensity: str | None
    cognitive_patterns: str | None
    behavior: str | None
    clinical_notes: str | None
    suggested_focus: str | None
    model_name: str
    prompt_version: str
    date_created: datetime
    date_updated: datetime


class JournalEntryWithAnalysis(BaseModel):
    id: UUID
    patient_id: UUID
    content: str
    source_type: str
    date_created: datetime
    date_updated: datetime
    analysis: JournalEntryAnalysisPublic | None = None


class JournalEntryWithAnalysisList(BaseModel):
    journal_entries: list[JournalEntryWithAnalysis]
