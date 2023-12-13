import asyncio
import glob
import logging

from watchfiles import awatch

from .log_file_watcher import LogFileWatcher
from .log_event_bus import LogEventBus
from ..datamodel.log_event import LogEvent, EventType

logger = logging.getLogger(__name__)


# really? must be a better way
def _get_file_watcher_cb(file: str, event_bus: LogEventBus):
    def cb(entry):
        event = LogEvent(EventType.NEW_ENTRY, file, entry)
        event_bus.publish(event)
    return cb


# TODO: warn user if being called with no asyncio event loop
class LogDirWatcher:
    def __init__(self, dir_path: str, event_bus: LogEventBus):
        self.dir_path = dir_path
        self.event_bus = event_bus
        self.file_watchers: dict[str, LogFileWatcher] = {}
        self.watch_task = None

    def _watch_existing_logs(self):
        logs = glob.glob(f"{self.dir_path}/*.log")
        for log in logs:
            self._watch_file(log)

    def _watch_file(self, file: str):
        self.event_bus.publish(LogEvent(EventType.FILE_OPEN, file, None))
        new_entry_cb = _get_file_watcher_cb(file, self.event_bus)
        self.file_watchers[file] = LogFileWatcher(file, new_entry_cb)

    def _unwatch_file(self, file: str, do_pop=True):
        self.file_watchers[file].stop_watch()
        if do_pop:
            self.file_watchers.pop(file)
        self.event_bus.publish(LogEvent(EventType.FILE_CLOSE, file, None))

    def _handle_dir_changes(self, changes):
        for change, file in changes:
            match change:
                case change.added:
                    self._watch_file(file)
                case change.deleted:
                    if file in self.file_watchers:
                        self._unwatch_file(file)

    async def _watch_loop(self):
        self._watch_existing_logs()
        async for changes in awatch(self.dir_path):
            self._handle_dir_changes(changes)

    def start_watch(self):
        logger.debug(f"starting watch on directory {self.dir_path}")
        self.watch_task = asyncio.create_task(self._watch_loop())

    def stop_watch(self):
        logger.debug(f"stopping watch on directory {self.dir_path}")
        if self.watch_task:
            self.watch_task.cancel()
        for file in self.file_watchers.keys():
            self._unwatch_file(file, do_pop=False)

    def __enter__(self):
        self.start_watch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()
