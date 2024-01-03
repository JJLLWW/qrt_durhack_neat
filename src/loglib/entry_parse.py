import logging
import re
from datetime import datetime

from loglib.typing import ExchangeStats, LogEntry, LogEntryData


logger = logging.getLogger(__name__)


_default_line_regex = r"^(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+) (?P<status>\w+:) (?P<message>.*)$"
_default_timestamp_format = "%d-%m-%Y %H:%M:%S.%f"


def _correct_nanos(timestamp: str) -> str:
    """python datetime can only store time up to microsecond precision, but log can
    store nanosecond precision, so ignore the nanosecond digits"""
    chunks = timestamp.split(".")
    chunks[1] = chunks[1][:6]
    return ".".join(chunks)


def _convert_timestamp(
    timestamp: str, timestamp_format: str = _default_timestamp_format
) -> datetime:
    timestamp = _correct_nanos(timestamp)
    return datetime.strptime(timestamp, timestamp_format)


# this assumes the only multiline log entries are "exchange order timing..." entries
def parse_statistics(entry: str) -> list[ExchangeStats]:
    stats = []
    for line in entry.split('\n')[3:-2]:
        columns = line.lstrip().split()
        next_stat = ExchangeStats(exchange=columns[0], order=columns[1], recv_nu=int(columns[2]), X=int(columns[3]))
        stats.append(next_stat)
    return stats  # TODO: DOESN'T WORK PROPERLY WITH PYDANTIC


def parse_log_entry(entry: str, line_re: str = _default_line_regex) -> LogEntry:
    line_pattern = re.compile(line_re, re.MULTILINE | re.DOTALL)
    match = line_pattern.match(entry)
    stats = []
    if match is None:
        logger.error(f"failed to parse line '{entry}'")
        raise ValueError("unable to parse input line")
    if len(entry.split("\n")) > 2:
        stats = parse_statistics(entry)
    data = LogEntryData(
        timestamp=_convert_timestamp(match.group("timestamp")),
        status=match.group("status").strip(":"),
        message=match.group("message"),
        stats=stats
    )
    return LogEntry(
        data=data,
        info=None
    )


def is_log_head(line: str, line_re: str = _default_line_regex) -> bool:
    line_pattern = re.compile(line_re)
    match = line_pattern.match(line)
    return match is not None
