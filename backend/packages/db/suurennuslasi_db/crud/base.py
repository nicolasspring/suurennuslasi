import typing as t
from abc import ABC
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

T = t.TypeVar("T", bound=SQLModel)


class BaseRepository(ABC):
    model: t.Type[T]
    exception_factory: t.Callable[[str, UUID], Exception] = lambda x, y: ValueError(
        f"{x} with ID {y} not found."
    )

    @classmethod
    def get_mapped_class(
        cls,
        item: T,
        exclude: t.Optional[list[str]] = NotImplemented,
        additional: t.Optional[dict[str, t.Any]] = NotImplemented,
    ) -> T:
        item_data = item.model_dump(exclude=exclude or [], exclude_unset=True)
        return cls.model(**item_data, **additional or {})

    @classmethod
    async def _get_or_raise(cls, session: AsyncSession, id: UUID) -> T:
        db_item = await session.get(cls.model, id)
        if not db_item:
            raise cls.exception_factory(cls.model.__name__, id)
        return db_item

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        item: T,
        exclude: t.Optional[list[str]] = None,
        additional: t.Optional[dict[str, t.Any]] = None,
    ) -> T:
        item = cls.get_mapped_class(item, exclude or [], additional or {})
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @classmethod
    async def read(cls, session: AsyncSession, id: UUID) -> T:
        return await cls._get_or_raise(session, id)

    @classmethod
    async def read_all(cls, session: AsyncSession, **filters) -> t.List[T]:
        filter_args = []
        for key, value in filters.items():
            if not hasattr(cls.model, key):
                raise ValueError(f"Invalid filter field: {key}")
            filter_args.append(getattr(cls.model, key) == value)
        stmt = select(cls.model)
        stmt = stmt.where(*filter_args)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, item: T) -> t.Optional[T]:
        db_item = await cls._get_or_raise(session, item.id)
        item_data = item.model_dump(exclude_unset=True)
        for key, value in item_data.items():
            setattr(db_item, key, value)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    @classmethod
    async def delete(cls, session: AsyncSession, id: UUID) -> T:
        db_item = await cls._get_or_raise(session, id)
        await session.delete(db_item)
        await session.commit()
        return db_item
