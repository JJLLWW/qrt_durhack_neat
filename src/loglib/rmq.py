import asyncio

import aio_pika

from .json_serialise import encode


async def create_connection():
    return await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")


async def connection_loop(
        connection: aio_pika.RobustConnection,
        queue: asyncio.Queue,
        stop: asyncio.Event
):
    routing_key = "test_queue"

    async with connection:
        channel = await connection.channel()
        while not stop.is_set() or not queue.empty():
            entry = await queue.get()
            as_json: str = encode(entry)
            await channel.default_exchange.publish(
                aio_pika.Message(body=as_json.encode()),
                routing_key=routing_key,
            )