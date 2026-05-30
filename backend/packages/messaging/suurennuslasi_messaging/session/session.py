import os

import aio_pika


async def get_connection():
    return await aio_pika.connect_robust(
        f"amqp://{os.getenv("RABBITMQ_USER")}:{os.getenv("RABBITMQ_PASSWORD")}@rabbitmq/"
    )
