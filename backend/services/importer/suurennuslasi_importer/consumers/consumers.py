from suurennuslasi_importer.handlers.import_zip import import_zip

from suurennuslasi_events.events.models import ImportCreated


async def consume_import_created(message):
    event = ImportCreated.model_validate_json(message.body)
    await import_zip(event)
