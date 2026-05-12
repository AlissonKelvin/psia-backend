from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserPublic(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    date_created: datetime
    date_updated: datetime


class UserList(BaseModel):
    users: list[UserPublic]
