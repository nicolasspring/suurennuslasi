import json
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJobUpdate
from suurennuslasi_db.models.post import PostUpdate
from suurennuslasi_db.session.db import AsyncSessionLocal
from suurennuslasi_domain.constants.constants import IMPORT_JOB_STATUS
from suurennuslasi_events.events.models import PostExtracted

logger = logging.getLogger(__name__)


async def parse_post(event: PostExtracted):
    async with AsyncSessionLocal() as session:
        await ImportJobRepository.update(
            session,
            ImportJobUpdate(id=event.job_id, status=IMPORT_JOB_STATUS.PARSING),
        )
        logger.info(f"Parsing post {event.post_id} for job {event.job_id}")
        post = await PostRepository.read(session, event.post_id)
        post_json = json.loads(post.raw_json)
        await PostRepository.update(
            session,
            PostUpdate(
                id=event.post_id,
                caption=post_json["title"],
                created_at=datetime.fromtimestamp(post_json["creation_timestamp"]),
            ),
        )
        logger.info(f"Post {event.post_id} for job {event.job_id} ready for geoparsing")
