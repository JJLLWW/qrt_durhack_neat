import asyncio
import logging
import sys

print(sys.path)

# this is why there should probably be some global api
from loglib.loader.log_dir_watcher import LogDirWatcher
from loglib.loader.log_event_bus import LogEventBus
from loglib.loader.log_manager import OpenLogManager


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


async def main():
    log_eb = LogEventBus()
    log_manager = OpenLogManager()
    log_eb.add_subscriber(log_manager)
    log_dir = "./rough/log_dir"
    with LogDirWatcher(log_dir, log_eb) as watcher:
        await asyncio.sleep(200)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())