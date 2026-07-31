import logging
from functools import lru_cache

from geoparser import Geoparser
from geoparser.modules import SpacyRecognizer

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJobUpdate
from suurennuslasi_db.session.db import AsyncSessionLocal
from suurennuslasi_domain.constants import IMPORT_JOB_STATUS
from suurennuslasi_events.events.models import PostParsed

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_geoparser() -> Geoparser:
    return Geoparser(recognizer=SpacyRecognizer(model_name="en_core_web_trf"))


async def geoparse_post(event: PostParsed):
    geoparser = get_geoparser()
    async with AsyncSessionLocal() as session:
        await ImportJobRepository.update(
            session,
            ImportJobUpdate(id=event.job_id, status=IMPORT_JOB_STATUS.PARSING),
        )
        logger.info(f"Geoparsing post {event.post_id} for job {event.job_id}")
        post = await PostRepository.read(session, event.post_id)
        document = geoparser.parse(post.caption)[0]
        for toponym in document.toponyms:
            logger.info(
                f"Found toponym {toponym.text} in post {event.post_id} for job {event.job_id}"
            )
