import logging
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.source import SourceRepository
from suurennuslasi_db.models.job import ImportJobCreate, ImportJobRead, ImportJobUpdate
from suurennuslasi_db.models.source import SourceCreate
from suurennuslasi_db.session.db import get_session
from suurennuslasi_domain.constants import IMPORT_JOB_STATUS, SOURCE_TYPE
from suurennuslasi_messaging.publisher import publish
from suurennuslasi_storage.crud.storage import AsyncObjectStorage

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ingestion"])


@router.post("/ingest/file")
async def ingest_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
) -> ImportJobRead:
    logger.info(f"File {file.filename} received")
    job = await ImportJobRepository.create(session, ImportJobCreate())
    logger.info(f"Import job with ID {job.id} created")
    source = await SourceRepository.create(
        session,
        SourceCreate(
            name=file.filename,
            type=SOURCE_TYPE.ZIP,
            mime_type=file.content_type,
            size=getattr(file, "size", None),
        ),
    )
    logger.info(f"Source with ID {source.id} created for upload {file.filename}")
    object_key = f"uploads/{job.id}/instagram.zip"
    await AsyncObjectStorage.upload(object_key, file)
    logger.info(f"File with key {object_key} uploaded to object storage")
    payload = {
        "job_id": str(job.id),
        "object_key": object_key,
        "source_id": str(source.id),
    }
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
) -> ImportJobRead:
    return await ImportJobRepository.read(session, job_id)
