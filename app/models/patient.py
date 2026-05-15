from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patients'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    psychologist_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

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
