import pandas as pd
import logging
from .parser import LogParser
from .real_time import RealTimeLogManager


class LogLoader():
    """ Loader class for reading log files and storing their data """

    def __init__(self):
        self.rt_manager = RealTimeLogManager()
        self.log_buffers = [] # temporary
        self.logger = logging.getLogger(__name__)
        self.parser = LogParser()

    def __enter__(self):
        return self

    def load_log_snapshot(self, log_path: str):
        """ file has been opened in snapshot mode, so process all lines currently in the file """
        with open(log_path) as log_file:
            snapshot_df = self.parser.parse_static_logfile(log_file)
            self.log_buffers.append(snapshot_df)
        return None

    def track_log_file(self, log_path: str):
        """ track this log file in real time """
        pass