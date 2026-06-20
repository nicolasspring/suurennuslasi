import asyncio
import os

import aio_pika


async def get_connection():
    while True:
        try:
            print("Connecting to RabbitMQ...")
            conn = await aio_pika.connect_robust(
                f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@rabbitmq/"
            )
            print("Connected to RabbitMQ")
            return conn
        except Exception as exc:
            print(f"RabbitMQ not ready: {exc}")
            await asyncio.sleep(5)
