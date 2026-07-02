from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    raw_json: str
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None


class Post(PostBase, table=True):
    __tablename__ = "post"

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    id: UUID
    raw_json: str | None = None
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
