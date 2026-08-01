from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from suurennuslasi_domain.constants import SOURCE_TYPE

if TYPE_CHECKING:
    from suurennuslasi_db.models.post import Post, PostRead


class SourceBase(SQLModel):
    name: str | None = None
    type: SOURCE_TYPE = Field(default=SOURCE_TYPE.ZIP)
    mime_type: str | None = None
    size: int | None = None
    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    n_posts: int | None = None


class Source(SourceBase, table=True):
    __tablename__ = "source"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    posts: list["Post"] = Relationship(
        back_populates="source",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )


class SourceCreate(SourceBase):
    pass


class SourceUpdate(SQLModel):
    id: UUID
    name: str | None = None
    type: SOURCE_TYPE | None = None
    mime_type: str | None = None
    size: int | None = Field(default=None, ge=0)
    created_at: datetime | None = None
    n_posts: int | None = Field(default=None, ge=0)


class SourceRead(SQLModel):
    id: UUID
    name: str | None = None
    type: SOURCE_TYPE | None = None
    mime_type: str | None = None
    size: int | None = None
    created_at: datetime | None = None
    n_posts: int | None = None
    posts: list["PostRead"] = Field(default_factory=list)


from suurennuslasi_db.models.post import Post, PostRead

Source.model_rebuild()
SourceCreate.model_rebuild()
SourceUpdate.model_rebuild()
SourceRead.model_rebuild()
