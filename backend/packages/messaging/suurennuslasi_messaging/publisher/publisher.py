import json

import aio_pika

from suurennuslasi_messaging.session import get_connection


async def publish(
    exchange_name: str,
    routing_key: str,
    payload: dict,
):
    connection = await get_connection()

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            exchange_name,
            aio_pika.ExchangeType.TOPIC,
        )
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
            ),
            routing_key=routing_key,
        )
