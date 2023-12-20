import logging
from typing import Callable

from .entry_parse import parse_log_entry, is_log_head
from ..datamodel.log_file import LogEntry

logger = logging.getLogger(__name__)


# error handling?
class LogEntryStream:
    def __init__(self):
        self.entry_lines = ""
        self.callbacks = set()

    def _notify_callbacks(self, entry: LogEntry):
        for cb in self.callbacks:
            cb(entry)

    def add_line(self, line: str):
        if not line.endswith("\n"):
            line += "\n"
        if is_log_head(line) and self.entry_lines != "":
            entry = parse_log_entry(self.entry_lines)
            self.entry_lines = line
            self._notify_callbacks(entry)
        else:
            self.entry_lines += line

    def flush(self):
        try:
            entry = parse_log_entry(self.entry_lines)
            self._notify_callbacks(entry)
        except ValueError:
            logger.debug(f"parsing failed for raw text: {self.entry_lines}")

    def register_callback(self, cb: Callable[[LogEntry], None]):
        self.callbacks.add(cb)

    def unregister_callback(self, cb: Callable[[LogEntry], None]):
        self.callbacks.discard(cb)
