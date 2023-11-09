from datetime import datetime


class LogEntry:
    def __init__(self, timestamp: datetime, status: str, message: str):
        self.timestamp = timestamp
        self.status = status
        self.message = message

    def __str__(self):
        return "[" + str(self.timestamp) + ", " + self.status + ", " + self.message + "]"

    def as_dict(self):
        return {
            'Timestamp': self.timestamp,
            'Status': self.status,
            'Message': self.message
        }
