import argparse
import logging
import pathlib
from typing import Iterable, Optional

from .command import *


logger = logging.getLogger(__name__)


# TODO: should this really be outside any function?
cli_parser = argparse.ArgumentParser()
s_help = "statically load these log files"
w_help = "watch this log file in real time"
d_help = "watch this directory for changes to log files within it"
group = cli_parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-s", "--static", nargs="+", metavar="LOGFILE", type=pathlib.Path, help=s_help
)
group.add_argument(
    "-f", "--file-watch", nargs="+", metavar="LOGFILE", type=pathlib.Path, help=w_help
)
group.add_argument(
    "-d", "--dir-watch", nargs="+", metavar="DIRECTORY", type=pathlib.Path, help=d_help
)


def cli_main() -> Command:
    args = parse_argv()
    if args.static:
        return StaticFileCommand(file_paths=[str(path) for path in args.static])
    elif args.file_watch:
        return FileWatchCommand(file_paths=[str(path) for path in args.file_watch])
    elif args.dir_watch:
        return DirWatchCommand(dir_paths=[str(path) for path in args.dir_watch])


def parse_argv():
    args = cli_parser.parse_args()
    validate_args(args)
    return args


def validate_args(args):
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
