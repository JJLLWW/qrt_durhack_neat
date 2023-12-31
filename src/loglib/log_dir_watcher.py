import asyncio
import glob
import logging

from watchfiles import awatch

from loglib.file_reader import FileReader


logger = logging.getLogger(__name__)


class LogDirWatcher:
    """
    Watch all log files present and created in a directory, monitoring for
    new entries.

    :param dir_path: path to the directory to watch
    :param queue: publish all new log entries to this queue
    """
    def __init__(self, dir_path: str, queue: asyncio.Queue):
        self.dir_path = dir_path
        self.queue = queue
        self.file_readers: dict[str, FileReader] = {}
        self.watch_task = None

    def _watch_existing_logs(self):
        logs = glob.glob(f"{self.dir_path}/*.log")
        for log in logs:
            self._watch_file(log)

    def _watch_file(self, file: str):
        self.file_readers[file] = FileReader(file, self.queue)

    def _unwatch_file(self, file: str, do_pop=True):
        self.file_readers[file].stop_read()
        if do_pop:
            self.file_readers.pop(file)

    def _handle_dir_changes(self, changes):
        for change, file in changes:
            match change:
                case change.added:
                    self._watch_file(file)
                case change.deleted:
                    if file in self.file_readers:
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
        for file in self.file_readers.keys():
            self._unwatch_file(file, do_pop=False)

    def __enter__(self):
        self.start_watch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()
