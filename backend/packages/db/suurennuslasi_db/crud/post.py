import typing as t
from uuid import UUID
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.exceptions import PostNotFoundException
from suurennuslasi_db.crud.media import MediaRepository
from suurennuslasi_db.models.media import MediaUpdate
from suurennuslasi_db.models.post import Post, PostCreate, PostUpdate


class PostRepository(BaseRepository):
    model = Post
    load_options = (selectinload(Post.media),)
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
        post = await super().create(
            session,
            item,
            exclude=["media", *(exclude or [])],
            additional=additional,
        )
        if item.media:
            for i, media in enumerate(item.media):
                await MediaRepository.update(
                    session,
                    MediaUpdate(id=media.id, position=i),
                    additional={"post_id": post.id},
                )
        return post

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> Post:
        return await super().read(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> list[Post]:
        return await super().read_all(session, **filters)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        item: PostUpdate,
        exclude: list[str] | None = None,
        additional: dict[str, t.Any] | None = None,
    ) -> Post:
        if item.media:
            for i, media in enumerate(item.media):
                await MediaRepository.update(
                    session,
                    MediaUpdate(id=media.id, position=i),
                    additional={"post_id": item.id},
                )
        return await super().update(
            session, item, exclude=["media", *(exclude or [])], additional=additional
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> Post:
        return await super().delete(session, id)

    @classmethod
    async def geoparsing_stats(cls, session: AsyncSession) -> tuple[int, int, int]:
        """
        Returns:
            (total_posts, geoparsed_posts, ungeoparsed_posts)
        """
        stmt = select(
            func.count().label("total"),
            func.sum(case((cls.model.geoparsed_at.is_not(None), 1), else_=0)).label(
                "geoparsed"
            ),
            func.sum(case((cls.model.geoparsed_at.is_(None), 1), else_=0)).label(
                "ungeoparsed"
            ),
        )

        total, geoparsed, ungeoparsed = (await session.execute(stmt)).one()

        return (
            total or 0,
            geoparsed or 0,
            ungeoparsed or 0,
        )
