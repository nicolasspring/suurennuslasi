import json
import logging
import mimetypes
import os
import tempfile
from zipfile import Path, ZipFile

import ijson
from sqlalchemy.ext.asyncio import AsyncSession

from suurennuslasi_db.crud.media import MediaRepository
from suurennuslasi_db.crud.post import PostRepository
from suurennuslasi_db.models.media import MediaCreate
from suurennuslasi_db.models.post import PostCreate
from suurennuslasi_db.session.db import get_session
from suurennuslasi_events.events.models import ImportCreated
from suurennuslasi_storage.crud.storage import AsyncObjectStorage

logger = logging.getLogger(__name__)


async def import_zip(event: ImportCreated):
    session = await get_session()
    logger.info(
        f"Importing zip file for job {event.job_id} with object key {event.object_key}"
    )
    with tempfile.NamedTemporaryFile() as tmp:
        await AsyncObjectStorage.download_to_path(event.object_key, tmp.name)

        with ZipFile(tmp.name) as archive:
            media_saved = await save_media(session, archive)
            posts_saved = await save_posts(session, archive)
    logger.info(
        f"Extracted {media_saved} media items and {posts_saved} posts for job {event.job_id}"
    )
    await AsyncObjectStorage.delete(event.object_key)
    logger.info(f"Deleted zip file with object key {event.object_key} from storage")


async def save_media(session: AsyncSession, file: ZipFile) -> int:
    root = Path(file)
    media = root / "media" / "posts"
    for i, image in enumerate(media.rglob("*")):
        if image.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
            with image.open("rb") as f:
                object_key = f"images/{image.name}"
                await AsyncObjectStorage.upload(object_key, f)
                f.seek(0, os.SEEK_END)
                await MediaRepository.create(
                    session,
                    MediaCreate(
                        filename=image.name,
                        mime_type=mimetypes.guess_type(image.name)[0],
                        object_key=object_key,
                        size=f.tell(),
                    ),
                )
            logger.info(f"Imported media {image.name} with object key {object_key}")
    return i + 1


async def save_posts(session: AsyncSession, file: ZipFile) -> int:
    root = Path(file)
    media = root / "your_instagram_activity" / "media"
    saved = 0
    for json_file in media.rglob("posts_*.json"):
        logger.info("Importing %s", json_file)
        with json_file.open("rb") as f:
            for post in ijson.items(f, "item"):
                raw_json = json.dumps(
                    post,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                await PostRepository.create(
                    session,
                    PostCreate(
                        raw_json=raw_json,
                    ),
                )
                # publish import created event
                saved += 1
    return saved
