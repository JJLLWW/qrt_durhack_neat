import dataclasses
import datetime
import json
import uuid

import pandas as pd

from .typing import LogEntry, SourceInfo


class LogEntryEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, pd.DataFrame):
            return o.to_json()
        return super().default(o)


def encode(obj) -> str:
    encoder = LogEntryEncoder()
    return encoder.encode(obj)


# TODO: is there a better way to avoid writing this boilerplate?
def decode_log_entry(as_json: str) -> LogEntry:
    decoded = json.loads(as_json)
    tstamp = datetime.datetime.fromisoformat(decoded['timestamp'])
    status = decoded['status']
    msg = decoded['message']
    stats = None
    if decoded['stats'] is not None:
        stats_dict = json.loads(decoded['stats'])
        stats = pd.DataFrame.from_dict(stats_dict)  # TODO: DTYPES CORRECT?
    info = SourceInfo(name=decoded['info']['name'], uuid=uuid.UUID(decoded['info']['uuid']))
    return LogEntry(timestamp=tstamp, status=status, message=msg, stats=stats, info=info)