import pandas as pd
from collections import namedtuple

LogEntry = namedtuple(
    typename="LogEntry",
    field_names=["timestamp", "status", "message", "statistics"]
)

LogFileEntry = namedtuple(
    typename="LogFileEntry",
    field_names=["timestamp", "status", "message", "stats_id"]
)


# not thread safe
class LogFile:
    def __init__(self):
        self.log_entries: list[LogFileEntry] = []
        self.stat_frames: list[pd.DataFrame] = []
        self.snapshot = None

    def add_entry(self, entry: LogEntry):
        file_entry = LogFileEntry(entry.timestamp, entry.status, entry.message, None)
        if entry.statistics is not None:
            stat_id = len(self.stat_frames)
            file_entry.stats_id = stat_id
            self.stat_frames.append(entry.statistics)
        self.log_entries.append(file_entry)

    def add_entries(self, entries: list[LogEntry]):
        for entry in entries:
            self.add_entry(entry)

    # TODO: what about the stats auxiliary data frames?
    def get_file_snapshot(self, regenerate=True) -> pd.DataFrame:
        if self.snapshot is None or regenerate:
            self.snapshot = pd.DataFrame(data=self.log_entries)
        return self.snapshot
