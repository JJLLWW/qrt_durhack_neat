import io
import logging
import re
from datetime import datetime

import pandas as pd

from ..datamodel import LogEntry


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
def parse_statistics(entry: str) -> pd.DataFrame:
    stat_lines = entry.split("\n")[2:-1]
    stat_lines[0] = stat_lines[0].replace("recv nu", "recv_nu")
    stat_lines[0] = stat_lines[0].replace("X (us)", "X")
    stat_lines = [line.lstrip() for line in stat_lines]
    stats_chunk = "\n".join(stat_lines)
    stats_df = pd.read_csv(io.StringIO(stats_chunk), sep=r"\s+")
    return stats_df


def parse_log_entry(entry: str, line_re: str = _default_line_regex) -> LogEntry:
    line_pattern = re.compile(line_re, re.MULTILINE | re.DOTALL)
    match = line_pattern.match(entry)
    stats = None
    if match is None:
        logger.error(f"failed to parse line '{entry}'")
        raise ValueError("unable to parse input line")
    if len(entry.split("\n")) > 2:
        stats = parse_statistics(entry)
    return LogEntry(
        timestamp=_convert_timestamp(match.group("timestamp")),
        status=match.group("status").strip(":"),
        message=match.group("message"),
        statistics=stats,
    )


def is_log_head(line: str, line_re: str = _default_line_regex) -> bool:
    line_pattern = re.compile(line_re)
    match = line_pattern.match(line)
    return match is not None
