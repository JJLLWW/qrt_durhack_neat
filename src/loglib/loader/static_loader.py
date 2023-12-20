import logging
from typing import Callable, TextIO

from ..datamodel import LogEntry, LogFile
from .log_entry_stream import LogEntryStream


logger = logging.getLogger(__name__)


# TODO: implement in terms of stream static logfile
def load_static_logfile(buf: TextIO) -> LogFile:
    stream = LogEntryStream()
    file = LogFile()
    stream.register_callback(lambda entry: file.add_entry(entry))
    for line in buf:
        stream.add_line(line)
    stream.flush()
    return file


def stream_static_logfile(buf: TextIO, entry_cb: Callable[[LogEntry], None]):
    stream = LogEntryStream()
    stream.register_callback(entry_cb)
    for line in buf:
        stream.add_line(line)
    stream.flush()
