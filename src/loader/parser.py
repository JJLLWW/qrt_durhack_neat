import re
from datetime import datetime
from typing import TextIO
import pandas as pd
import logging

from .entry import LogEntry


# TextIO can be a file or also some StringReader equivalent so not locked in to a file.
class LogParser:
    default_line_regex = r"^(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+) (?P<status>\w+:) (?P<message>.*)$"
    default_timestamp_format = "%d-%m-%Y %H:%M:%S.%f"

    def __init__(self, line_regex: str = default_line_regex, timestamp_format: str = default_timestamp_format):
        self.logger = logging.getLogger(__name__)
        self.line_pattern = re.compile(line_regex)
        self.timestamp_format = timestamp_format

    @staticmethod
    def __correct_nanos(timestamp: str) -> str:
        """ python datetime can only store time up to microsecond precision, but log can
            store nanosecond precision, so ignore the nanosecond digits"""
        chunks = timestamp.split('.')
        chunks[1] = chunks[1][:6]
        return '.'.join(chunks)

    def __convert_timestamp(self, timestamp: str) -> datetime:
        timestamp = LogParser.__correct_nanos(timestamp)
        return datetime.strptime(timestamp, self.timestamp_format)

    def parse_log_entry_head(self, line: str) -> LogEntry:
        match = self.line_pattern.match(line)
        if match is None:
            self.logger.error(f"parser failed to parse line '{line}'")
            raise ValueError("unable to parse input line")
        return LogEntry(
            timestamp=self.__convert_timestamp(match.group('timestamp')),
            status=match.group('status').strip(':'),
            message=match.group('message')
        )

    def is_entry_head(self, line: str) -> bool:
        return self.line_pattern.match(line) is not None

    def parse_static_logfile(self, log_file: TextIO):
        entries = []
        while (line := log_file.readline()) != '':
            entry = self.parse_log_entry_head(line)
            if entry.message == '':
                line = log_file.readline()
                while line != '\n':
                    entry.message += line
                    line = log_file.readline()
            entries.append(entry)
        return pd.DataFrame([entry.as_dict() for entry in entries])
