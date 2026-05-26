from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.base import BaseRepository
from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.models.job import ImportJob
from suurennuslasi_db.session.db import get_session

router = APIRouter(tags=["ingestion"])


@router.post("/ingest/file")
async def ingest_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    pass


@router.get("/ingest/job/{job_id}/status")
async def get_ingestion_job_status(
    job_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    return await ImportJobRepository.read(session, job_id)
