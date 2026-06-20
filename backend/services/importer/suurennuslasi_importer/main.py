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
        "import.created",
        consume_import_created,
    )


if __name__ == "__main__":
    asyncio.run(main())
