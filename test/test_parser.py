from io import StringIO
import datetime

import pytest

from ..src.loader.parser import *

# possible to run pytest from within pycharm
# https://www.jetbrains.com/help/pycharm/run-debug-configuration-py-test.html

# surely this should be within a file
multiline1 = """04-11-2023 12:36:16.542765000 INFO: 
Exchange order message timing output
  Exchange            Order recv nu  X (us)
      King           timing   14113     480
      King           update    8290    1092
      King           delete   18434     326
      King              add   11362     766
      King  additional_info    8170    1032
     Queen           timing   11074     652
     Queen           update   19825     898
     Queen           delete   19214     427
     Queen              add   13472     787
     Queen  additional_info    9107     757
    Bishop           timing    9907     638
    Bishop           update   13252     811
    Bishop           delete   18454     459
    Bishop              add    8194     560
    Bishop  additional_info   14037     742
      Rook           timing   13392     618
      Rook           update   13519     508
      Rook           delete    8219     476
      Rook              add   11842     879
      Rook  additional_info    9443    1046
    Knight           timing   15564     321
    Knight           update   18448    1010
    Knight           delete   13267     356
    Knight              add   19793     486
    Knight  additional_info   18624    1303
"""

def test_parser_one_line_success():
    log_parser = LogParser()
    # check if a blank line will cause problems - believe it does
    inputs = [
        "04-11-2023 12:36:15.739592000 DEBUG: Hello World",
        "04-11-2023 12:36:16.542765000 INFO: a"
    ]
    expected = [
        LogEntry(timestamp=datetime(2023, 11, 4, 12, 36, 15, 739592), status="DEBUG", message="Hello World"),
        LogEntry(timestamp=datetime(2023, 11, 4, 12, 36, 16, 542765), status="INFO", message="a")
    ]
    actual = [log_parser.parse_log_entry_head(line) for line in inputs]
    assert actual == expected


def test_parser_complex_success():
    log_parser = LogParser()
    log_parser.parse_static_logfile(StringIO(multiline1))


def test_parser_failure_1():
    log_parser = LogParser()
    inputs = [
        "nonsense",
        "04-13-2023 12:36:16.542765000 INFO: Bad Date"
    ]
    for line in inputs:
        with pytest.raises(Exception) as e_info:
            log_parser.parse_log_entry_head(line)