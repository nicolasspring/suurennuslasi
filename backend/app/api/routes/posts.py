from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.crud.post import PostRepository
from app.core.db import get_session
from app.models.post import Post

router = APIRouter(tags=["posts"])


@router.get("/posts")
async def get_posts(
    session: AsyncSession = Depends(get_session),
) -> list[Post]:
    return await PostRepository.read_all(session)
