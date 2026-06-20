import asyncio
import logging

from suurennuslasi_importer.consumers import consume_import_created

from suurennuslasi_messaging.subscriber import subscribe

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"),
)


async def main() -> None:
    await subscribe(
        exchange_name="imports",
        queue_name="importer.imports",
        routing_key="import.created",
        callback=consume_import_created,
    )


if __name__ == "__main__":
    asyncio.run(main())
