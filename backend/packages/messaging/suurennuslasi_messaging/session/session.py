import asyncio
import os

import aio_pika


async def get_connection():
    while True:
        try:
            return await aio_pika.connect_robust(
                f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@rabbitmq/"
            )
        except Exception as exc:
            print(f"RabbitMQ not ready: {exc}")
            await asyncio.sleep(5)
