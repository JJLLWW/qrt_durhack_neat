from datetime import datetime


class LogEntry:
    def __init__(self, timestamp: datetime, status: str, message: str):
        self.timestamp = timestamp
        self.status = status
        self.message = message

    def __str__(self):
        return "[" + str(self.timestamp) + ", " + self.status + ", " + self.message + "]"

    def __repr__(self):
        return f"LogEntry({self.timestamp}, {self.status}, {self.message})"

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def as_dict(self):
        return {
            'Timestamp': self.timestamp,
            'Status': self.status,
            'Message': self.message
        }
