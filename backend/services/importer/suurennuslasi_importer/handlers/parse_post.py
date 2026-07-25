import json
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.job import ImportJobRepository
from suurennuslasi_db.crud.media import MediaRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.job import ImportJobUpdate
from suurennuslasi_db.models.media import MediaUpdate
from suurennuslasi_db.models.post import PostUpdate
from suurennuslasi_db.session.db import AsyncSessionLocal
from suurennuslasi_domain.constants.constants import IMPORT_JOB_STATUS
from suurennuslasi_events.events.models import PostExtracted
from suurennuslasi_messaging.publisher import publish

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
        # sometimes there are ghost posts in the zip file that have no title
        # or creation_timestamp. these are just deleted
        if not post_json.get("title") or not post_json.get("creation_timestamp"):
            logger.warning(
                f"Post {event.post_id} for job {event.job_id} is missing title or creation_timestamp. Deleting..."
            )
            await PostRepository.delete(session, event.post_id)
            return
        post_media = []
        for media in post_json.get("media", []):
            media_db = (
                await MediaRepository.read_all(
                    session, filename=media["uri"].split("/")[-1]
                )
            )[0]
            # update media with new data from post
            await MediaRepository.update(
                session,
                MediaUpdate(
                    id=media_db.id,
                    original_uri=media.get("uri"),
                    created_at=(
                        datetime.fromtimestamp(media.get("creation_timestamp"))
                        if media.get("creation_timestamp")
                        else None
                    ),
                    title=media.get("title"),
                ),
            )
            logger.info(
                f"Media {media['uri']} ({media['uri'].split('/')[-1]}) updated for post {event.post_id} for job {event.job_id}"
            )
            # prepare for linking media to post
            post_media.append(MediaUpdate(id=media_db.id))
        # update post and link media
        await PostRepository.update(
            session,
            PostUpdate(
                id=event.post_id,
                caption=post_json.get("title"),
                created_at=(
                    datetime.fromtimestamp(post_json.get("creation_timestamp"))
                    if post_json.get("creation_timestamp")
                    else None
                ),
                media=post_media,
            ),
        )
        payload = {"job_id": str(event.job_id), "post_id": str(post.id)}
        await publish(
            exchange_name="imports",
            routing_key="import.post_parsed",
            payload=payload,
        )
        logger.info(
            f"Post {event.post_id} for job {event.job_id} updated and ready for geoparsing"
        )
