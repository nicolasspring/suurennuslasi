from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class JobBase(SQLModel):
    status: str
    progress: float
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None


class ImportJobBase(JobBase):
    total_posts: int | None = None
    processed_posts: int | None = None


class ImportJob(ImportJobBase, table=True):
    __tablename__ = "importjob"

    id: UUID = Field(primary_key=True)


class ImportJobCreate(ImportJobBase):
    pass


class ImportJobUpdate(SQLModel):
    id: UUID
    status: str | None = None
    progress: float | None = None
    created_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None
    total_posts: int | None = None
    processed_posts: int | None = None
