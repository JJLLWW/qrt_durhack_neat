from collections import namedtuple

# this shouldn't be its own file
LogEntry = namedtuple(typename="LogEntry", field_names=["timestamp", "status", "message"])