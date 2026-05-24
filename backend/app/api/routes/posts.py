import typing as t

from app.core.db import get_session
from app.models.post import Post
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(tags=["posts"])


@router.get("/posts")
async def get_posts(
    session: AsyncSession = Depends(get_session),
) -> t.List[Post]:
    result = await session.execute(select(Post))

    posts = result.scalars().all()

    return posts
