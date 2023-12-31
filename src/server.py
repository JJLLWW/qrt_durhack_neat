""" PROOF OF CONCEPT ONLY! """
import asyncio
import logging
from os import getenv

import aio_pika
from loglib.json_serialise import decode_log_entry


def get_rmq_url() -> str:
    if getenv('IN_DOCKER_CONTAINER') is not None:
        return "amqp://guest:guest@rmq/"
    else:
        return "amqp://guest:guest@127.0.0.1/"


# TODO: Make types explicit - can this be run in the container?
async def server_main(aio_queue: asyncio.Queue) -> None:
    logging.basicConfig(level=logging.INFO)
    connection = await aio_pika.connect_robust(
        get_rmq_url()
    )

    queue_name = "test_queue"

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    entry = decode_log_entry(message.body.decode('utf-8'))
                    aio_queue.put_nowait(entry)


async def main():
    queue = asyncio.Queue()
    await server_main(queue)


if __name__ == "__main__":
    asyncio.run(main())