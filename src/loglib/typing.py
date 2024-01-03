from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ExchangeStats(BaseModel):
    exchange: str
    order: str
    recv_nu: int
    X: int


class SourceInfo(BaseModel):
    name: str
    uuid: UUID


class LogEntryData(BaseModel):
    timestamp: datetime
    status: str
    message: str
    stats: list[ExchangeStats] = []


class LogEntry(BaseModel):
    data: LogEntryData
    info: Optional[SourceInfo] = None


class LogFile(BaseModel):
    info: SourceInfo
    entries: list[LogEntryData] = []

    def add_entry(self, entry: LogEntry):
        self.entries.append(entry.data)