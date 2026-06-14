from suurennuslasi_events.events.models import ImportCreated


async def import_zip(event: ImportCreated):
    print(event)
