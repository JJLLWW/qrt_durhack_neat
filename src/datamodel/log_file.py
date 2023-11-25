import pandas as pd

from ..loader.entry import LogEntry


# does this have too little functionality to be a useful abstraction? [well
# check it works first] [apparently some python list operations, append etc. are thread safe].
class LogFile:
    def __init__(self):
        self.log_entries = []

    def add_entry(self, entry: LogEntry):
        self.log_entries.append(entry)

    def get_file_snapshot(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.log_entries)