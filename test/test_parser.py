from ..src.loader.parser import *


def test_loader_succeed():
    log_parser = LogParser()
    lines = [
        "04-11-2023 12:36:15.739592000 DEBUG: Entering unimportant code area!!!",
        "04-11-2023 12:36:16.542765000 INFO: "
    ]
    for line in lines:
        ent = log_parser.parse_log_entry_head(line)
        print(ent)
    assert True


def test_read_file():
    log_parser = LogParser()
    with open("./data/frozen_output.log") as f:
        entries = log_parser.parse_static_logfile(f)