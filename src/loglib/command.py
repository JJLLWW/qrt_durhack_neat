import asyncio

from .file_reader import FileReader
from .log_dir_watcher import LogDirWatcher


class Command:
    async def execute(self, queue: asyncio.Queue):
        raise NotImplementedError("execute not implemented")


class StaticFileCommand(Command):
    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths

    async def execute(self, queue: asyncio.Queue):
        barrier = asyncio.Barrier(len(self.file_paths) + 1)
        readers = []
        for file_path in self.file_paths:
            readers.append(FileReader(file_path, queue, watch=False, barrier=barrier))
        await barrier.wait()


class DirWatchCommand(Command):
    def __init__(self, dir_paths: list[str]):
        self.dir_paths = dir_paths

    async def execute(self, queue: asyncio.Queue):
        watchers = []
        for dir_path in self.dir_paths:
            watchers.append(LogDirWatcher(dir_path, queue))
        await asyncio.Event().wait()  # TODO: better way than to hang forever


class FileWatchCommand(Command):
    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths

    async def execute(self, queue: asyncio.Queue):
        readers = []
        for file_path in self.file_paths:
            readers.append(FileReader(file_path, queue, watch=True))
        await asyncio.Event().wait()  # TODO: better way than to hang forever
