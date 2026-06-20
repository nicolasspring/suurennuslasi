import logging

from suurennuslasi_events.events.models import ImportCreated

logger = logging.getLogger(__name__)


async def import_zip(event: ImportCreated):
    logger.info(
        f"Importing zip file for job {event.job_id} with object key {event.object_key}"
    )
