import logging
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

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ingestion"])


@router.post("/ingest/file")
async def ingest_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    logger.info(f"File {file.filename} received")
    job = await ImportJobRepository.create(session, ImportJobCreate())
    logger.info(f"Import job with ID {job.id} created")
    object_key = f"uploads/{job.id}/instagram.zip"
    await AsyncObjectStorage.upload(object_key, file)
    logger.info(f"File with key {object_key} uploaded to object storage")
    with tempfile.NamedTemporaryFile() as tmp:
        await AsyncObjectStorage.download_to_path(object_key, tmp.name)
    await AsyncObjectStorage.delete(object_key)
    logger.info(f"File with key {object_key} deleted from object storage")
    payload = {"job_id": str(job.id), "object_key": object_key}
    await publish(
        exchange_name="imports",
        routing_key="import.created",
        payload=payload,
    )
    logger.info(f"published import.created for job ID {job.id} published")
    await ImportJobRepository.update(
        session, ImportJobUpdate(id=job.id, status=IMPORT_JOB_STATUS.QUEUED)
    )
    logger.info(
        f"Import job with ID {job.id} updated to status {IMPORT_JOB_STATUS.QUEUED}"
    )
    return job


@router.get("/ingest/job/{job_id}/status")
async def get_ingestion_job_status(
    job_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> ImportJob:
    return await ImportJobRepository.read(session, job_id)
