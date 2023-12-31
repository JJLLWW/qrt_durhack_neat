import asyncio
import logging

from loglib.cli_parser import cli_main


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


async def main():
    cmd = cli_main()
    queue = asyncio.Queue()
    await cmd.execute(queue)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
