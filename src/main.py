import asyncio
import logging

from loglib.cli_parser import cli_main
from loglib.rmq import connection_loop, create_connection


def setup_logging():
    logging.basicConfig(level=logging.INFO)


async def main():
    cmd = cli_main()
    conn = await create_connection()
    queue = asyncio.Queue()
    stop = asyncio.Event()
    async with asyncio.TaskGroup() as tg:
        cmd_task = tg.create_task(cmd.execute(queue, stop))
        rmq_task = tg.create_task(connection_loop(conn, queue, stop))


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
