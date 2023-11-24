from io import StringIO
import datetime

import pytest

from ..src.loader.parser import *


def test_parser_one_line_success():
    log_parser = LogParser()
    inputs = [
        "04-11-2023 12:36:15.739592000 DEBUG: Hello World",
        "04-11-2023 12:36:16.542765000 INFO: a"
    ]
    expected = [
        LogEntry(timestamp=datetime(2023, 11, 4, 12, 36, 15, 739592), status="DEBUG", message="Hello World"),
        LogEntry(timestamp=datetime(2023, 11, 4, 12, 36, 16, 542765), status="INFO", message="a")
    ]
    actual = [log_parser.parse_log_entry(line) for line in inputs]
    assert actual == expected


def test_parser_failure_1():
    log_parser = LogParser()
    inputs = [
        "nonsense",
        "04-13-2023 12:36:16.542765000 INFO: Bad Date",
        ""
    ]
    for line in inputs:
        with pytest.raises(Exception) as e_info:
            log_parser.parse_log_entry(line)


def test_check_multiline():
    log_parser = LogParser()
    msg = "this\n is\n multiline\n"
    line = f"04-11-2023 12:36:15.739592000 DEBUG: {msg}"
    val = log_parser.parse_log_entry(line)
    assert val.message == msg
