from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import UUID as SA_UUID
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from suurennuslasi_db.models.media import Media, MediaCreate, MediaRead, MediaUpdate
    from suurennuslasi_db.models.source import Source


class PostBase(SQLModel):
    raw_json: str
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
    geoparsed_at: datetime | None = None
    source_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            SA_UUID,
            ForeignKey("source.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )


class Post(PostBase, table=True):
    __tablename__ = "post"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    media: list["Media"] = Relationship(
        back_populates="post",
        sa_relationship_kwargs={
            "order_by": "Media.position",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    source: "Source" = Relationship(back_populates="posts")


class PostCreate(PostBase):
    media: list["MediaCreate"] = Field(default_factory=list)


class PostUpdate(SQLModel):
    id: UUID
    raw_json: str | None = None
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
    geoparsed_at: datetime | None = None
    source_id: UUID | None = None
    media: list["MediaUpdate"] | None = None


class PostRead(SQLModel):
    id: UUID
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
    geoparsed_at: datetime | None = None
    source_id: UUID | None = None
    media: list["MediaRead"] = Field(default_factory=list)


# Rebuild the models to ensure relationships are properly initialized
from suurennuslasi_db.models.media import Media, MediaCreate, MediaRead, MediaUpdate
from suurennuslasi_db.models.source import Source

Post.model_rebuild()
PostCreate.model_rebuild()
PostUpdate.model_rebuild()
PostRead.model_rebuild()
