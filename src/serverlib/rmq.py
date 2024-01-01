from os import getenv

import aio_pika
from loglib.json_serialise import decode_log_entry

from .model import LogFileManager


def get_rmq_url() -> str:
    if getenv('IN_DOCKER_CONTAINER') is not None:
        return "amqp://guest:guest@rmq/"
    else:
        return "amqp://guest:guest@127.0.0.1/"


async def get_rmq_connection():
    return await aio_pika.connect(get_rmq_url())


async def rmq_consumer(file_manager: LogFileManager, connection) -> None:
    queue_name = "test_queue"

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                entry = decode_log_entry(message.body.decode('utf-8'))
                file_manager.route_entry(entry)
