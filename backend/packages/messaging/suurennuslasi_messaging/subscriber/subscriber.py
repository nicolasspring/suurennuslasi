import asyncio

import aio_pika

from suurennuslasi_messaging.session import get_connection


async def subscribe(
    queue_name: str,
    callback,
):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        await queue.consume(callback, no_ack=True)
        await asyncio.Future()
