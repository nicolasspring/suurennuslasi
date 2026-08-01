from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.source import SourceRepository
from suurennuslasi_db.models.source import SourceRead
from suurennuslasi_db.session.db import get_session

router = APIRouter(tags=["sources"])


@router.get("/sources")
async def get_sources(
    session: AsyncSession = Depends(get_session),
) -> list[SourceRead]:
    return await SourceRepository.read_all(session)


@router.get("/source/{source_id}")
async def get_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    return await SourceRepository.read(session, source_id)


@router.delete("/source/{source_id}")
async def delete_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    return await SourceRepository.delete(session, source_id)
