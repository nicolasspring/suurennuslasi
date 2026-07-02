import asyncio

import aio_pika

from suurennuslasi_messaging.session import get_connection


async def subscribe(
    exchange_name: str,
    queue_name: str,
    handlers: dict[str, callable],
):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
        )
        queue = await channel.declare_queue(
            queue_name,
        )
        for routing_key, callback in handlers.items():
            await queue.bind(
                exchange,
                routing_key=routing_key,
            )
        await queue.consume(callback)
        await asyncio.Future()
