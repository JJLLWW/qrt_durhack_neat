import pandas as pd
import logging
from .parser import LogParser


class LogLoader():
    """ Loader class for reading log files """

    def __init__(self):
        self.open_logs = {}
        self.log_buffers = [] # temporary
        self.logger = logging.getLogger(__name__)
        self.parser = LogParser()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for log_file in self.open_logs.values():
            log_file.close()

    def load_log_snapshot(self, log_path: str):
        with open(log_path) as log_file:
            snapshot_df = self.parser.parse_static_logfile(log_file)
            self.log_buffers.append(snapshot_df)
        return None

    def load_real_time_log(self, log_path: str):
        return None