import logging
from typing import Optional, Any

from ..datamodel.log_event import LogEvent, EventType

logger = logging.getLogger(__name__)


TypeMask = Optional[set[EventType]]


class LogEventBus:
    def __init__(self):
        # can't use a set/dict as not all objects are hashable
        self._subscribers: list[tuple[Any, TypeMask]] = []

    def _get_subscriber_info(self, subscriber):
        for sub, mask in self._subscribers:
            if sub == subscriber:
                return sub, mask
        return None

    def add_subscriber(self, subscriber, type_mask: TypeMask = None):
        if not hasattr(subscriber, "handle_log_event"):
            raise TypeError("subscriber must have handle_log_event(self, event) method.")
        if self._get_subscriber_info(subscriber) is None:
            self._subscribers.append((subscriber, type_mask))

    def remove_subscriber(self, subscriber):
        sub_info = self._get_subscriber_info(subscriber)
        if sub_info is not None:
            self._subscribers.remove(sub_info)

    def publish(self, event: LogEvent):
        for subscriber, type_mask in self._subscribers:
            if not type_mask or event.type in type_mask:
                subscriber.handle_log_event(event)