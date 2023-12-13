import asyncio
import glob
import logging
import re

import aiofiles
from watchfiles import awatch

from .log_parser import LogParser
from .log_event_bus import LogEventBus
from ..datamodel.log_dir_event import LogDirEvent, EventType

logger = logging.getLogger(__name__)


# is it possible to have this class manage its own event loop so surrounding code
# doesn't have to use asyncio.run()? <- not sure this is a good idea
class LogDirWatcher:
    def __init__(self, dir_path: str, event_bus: LogEventBus):
        self.dir_path = dir_path
        self.event_bus = event_bus
        self.parser = LogParser()
        self.file_tasks = {}
        self.watch_task = None

    def _watch_existing_logs(self):
        logs = glob.glob(f"{self.dir_path}/*.log")
        for log in logs:
            self._watch_file(log)

    def _watch_file(self, file: str):
        self.file_tasks[file] = asyncio.create_task(self._get_file_entries(file))
        self.event_bus.publish(LogDirEvent(EventType.FILE_OPEN, file, None))
        logger.debug(f"watching file {file}")

    def _unwatch_file(self, file: str, do_pop=True):
        self.file_tasks[file].cancel()
        if do_pop:
            self.file_tasks.pop(file)
        self.event_bus.publish(LogDirEvent(EventType.FILE_CLOSE, file, None))
        logger.debug(f"unwatching file {file}")

    def _handle_dir_changes(self, changes):
        for change, file in changes:
            match change:
                case change.added:
                    self._watch_file(file)
                case change.deleted:
                    if file in self.file_tasks:
                        self._unwatch_file(file)

    async def _watch_loop(self):
        self._watch_existing_logs()
        async for changes in awatch(self.dir_path):
            self._handle_dir_changes(changes)

    # do not use this for files that are not still being written as will miss the last line
    async def _get_file_entries(self, file: str):
        entry_head_pat = re.compile(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+ \w+: .*$")
        cur_entry = ""
        async with aiofiles.open(file, mode='r') as f:
            while True:
                line = await f.readline()
                if line:
                    if re.match(entry_head_pat, line) is not None:
                        if cur_entry != "":
                            entry = self.parser.parse_log_entry(cur_entry)
                            cur_entry = ""
                            self.event_bus.publish(LogDirEvent(EventType.NEW_ENTRY, file, entry))
                    cur_entry += line
                else:
                    await asyncio.sleep(1)  # surely a better way?

    def start_watch(self):
        logger.debug(f"starting watch on directory {self.dir_path}")
        self.watch_task = asyncio.create_task(self._watch_loop())

    def stop_watch(self):
        logger.debug(f"stopping watch on directory {self.dir_path}")
        if self.watch_task:
            self.watch_task.cancel()
        for file in self.file_tasks.keys():
            self._unwatch_file(file, do_pop=False)

    def __enter__(self):
        self.start_watch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()