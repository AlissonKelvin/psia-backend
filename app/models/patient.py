from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patients'

    psychologist_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        insert_default=datetime.now(UTC)
    )
    date_updated: Mapped[datetime] = mapped_column(
        insert_default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    id: Mapped[UUID] = mapped_column(init=False, primary_key=True, insert_default=uuid4)
