import asyncio
import logging

from suurennuslasi_messaging.subscriber import subscribe

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"),
)

logger = logging.getLogger(__name__)

handlers = {}


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
        queue_name="geoparser",
        handlers=handlers,
        dispatch=dispatch,
    )


if __name__ == "__main__":
    asyncio.run(main())
