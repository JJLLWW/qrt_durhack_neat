import pandas as pd
from collections import namedtuple

LogEntry = namedtuple(
    typename="LogEntry",
    field_names=["timestamp", "status", "message", "statistics"]
)


class LogFile:
    def __init__(self):
        self.log_entries = []

    def add_entry(self, entry: LogEntry):
        self.log_entries.append(entry)

    def add_entries(self, entries: list[LogEntry]):
        for entry in entries:
            self.add_entry(entry)

    def get_file_snapshot(self) -> pd.DataFrame:
        # this won't behave as expected.
        return pd.DataFrame(data=self.log_entries)