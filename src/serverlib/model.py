from uuid import UUID

import pandas as pd
from loglib.typing import LogEntry


class LogFile:
    def __init__(self, name: str, uuid: UUID):
        self.name = name
        self.uuid = uuid
        self.entries: list[LogEntry] = []

    def add_entry(self, entry: LogEntry):
        self.entries.append(entry)

    def get_snapshot(self) -> pd.DataFrame:
        print(self.name)
        return pd.DataFrame()

    def __str__(self):
        return str(self.entries)

    def __repr__(self):
        return repr(self.entries)

class LogFileManager:
    def __init__(self):
        self.files: dict[str, LogFile] = {}

    def route_entry(self, entry: LogEntry):
        if str(entry.info.uuid) not in self.files.keys():
            self.files[str(entry.info.uuid)] = LogFile(entry.info.name, entry.info.uuid)
        self.files[str(entry.info.uuid)].add_entry(entry)