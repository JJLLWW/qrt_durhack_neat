# good proof of concept, is it possible to encapsulate any of this into a class?
# now just actually get the lines somewhere else
import asyncio
from collections import namedtuple


import aiofiles
from watchfiles import awatch


class FileObserver:
    def __init__(self, file: str):
        self.file = file

    def update(self, line: str):
        print(line)


async def file_coro(filename: str, observer: FileObserver):
    async with aiofiles.open(filename, mode='r') as f:
        while True:
            line = await f.readline()
            if line:
                observer.update(line)
            else:
                await asyncio.sleep(1)


FileInfo = namedtuple("FileInfo", ['task', 'observer'])


class LogLoader:
    def __init__(self):
        self.file_info = {}

    def handle_changes(self, changes):
        for change, file in changes:
            match change:
                case change.added:
                    # some strange issue with pycharm opening files but works with log producer.
                    observer = FileObserver(file)
                    task = asyncio.create_task(file_coro(file, observer))
                    self.file_info[file] = FileInfo(task=task, observer=observer)
                case change.deleted:
                    if file in self.file_info:
                        self.file_info[file].task.cancel()
                        self.file_info.pop(file)


async def main():
    loader = LogLoader()
    async for changes in awatch("log_dir"):
        loader.handle_changes(changes)


if __name__ == "__main__":
    asyncio.run(main())