import re
from datetime import datetime
import logging
import io

import pandas as pd

from src.datamodel.log_file import LogEntry

logger = logging.getLogger(__name__)


class LogParser:
    default_line_regex = r"^(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+) (?P<status>\w+:) (?P<message>.*)$"
    default_timestamp_format = "%d-%m-%Y %H:%M:%S.%f"

    def __init__(self, line_regex: str = default_line_regex, timestamp_format: str = default_timestamp_format):
        self.line_pattern = re.compile(line_regex, re.MULTILINE | re.DOTALL)
        self.timestamp_format = timestamp_format

    @staticmethod
    def _correct_nanos(timestamp: str) -> str:
        """ python datetime can only store time up to microsecond precision, but log can
            store nanosecond precision, so ignore the nanosecond digits"""
        chunks = timestamp.split('.')
        chunks[1] = chunks[1][:6]
        return '.'.join(chunks)

    def _convert_timestamp(self, timestamp: str) -> datetime:
        timestamp = LogParser._correct_nanos(timestamp)
        return datetime.strptime(timestamp, self.timestamp_format)

    # TODO: check stats entries have the correct dtypes
    # this assumes the only multiline log entries are "exchange order timing..." entries
    @staticmethod
    def parse_statistics(entry: str) -> pd.DataFrame:
        stat_lines = entry.split('\n')[2:-1]
        stat_lines[0] = stat_lines[0].replace("recv nu", "recv_nu")
        stat_lines[0] = stat_lines[0].replace("X (us)", "X")
        stat_lines = [line.lstrip() for line in stat_lines]
        stats_chunk = '\n'.join(stat_lines)
        stats_df = pd.read_csv(io.StringIO(stats_chunk), sep=r'\s+')
        return stats_df

    def parse_log_entry(self, entry: str) -> LogEntry:
        match = self.line_pattern.match(entry)
        stats = None
        if match is None:
            logger.error(f"parser failed to parse line '{entry}'")
            raise ValueError("unable to parse input line")
        if len(entry.split('\n')) > 1:
            stats = LogParser.parse_statistics(entry)
        return LogEntry(
            timestamp=self._convert_timestamp(match.group('timestamp')),
            status=match.group('status').strip(':'),
            message=match.group('message'),
            statistics=stats
        )
