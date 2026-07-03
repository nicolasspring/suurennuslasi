import asyncio
import logging
import mimetypes

from suurennuslasi_importer.consumers import (
    consume_import_created,
    consume_post_extracted,
)

from suurennuslasi_domain.mime_types import register_mime_types
from suurennuslasi_messaging.subscriber import subscribe

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"),
)

logger = logging.getLogger(__name__)

register_mime_types()

handlers = {
    "import.created": consume_import_created,
    "post.extracted": consume_post_extracted,
}


async def dispatch(message):
    async with message.process():
        handler = handlers.get(message.routing_key)
        if handler is None:
            logger.warning(
                "No handler for %s",
                message.routing_key,
            )
            return
        await handler(message)


async def main() -> None:
    await subscribe(
        exchange_name="imports",
        queue_name="importer",
        handlers=handlers,
        dispatch=dispatch,
    )


if __name__ == "__main__":
    asyncio.run(main())
