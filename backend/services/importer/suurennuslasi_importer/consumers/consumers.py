from suurennuslasi_importer.handlers.parse_post import parse_post
from suurennuslasi_importer.handlers.import_zip import import_zip

from suurennuslasi_events.events.models import ImportCreated, PostExtracted


async def consume_import_created(message):
    event = ImportCreated.model_validate_json(message.body)
    await import_zip(event)


async def consume_post_extracted(message):
    event = PostExtracted.model_validate_json(message.body)
    await parse_post(event)
