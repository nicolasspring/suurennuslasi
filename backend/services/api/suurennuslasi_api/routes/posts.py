from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.post import Post
from suurennuslasi_db.session.db import get_session

router = APIRouter(tags=["posts"])


@router.get("/posts")
async def get_posts(
    session: AsyncSession = Depends(get_session),
) -> list[Post]:
    return await PostRepository.read_all(session)
