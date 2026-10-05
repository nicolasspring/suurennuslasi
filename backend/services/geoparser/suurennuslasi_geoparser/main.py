import asyncio
import logging
import os

from suurennuslasi_geoparser.consumers import consume_post_parsed
from suurennuslasi_geoparser.handlers.geoparse import get_geoparser

from suurennuslasi_messaging.subscriber import subscribe

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"),
)

logger = logging.getLogger(__name__)

handlers = {"import.post_parsed": consume_post_parsed}


def validate_geoparser_setup() -> None:
    geoparser = get_geoparser()
    try:
        result = geoparser.parse("Zurich")
        document = result[0] if isinstance(result, list) else result
        if not document.toponyms:
            logger.warning("Geoparser startup check found no toponyms for sanity input")
    except RuntimeError as exc:
        message = str(exc)
        if "created by an older version" in message:
            logger.critical(
                "Incompatible geoparser database. Stop the service, remove "
                "/root/.local/share/geoparser/geoparser.db, then restart the service. "
                "The installed gazetteer is stored separately and does not need reinstalling."
            )
        raise


async def dispatch(message):
    async with message.process(requeue=True):
        handler = handlers.get(message.routing_key)
        if handler is None:
            logger.warning(
                "No handler for %s",
                message.routing_key,
            )
            return
        try:
            await handler(message)
        except Exception:
            logger.exception(
                "Failed to process message with routing key %s", message.routing_key
            )
            raise


async def main() -> None:
    validate_geoparser_setup()
    await subscribe(
        exchange_name="imports",
        queue_name="geoparser",
        handlers=handlers,
        dispatch=dispatch,
        prefetch_count=int(os.getenv("RABBITMQ_PREFETCH_COUNT", "5")),
    )


if __name__ == "__main__":
    asyncio.run(main())
