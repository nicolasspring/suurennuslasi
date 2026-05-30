import json

import aio_pika

from suurennuslasi_messaging.session import get_connection


async def publish(queue_name: str, payload: dict):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(
            queue_name,
            durable=True,
        )
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(payload).encode()),
            routing_key=queue.name,
        )
