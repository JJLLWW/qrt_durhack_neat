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
        assert val == ''.join(output)


def test_log_iterator_multiline_entries():
    entry1 = """04-11-2023 21:06:30.725677000 INFO: 
Exchange order message timing output
  Exchange            Order recv nu  X (us)
      King           timing   14113     480
      King           update    8290    1092
      King           delete   18434     326
      King              add   11362     766
      King  additional_info    8170    1032
     Queen           timing   11074     652
     Queen           update   19825     898
"""
    entry2 = "04-11-2023 21:04:30.29734000 DEBUG: Received heartbeat from exchange *Rook*"
    expected = [entry1, entry2]
    multiline = ''.join(expected)
    it = StringIO(multiline)
    log_it = LogIterator(it)
    output = [entry for entry in log_it]
    assert len(output) == len(expected)
    assert output == expected