
from loglib.typing import LogEntry, LogFile


class LogFileManager:
    def __init__(self):
        self.files: dict[str, LogFile] = {}

    def route_entry(self, entry: LogEntry):
        if str(entry.info.uuid) not in self.files.keys():
            self.files[str(entry.info.uuid)] = LogFile(info=entry.info)
        self.files[str(entry.info.uuid)].add_entry(entry)

    def add_file(self, file: LogFile):
        self.files[str(file.info.uuid)] = file