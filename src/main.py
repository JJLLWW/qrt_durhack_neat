import asyncio
import logging

# this is why there should probably be some global api
from loglib.loader.log_dir_watcher import LogDirWatcher
from loglib.loader.log_event_bus import LogEventBus
from loglib.datamodel.log_event import LogEvent
from loglib.net.web_socket_client import WSocketEventForwarder
from loglib.cli.cli_parser import cli_main


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)


class EventLogger:
    def handle_log_event(self, event: LogEvent):
        print(event)


async def main():
    log_eb = LogEventBus()
    log_eb.add_subscriber(EventLogger())
    log_eb.add_subscriber(WSocketEventForwarder())
    log_dir = "./rough/log_dir"
    with LogDirWatcher(log_dir, log_eb):
        await asyncio.sleep(200)


if __name__ == "__main__":
    setup_logging()
    # asyncio.run(main())
    asyncio.run(cli_main())
