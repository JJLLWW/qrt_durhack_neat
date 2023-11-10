import pandas as pd

from typing import TextIO
import time
import asyncio

from .parser import LogParser
from .entry import LogEntry


# nice apparently async/await are in 3.5+, determines coroutine (they aren't actually parallelised)
# asyncio in stdlib? https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio
# asyncio has StreamReader class
# probably better to use aiofiles
# main needs to be wrapped in asyncio.run(main())
class RealTimeLogManager:
    """ manages files open for real time reading """
    def __init__(self):
        self.parser = LogParser()
        self.log_files: dict[str, TextIO] = {}
        self.log_entries: dict[str, list[LogEntry]] = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        for log_file in self.log_files.values():
            log_file.close()

    def poll_all_files_once(self):
        for log_key, log_file in self.log_files.items():
            line = log_file.readline()
            if line != '' and line != '\n':
                if self.parser.is_entry_head(line):
                    entry = self.parser.parse_log_entry_head(line)
                    self.log_entries[log_key].append(entry)
                else:
                    self.log_entries[log_key][-1].message += line

    def poll_all_files(self):
        # surely there's some way to do this asynchronously
        while True:
            time.sleep(0.1)
            self.poll_all_files_once()

    def remove_file(self, log_key: str):
        if log_key not in self.log_files.keys():
            return
        file = self.log_files[log_key]
        self.log_entries.pop(log_key)
        self.log_files.pop(log_key)
        file.close()

    def add_file(self, log_path: str):
        # TODO: what if the path is invalid
        log_file = open(log_path)
        self.log_files[log_path] = log_file
        self.log_entries[log_path] = []