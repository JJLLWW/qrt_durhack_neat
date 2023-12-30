""" ! PROOF OF CONCEPT ONLY ! """
import argparse
import asyncio
import logging
import pathlib
from typing import Iterable, Optional

from .file_reader import FileReader
from .log_dir_watcher import LogDirWatcher


logger = logging.getLogger(__name__)


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


async def cli_main(queue: asyncio.Queue):
    args = parse_argv()
    dir_watchers, file_watchers = [], []
    if args.static:
        for path in args.static:
            file = str(path)
            file_watchers.append(FileReader(file, queue, watch=False))
    if args.file_watch:
        for path in args.file_watch:
            file = str(path)
            file_watchers.append(FileReader(file, queue, watch=True))
    if args.dir_watch:
        for path in args.dir_watch:
            dir_watcher = LogDirWatcher(str(path), queue)
            dir_watchers.append(dir_watcher)


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
