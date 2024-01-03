from loglib.entry_parse import parse_log_entry
from loglib.typing import LogEntry


def test_json():
    entry = parse_log_entry("04-11-2023 12:36:15.739592000 DEBUG: Hello World\n")
    json = entry.model_dump_json()
    entry_back = LogEntry.model_validate_json(json)
    print(entry_back)