import asyncio
import logging

from loglib.cli_parser import cli_main


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


async def main():
    queue = asyncio.Queue()
    await cli_main(queue)
    while True:
        entry = await queue.get()
        print(entry)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
