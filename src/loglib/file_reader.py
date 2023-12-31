import asyncio
import logging

from loglib.entry_helpers import get_next_entry_lines
from loglib.entry_parse import parse_log_entry


logger = logging.getLogger(__name__)


# this will not notice if the underlying file is deleted
class FileReader:
    def __init__(
            self,
            file_path: str,
            entry_queue: asyncio.Queue,
            watch: bool = False,
    ):
        self.file_path = file_path
        self.entry_queue = entry_queue
        self.watch = watch
        self.read_task: asyncio.Task = asyncio.create_task(self._read_file())

    async def _read_file(self):
        async for entry_lines in get_next_entry_lines(self.file_path, self.watch):
            entry = parse_log_entry(entry_lines)
            # TODO: ADD SOURCE INFO
            self.entry_queue.put_nowait(entry)
            pass

    def stop_read(self):
        self.read_task.cancel()