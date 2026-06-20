import asyncio
import logging
import os

import aio_pika

logger = logging.getLogger(__name__)


async def get_connection():
    while True:
        try:
            logger.info("Connecting to RabbitMQ...")
            conn = await aio_pika.connect_robust(
                f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@rabbitmq/"
            )
            logger.info("Connected to RabbitMQ")
            return conn
        except Exception as exc:
            logger.error(f"RabbitMQ not ready: {exc}")
            await asyncio.sleep(5)
