# their example, does it work? if this is using multiple threads how will it interface
# with coroutines from async io?
# - doesn't work with coroutines, however there is the "watchfiles" library which might be better
import sys
import time
import logging
import asyncio

import aiofiles
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent


async def file_coro(filename: str):
    async with aiofiles.open(filename, mode='r') as f:
        while True:
            line = await f.readline()
            if line:
                print(f"{filename}: {line}", end='')
            else:
                await asyncio.sleep(1)


# can't create a new event loop in this class since its constructed
# in the
class TestEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.live_tasks = {}

    def on_created(self, event: FileCreatedEvent):
        task = asyncio.create_task(file_coro(event.src_path))
        self.live_tasks[event.src_path] = task

    def on_deleted(self, event: FileDeletedEvent):
        if event.src_path in self.live_tasks:
            self.live_tasks[event.src_path].cancel()
            self.live_tasks.pop(event.src_path)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = TestEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()