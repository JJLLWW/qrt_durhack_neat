import asyncio
import logging
import re

import aiofiles

from .log_parser import parse_log_entry
from .log_event_bus import LogEventBus
from ..datamodel.log_dir_event import LogEvent, EventType

logger = logging.getLogger(__name__)


# bug where does not read the last line - surely some way to dump this somewhere else
async def _get_file_entries(file: str, event_bus: LogEventBus):
    entry_head_pat = re.compile(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+ \w+: .*$")
    cur_entry = ""
    async with aiofiles.open(file, mode='r') as f:
        while True:
            line = await f.readline()
            if line:
                if re.match(entry_head_pat, line) is not None:
                    if cur_entry != "":
                        entry = parse_log_entry(cur_entry)
                        cur_entry = ""
                        event_bus.publish(LogEvent(EventType.NEW_ENTRY, file, entry))
                cur_entry += line
            else:
                await asyncio.sleep(1)  # surely a better way?


# - this will not notice if the underlying file is deleted on its own.
class LogFileWatcher:
    def __init__(self, file: str, event_bus: LogEventBus):
        self.file: str = file
        self.event_bus: LogEventBus = event_bus
        logger.debug(f"watching file {file}")
        self.watch_task: asyncio.Task = asyncio.create_task(_get_file_entries(file, event_bus))

    def stop_watch(self):
        logger.debug(f"unwatching file {self.file}")
        self.watch_task.cancel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()