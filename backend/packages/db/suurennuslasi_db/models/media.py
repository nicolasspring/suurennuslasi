from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from suurennuslasi_domain.constants import IMPORT_JOB_STATUS


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


class MediaCreate(MediaBase):
    pass


class MediaUpdate(SQLModel):
    id: UUID
    filename: str | None = None
    mime_type: str | None = None
    size: int | None = None
    object_key: str | None = None
    original_uri: str | None = None
    title: str | None = None
    created_at: datetime | None = None
