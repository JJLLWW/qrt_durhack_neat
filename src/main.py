import asyncio
import logging

# this is why there should probably be some global api
from loglib.loader.log_dir_watcher import LogDirWatcher
from loglib.loader.log_event_bus import LogEventBus
from loglib.loader.log_manager import OpenLogManager


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


class EventLogger:
    def handle_log_event(self, event):
        print(event)


async def main():
    log_eb = LogEventBus()
    log_eb.add_subscriber(EventLogger())
    log_dir = "./rough/log_dir"
    with LogDirWatcher(log_dir, log_eb) as watcher:
        await asyncio.sleep(200)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())