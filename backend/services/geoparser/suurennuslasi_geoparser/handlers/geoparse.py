import logging
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
    async with AsyncSessionLocal() as session:
        await ImportJobRepository.update(
            session,
            ImportJobUpdate(id=event.job_id, status=IMPORT_JOB_STATUS.PARSING),
        )
        logger.info(f"Geoparsing post {event.post_id} for job {event.job_id}")
        post = await PostRepository.read(session, event.post_id)
        document = geoparser.parse(post.caption)[0]
        if document.toponyms:
            # for now, the first toponym found serves as the post location
            first_toponym = document.toponyms[0]
            if post_location := first_toponym.location:
                location = post_location.data.get("name")
                latitude = post_location.data.get("latitude")
                longitude = post_location.data.get("longitude")
                await PostRepository.update(
                    session,
                    PostUpdate(
                        id=post.id,
                        location=location,
                        latitude=latitude,
                        longitude=longitude,
                    ),
                )
                logger.info(f"Updated post {event.post_id} with location {location}")
            else:
                logger.info(
                    f"Toponym {first_toponym.text} for post {event.post_id} has no location"
                )
        else:
            logger.info(f"No toponyms detected for post {event.post_id}")
