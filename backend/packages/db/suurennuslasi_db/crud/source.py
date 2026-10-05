import typing as t
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import SourceNotFoundException
from suurennuslasi_db.models.source import Source, SourceCreate, SourceUpdate


class SourceRepository(BaseRepository):
    model = Source
    load_options = ()
    exception_factory: t.Callable[[str, UUID], Exception] = (
        lambda x, y: SourceNotFoundException(f"{x} with ID {y} not found.")
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        item: SourceCreate,
        exclude: t.Optional[list[str]] = None,
        additional: t.Optional[dict[str, t.Any]] = None,
    ) -> Source:
        return await super().create(session, item, exclude, additional)

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> Source:
        return await super().read(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> list[Source]:
        return await super().read_all(session, **filters)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        item: SourceUpdate,
        exclude: list[str] | None = None,
        additional: dict[str, t.Any] | None = None,
    ) -> Source:
        return await super().update(
            session,
            item,
            exclude=exclude,
            additional=additional,
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> Source:
        return await super().delete(session, id)
