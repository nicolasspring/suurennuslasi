from suurennuslasi_geoparser.handlers.geoparse import geoparse_post

from suurennuslasi_events.events.models import PostParsed


async def consume_post_parsed(message):
    event = PostParsed.model_validate_json(message.body)
    await geoparse_post(event)
