from datetime import datetime, UTC
from uuid import uuid4, UUID

from app.models.registry import table_registry

from sqlalchemy.orm import Mapped, mapped_column


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    name: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    date_created: Mapped[datetime] = mapped_column(
        init=False, insert_default=datetime.now(UTC)
    )
    date_updated: Mapped[datetime] = mapped_column(
        init=False,
        insert_default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    id: Mapped[UUID] = mapped_column(init=False, primary_key=True, insert_default=uuid4)

    @property
    def id_string(self):  # pragma: no cover
        return str(self.id)

    @property
    def date_created_string(self):  # pragma: no cover
        return self.date_created.isoformat()

    @property
    def date_updated_string(self):  # pragma: no cover
        return self.date_updated.isoformat()
