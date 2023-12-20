""" ! PROOF OF CONCEPT ONLY ! """
import argparse
import asyncio
import pathlib
import logging
from typing import Iterable, Optional

from loglib.datamodel.log_event import LogEvent
from loglib.loader.static_loader import stream_static_logfile
from loglib.loader.log_file_watcher import LogFileWatcher
from loglib.loader.log_dir_watcher import LogDirWatcher, get_file_watcher_event_bus_cb
from loglib.loader.log_event_bus import LogEventBus
from loglib.net.web_socket_client import WSocketEventForwarder

logger = logging.getLogger(__name__)


# can hook into type with some function doing validation, then raise a ValueError etc.
cli_parser = argparse.ArgumentParser()
s_help = "statically load these log files"
w_help = "watch this log file in real time"
d_help = "watch this directory for changes to log files within it"
cli_parser.add_argument(
    "-s", "--static", nargs="+", metavar="LOGFILE", type=pathlib.Path, help=s_help
)
cli_parser.add_argument(
    "-f", "--file-watch", nargs="+", metavar="LOGFILE", type=pathlib.Path, help=w_help
)
cli_parser.add_argument(
    "-d", "--dir-watch", nargs="+", metavar="DIRECTORY", type=pathlib.Path, help=d_help
)


# DEBUG ONLY
class EventLogger:
    def handle_log_event(self, event: LogEvent):
        print(event)


async def cli_main():
    args = parse_argv()
    event_bus = LogEventBus()
    ws_forwarder = WSocketEventForwarder()
    event_bus.add_subscriber(ws_forwarder)
    dir_watchers, file_watchers = [], []
    if args.static:
        for path in args.static:
            file = str(path)
            stream_cb = get_file_watcher_event_bus_cb(file, event_bus)
            with open(file) as f:
                stream_static_logfile(f, stream_cb)
        logging.info("all static files loaded successfully")
    if args.file_watch or args.dir_watch:
        if args.file_watch:
            for path in args.file_watch:
                file = str(path)
                fw_callback = get_file_watcher_event_bus_cb(file, event_bus)
                file_watchers.append(LogFileWatcher(file, fw_callback))
        if args.dir_watch:
            for path in args.dir_watch:
                dir_watcher = LogDirWatcher(str(path), event_bus)
                dir_watchers.append(dir_watcher)
        logging.info("all watches added successfully")
        await asyncio.Event().wait()  # hang forever


def parse_argv():
    args = cli_parser.parse_args()
    validate_args(args)
    return args


def validate_args(args):
    if not any(vars(args).values()):
        cli_parser.error("at least one argument is required")
    validate_paths(args.static)
    validate_paths(args.file_watch)
    validate_paths(args.dir_watch, is_dir=True)


def validate_paths(paths: Optional[Iterable[pathlib.Path]], is_dir: bool = False):
    if paths is None:
        return
    for path in paths:
        if is_dir and not path.is_dir():
            cli_parser.error(f"path '{path}' is not directory")
        if not is_dir and not path.is_file():
            cli_parser.error(f"path '{path}' is not regular file")
