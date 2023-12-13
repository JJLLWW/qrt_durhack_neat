import asyncio
import logging
from typing import Callable

import aiofiles

from ..datamodel.log_file import LogEntry
from .log_entry_stream import LogEntryStream

logger = logging.getLogger(__name__)


# bug where don't get the last entry if a stream is closed unexpectedly.
async def _get_file_entries(file: str, entry_cb: Callable[[LogEntry], None]):
    stream = LogEntryStream()
    stream.register_callback(entry_cb)
    async with aiofiles.open(file, mode='r') as f:
        while True:
            line = await f.readline()
            if line:
                stream.add_line(line)
            else:
                await asyncio.sleep(1)  # surely a better way?


# - this will not notice if the underlying file is deleted on its own.
# TODO: warn user if being called with no asyncio event loop
class LogFileWatcher:
    def __init__(self, file: str, entry_cb: Callable[[LogEntry], None]):
        self.file: str = file
        logger.debug(f"watching file {file}")
        self.watch_task: asyncio.Task = asyncio.create_task(_get_file_entries(file,entry_cb))

    def stop_watch(self):
        logger.debug(f"unwatching file {self.file}")
        self.watch_task.cancel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()