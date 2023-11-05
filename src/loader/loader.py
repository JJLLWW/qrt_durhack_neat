import pandas as pd
import logging
from .format_helpers import *

class LogLoader():
    """ Loader class for reading log files """
    def __init__(self):
        self.open_logs = {}
        self.log_buffers = {}
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for log_file in self.open_logs.values():
            log_file.close()

    def load_log_snapshot(self, log_path: str):
        snapshot_df = pd.DataFrame(columns=['Timestamp', 'Status', 'Message'])
        with open(log_path) as log_file:
            for line in log_file:
                if is_exchange_timing_preamble(line):
                    break
                    # parse_exchange_timing_snapshot(log_file)
                else:
                    line_df = parse_single_line_entry(line)
                    snapshot_df = pd.concat([snapshot_df, line_df]) # bit awful

        return None

    def load_real_time_log(self, log_path: str):
        return None