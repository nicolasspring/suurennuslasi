import asyncio
import logging
import mimetypes

from suurennuslasi_importer.consumers import consume_import_created

from suurennuslasi_domain.mime_types import register_mime_types
from suurennuslasi_messaging.subscriber import subscribe

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"),
)

register_mime_types()

handlers = {
    "import.created": consume_import_created,
}


async def main() -> None:
    await subscribe(
        exchange_name="imports",
        queue_name="importer",
        handlers=handlers,
    )


if __name__ == "__main__":
    asyncio.run(main())
