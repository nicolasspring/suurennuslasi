import typing as t
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import PostNotFoundException
from suurennuslasi_db.models.post import Post, PostCreate, PostUpdate


class PostRepository(BaseRepository):
    model = Post
    exception_factory: t.Callable[[str, UUID], Exception] = (
        lambda x, y: PostNotFoundException(f"{x} with ID {y} not found.")
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        item: PostCreate,
        exclude: t.Optional[list[str]] = None,
        additional: t.Optional[dict[str, t.Any]] = None,
    ) -> Post:
        return await super().create(session, item, exclude, additional)

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> Post:
        return await super().read(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> list[Post]:
        return await super().read_all(session, **filters)

    @classmethod
    async def update(cls, session: AsyncSession, item: PostUpdate) -> Post:
        return await super().update(session, item)

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> Post:
        return await super().delete(session, id)
