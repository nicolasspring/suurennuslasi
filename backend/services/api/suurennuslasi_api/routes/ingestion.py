import tempfile
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.models.job import ImportJob, ImportJobCreate, ImportJobUpdate
from suurennuslasi_db.session.db import get_session
from suurennuslasi_domain.constants import IMPORT_JOB_STATUS
from suurennuslasi_messaging.publisher import publish
from suurennuslasi_storage.crud.storage import AsyncObjectStorage

router = APIRouter(tags=["ingestion"])


@router.post("/ingest/file")
async def ingest_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    job = await ImportJobRepository.create(session, ImportJobCreate())
    object_key = f"uploads/{job.id}/instagram.zip"
    await AsyncObjectStorage.upload(object_key, file)
    with tempfile.NamedTemporaryFile() as tmp:
        await AsyncObjectStorage.download_to_path(object_key, tmp.name)
    await AsyncObjectStorage.delete(object_key)
    await publish("import.created", {"job_id": job.id, "object_key": object_key})
    await ImportJobRepository.update(
        session, ImportJobUpdate(id=job.id, status=IMPORT_JOB_STATUS.QUEUED)
    )
    return job


@router.get("/ingest/job/{job_id}/status")
async def get_ingestion_job_status(
    job_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    return await ImportJobRepository.read(session, job_id)
