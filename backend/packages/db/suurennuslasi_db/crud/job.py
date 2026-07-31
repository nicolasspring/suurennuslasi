import typing as t
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import ImportJobNotFoundException
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJob, ImportJobCreate, ImportJobUpdate
from suurennuslasi_domain.constants.constants import IMPORT_JOB_STATUS


class ImportJobRepository(BaseRepository):
    model = ImportJob
    load_options = ()
    exception_factory: t.Callable[[str, UUID], Exception] = (
        lambda x, y: ImportJobNotFoundException(f"{x} with ID {y} not found.")
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        item: ImportJobCreate,
        exclude: t.Optional[list[str]] = None,
        additional: t.Optional[dict[str, t.Any]] = None,
    ) -> ImportJob:
        return await super().create(session, item, exclude, additional)

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> ImportJob:
        return await super().read(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> list[ImportJob]:
        return await super().read_all(session, **filters)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        item: ImportJobUpdate,
        exclude: list[str] | None = None,
        additional: dict[str, t.Any] | None = None,
    ) -> ImportJob:
        if not item.last_edited:
            item.last_edited = datetime.now()
        return await super().update(
            session, item, exclude=exclude, additional=additional
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> ImportJob:
        return await super().delete(session, id)

    @classmethod
    async def update_progress(cls, session: AsyncSession, job_id: UUID) -> ImportJob:
        total, geoparsed, _ = await PostRepository.geoparsing_stats(session)
        additional = {}
        if total == geoparsed:
            additional["status"] = IMPORT_JOB_STATUS.COMPLETED
            additional["finished_at"] = datetime.now()
        return await cls.update(
            session,
            ImportJobUpdate(
                id=job_id,
                total_posts=total,
                processed_posts=geoparsed,
            ),
            additional=additional,
        )
