import logging
from typing import TextIO

from .log_entry_stream import LogEntryStream
from ..datamodel.log_file import LogFile

logger = logging.getLogger(__name__)


def load_static_logfile(buf: TextIO) -> LogFile:
    stream = LogEntryStream()
    file = LogFile()
    stream.register_callback(lambda entry: file.add_entry(entry))
    for line in buf:
        stream.add_line(line)
    stream.flush()
    return file
