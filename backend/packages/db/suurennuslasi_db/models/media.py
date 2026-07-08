from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import UUID as SA_UUID
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from suurennuslasi_db.models.post import Post


class MediaBase(SQLModel):
    filename: str
    mime_type: str
    size: int
    object_key: str
    original_uri: str | None = None
    title: str | None = None
    created_at: datetime | None = None


class Media(MediaBase, table=True):
    __tablename__ = "media"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID | None = Field(
        sa_column=Column(
            SA_UUID, ForeignKey("post.id", ondelete="CASCADE"), nullable=True
        )
    )
    post: "Post" = Relationship(back_populates="media")
    position: int | None = Field(index=True)


class MediaCreate(MediaBase):
    position: int | None = None


class MediaUpdate(SQLModel):
    id: UUID
    filename: str | None = None
    mime_type: str | None = None
    size: int | None = None
    object_key: str | None = None
    original_uri: str | None = None
    title: str | None = None
    created_at: datetime | None = None
    position: int | None = None


# Rebuild the models to ensure relationships are properly initialized
from suurennuslasi_db.models.post import Post

Media.model_rebuild()
MediaCreate.model_rebuild()
MediaUpdate.model_rebuild()
