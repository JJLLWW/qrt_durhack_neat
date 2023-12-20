from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from .log_file import LogEntry


class EventType(IntEnum):
    NEW_ENTRY = 1
    FILE_OPEN = 2
    FILE_CLOSE = 3


@dataclass
class LogEvent:
    type: EventType
    file: str
    entry: Optional[LogEntry]
