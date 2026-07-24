from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from suurennuslasi_domain.constants import IMPORT_JOB_STATUS


class JobBase(SQLModel):
    status: IMPORT_JOB_STATUS = Field(default=IMPORT_JOB_STATUS.CREATED)
    progress: float | None = None
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    last_edited: datetime = Field(default_factory=datetime.now, nullable=False)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None


class ImportJobBase(JobBase):
    total_posts: int | None = None
    processed_posts: int | None = None


class ImportJob(ImportJobBase, table=True):
    __tablename__ = "importjob"

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ImportJobCreate(ImportJobBase):
    pass


class ImportJobUpdate(SQLModel):
    id: UUID
    status: str | None = None
    progress: float | None = None
    created_at: datetime | None = None
    last_edited: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None
    total_posts: int | None = None
    processed_posts: int | None = None


class ImportJobRead(SQLModel):
    id: UUID
    status: IMPORT_JOB_STATUS
    progress: float | None = None
    created_at: datetime
    last_edited: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None
