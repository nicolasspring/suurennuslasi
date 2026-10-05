import logging
import re
from datetime import datetime
from functools import lru_cache

from geoparser import Geoparser
from geoparser.modules import SentenceTransformerResolver, SpacyRecognizer

from suurennuslasi_geoparser.geoparser_database import configure_geoparser_database

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJobUpdate
from suurennuslasi_db.models.post import PostUpdate
from suurennuslasi_db.session.db import AsyncSessionLocal
from suurennuslasi_domain.constants import (
    IMPORT_JOB_STATUS,
    POST_HEADER_LOCATION_SPLIT_PATTERN,
)
from suurennuslasi_events.events.models import PostParsed

logger = logging.getLogger(__name__)


def _first_document(parse_result):
    if isinstance(parse_result, list):
        return parse_result[0] if parse_result else None
    return parse_result


@lru_cache(maxsize=1)
def get_geoparser() -> Geoparser:
    configure_geoparser_database()
    return Geoparser(
        recognizer=SpacyRecognizer(model_name="en_core_web_trf"),
        # Lower similarity threshold to improve recall
        resolver=SentenceTransformerResolver(
            gazetteer_name="geonames",
            min_similarity=0.45,
        ),
    )


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
    document = _first_document(
        geoparser.parse(caption.replace("\n", " ").replace("\r", " "))
    )
    if document is None:
        logger.warning(
            "Geoparser returned no document for post %s (job %s)",
            event.post_id,
            event.job_id,
        )
        document_toponyms = []
    else:
        document_toponyms = document.toponyms
    update_data = {
        "id": post_id,
        "geoparsed_at": datetime.now(),
    }
    if document_toponyms:
        # for now, the first toponym found serves as the post location
        first_toponym = document_toponyms[0]
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
