import typing as t
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import ImportJobNotFoundException
from suurennuslasi_db.models.job import ImportJob, ImportJobCreate, ImportJobUpdate


class ImportJobRepository(BaseRepository):
    model = ImportJob
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
    async def update(cls, session: AsyncSession, item: ImportJobUpdate) -> ImportJob:
        if not item.last_edited:
            item.last_edited = datetime.now()
        return await super().update(session, item)

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> ImportJob:
        return await super().delete(session, id)
