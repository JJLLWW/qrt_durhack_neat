import logging

from ..datamodel.log_file import LogFile
from ..datamodel.log_dir_event import LogEvent, EventType

logger = logging.getLogger(__name__)


# should also be able to add logs manually
class OpenLogManager:
    def __init__(self):
        self.logs: dict[str, LogFile] = {}

    def _handle_new_entry(self, entry, file: str):
        self.logs[file].add_entry(entry)

    def _handle_new_file(self, file: str):
        self.logs[file] = LogFile()

    def _handle_file_close(self, file: str):
        self.logs.pop(file)

    def handle_log_event(self, event: LogEvent):
        match event.type:
            case EventType.NEW_ENTRY:
                self._handle_new_entry(event.entry, event.file)
            case EventType.FILE_OPEN:
                self._handle_new_file(event.file)
            case EventType.FILE_CLOSE:
                self._handle_file_close(event.file)
