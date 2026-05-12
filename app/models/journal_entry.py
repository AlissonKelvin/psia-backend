from datetime import UTC, UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class JournalEntry:
    __tablename__ = 'journal_entries'
    patient_id: Mapped[UUID] = mapped_column(ForeignKey('patients.id'))
    content: Mapped[str] = mapped_column(Text)
    data_created: Mapped[datetime] = mapped_column(insert_default=datetime.now(UTC))
    data_updated: Mapped[datetime] = mapped_column(
        insert_default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
