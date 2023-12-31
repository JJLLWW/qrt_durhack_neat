from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

import pandas as pd


@dataclass
class SourceInfo:
    name: str
    uuid: UUID


@dataclass
class LogEntry:
    timestamp: datetime
    status: str
    message: str
    stats: Optional[pd.DataFrame]
    info: Optional[SourceInfo]
