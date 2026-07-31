import logging
from datetime import datetime
from functools import lru_cache

from geoparser import Geoparser
from geoparser.modules import SpacyRecognizer

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJobUpdate
from suurennuslasi_db.models.post import PostUpdate
from suurennuslasi_db.session.db import AsyncSessionLocal
from suurennuslasi_domain.constants import IMPORT_JOB_STATUS
from suurennuslasi_events.events.models import PostParsed

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_geoparser() -> Geoparser:
    return Geoparser(recognizer=SpacyRecognizer(model_name="en_core_web_trf"))


async def geoparse_post(event: PostParsed):
    geoparser = get_geoparser()
    post_id = None
    caption = ""
    async with AsyncSessionLocal() as session:
        await ImportJobRepository.update(
            session,
            ImportJobUpdate(id=event.job_id, status=IMPORT_JOB_STATUS.GEOPARSING),
        )
        logger.info(f"Geoparsing post {event.post_id} for job {event.job_id}")
        post = await PostRepository.read(session, event.post_id)
        post_id = post.id
        caption = post.caption or ""

    document = geoparser.parse(caption)[0]
    update_data = {
        "id": post_id,
        "geoparsed_at": datetime.now(),
    }
    if document.toponyms:
        # for now, the first toponym found serves as the post location
        first_toponym = document.toponyms[0]
        if post_location := first_toponym.location:
            update_data["location"] = post_location.data.get("name")
            update_data["latitude"] = post_location.data.get("latitude")
            update_data["longitude"] = post_location.data.get("longitude")
            logger.info(
                f"Updated post {event.post_id} with location {update_data['location']}"
            )
        else:
            logger.info(
                f"Toponym {first_toponym.text} for post {event.post_id} has no location"
            )
    else:
        logger.info(f"No toponyms detected for post {event.post_id}")

    async with AsyncSessionLocal() as session:
        await PostRepository.update(session, PostUpdate(**update_data))
        await ImportJobRepository.update_progress(session, event.job_id)
        logger.info(
            f"Geoparsing completed for post {event.post_id} for job {event.job_id}"
        )
