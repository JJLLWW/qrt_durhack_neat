import asyncio
import logging
import uuid
from typing import Optional

from .entry_helpers import get_next_entry_lines
from .entry_parse import parse_log_entry
from .typing import SourceInfo


logger = logging.getLogger(__name__)


# this will not notice if the underlying file is deleted
class FileReader:
    def __init__(
            self,
            file_path: str,
            entry_queue: asyncio.Queue,
            watch: bool = False,
            barrier: Optional[asyncio.Barrier] = None
    ):
        self.file_path = file_path
        self.entry_queue = entry_queue
        self.watch = watch
        self.read_task: asyncio.Task = asyncio.create_task(self._read_file())
        self.barrier = barrier
        self.source_info = SourceInfo(name=self.file_path, uuid=uuid.uuid4())

    async def _read_file(self):
        async for entry_lines in get_next_entry_lines(self.file_path, self.watch):
            entry = parse_log_entry(entry_lines)
            entry.info = self.source_info
            self.entry_queue.put_nowait(entry)
        if self.barrier:
            await self.barrier.wait()

    async def stop_read(self):
        self.read_task.cancel()
        if self.barrier:
            await self.barrier.wait()