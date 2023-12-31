import asyncio
import logging

from loglib.cli_parser import cli_main


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


async def main():
    queue = asyncio.Queue()
    stop_cli = asyncio.Event()
    await cli_main(queue, stop_cli)
    while not stop_cli.is_set() or not queue.empty():
        entry = await queue.get()
        print(entry)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
