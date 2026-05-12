from datetime import datetime, UTC
from uuid import uuid4, UUID

from app.models.registry import table_registry

from sqlalchemy.orm import Mapped, mapped_column, registry

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    name: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    data_created: Mapped[datetime] = mapped_column(insert_default=datetime.now(UTC))
    data_updated: Mapped[datetime] = mapped_column(
        insert_default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    @property
    def is_string(self):  # pragma: no cover
        return str(self.id)

    @property
    def date_created_string(self):  # pragma: no cover
        return self.data_created.isoformat()

    @property
    def date_updated_string(self):  # pragma: no cover
        return self.data_updated.isoformat()
