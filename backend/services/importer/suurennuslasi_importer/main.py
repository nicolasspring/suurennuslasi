import asyncio

from suurennuslasi_importer.consumers import consume_import_created

from suurennuslasi_messaging.subscriber import subscribe


async def main() -> None:
    await subscribe(
        "import.created",
        consume_import_created,
    )


if __name__ == "__main__":
    asyncio.run(main())
