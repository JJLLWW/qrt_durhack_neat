import pytest

from io import StringIO
from ..src.loader.log_iterator import LogIterator


def test_log_iterator_single_line_entries():
    # TODO: formatting
    inputs = [
        """04-11-2023 21:04:30.29720000 WARN: Received out of order message from exchange {Rook}
04-11-2023 21:04:30.29734000 DEBUG: Received heartbeat from exchange *Rook*
04-11-2023 21:04:30.29750000 DEBUG: Exiting unimportant code area"""
    ]
    for val in inputs:
        it = StringIO(val)
        log_it = LogIterator(it)
        output = [entry for entry in log_it]
        assert len(output) == len(val.split('\n'))
        assert val == '\n'.join(output)


def test_log_iterator_multiline_entries():
    assert True