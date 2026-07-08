import typing as t
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import MediaNotFoundException
from suurennuslasi_db.models.media import Media, MediaCreate, MediaUpdate


class MediaRepository(BaseRepository):
    model = Media
    load_options = (selectinload(Media.post),)
    exception_factory: t.Callable[[str, UUID], Exception] = (
        lambda x, y: MediaNotFoundException(f"{x} with ID {y} not found.")
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        item: MediaCreate,
        exclude: t.Optional[list[str]] = None,
        additional: t.Optional[dict[str, t.Any]] = None,
    ) -> Media:
        return await super().create(session, item, exclude, additional)

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> Media:
        return await super().read(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> list[Media]:
        return await super().read_all(session, **filters)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        item: MediaUpdate,
        exclude: list[str] | None = None,
        additional: dict[str, t.Any] | None = None,
    ) -> Media:
        return await super().update(
            session,
            item,
            exclude=exclude,
            additional=additional,
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> Media:
        return await super().delete(session, id)
