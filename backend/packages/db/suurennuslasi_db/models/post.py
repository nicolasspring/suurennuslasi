from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    instagram_id: str
    caption: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime


class Post(PostBase, table=True):
    __tablename__ = "post"

    id: UUID = Field(primary_key=True)


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    id: UUID
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
