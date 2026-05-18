from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class JournalEntryAnalysis:
    __tablename__ = 'journal_entry_analysis'

    journal_entry_id: Mapped[UUID] = mapped_column(
        ForeignKey('journal_entries.id')
    )
    summary: Mapped[str] = mapped_column(Text)
    main_emotion: Mapped[str]
    trigger: Mapped[str | None] = mapped_column(nullable=True)
    intensity: Mapped[str | None] = mapped_column(nullable=True)
    cognitive_patterns: Mapped[str | None] = mapped_column(nullable=True)
    behavior: Mapped[str | None] = mapped_column(nullable=True)
    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_focus: Mapped[str | None] = mapped_column(Text, nullable=True)

    model_name: Mapped[str]
    prompt_version: Mapped[str]

    date_created: Mapped[datetime] = mapped_column(
        init=False,
        insert_default=lambda: datetime.now(UTC),
    )
    date_updated: Mapped[datetime] = mapped_column(
        init=False,
        insert_default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    id: Mapped[UUID] = mapped_column(
        init=False,
        primary_key=True,
        insert_default=uuid4,
    )
