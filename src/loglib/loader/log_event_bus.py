import logging
from typing import Any, Optional

from ..datamodel import EventType, LogEvent


logger = logging.getLogger(__name__)


TypeMask = Optional[set[EventType]]


class LogEventBus:
    """
    Log events can be published to an event bus, being forwarded to all subscribed objects'
    handle_log_event method.
    """
    def __init__(self):
        self._subscribers: list[tuple[Any, TypeMask]] = []

    def _get_subscriber_info(self, subscriber):
        for sub, mask in self._subscribers:
            if sub == subscriber:
                return sub, mask
        return None

    def add_subscriber(self, subscriber, type_mask: TypeMask = None) -> None:
        """
        :param subscriber: the subscribing object
        :param type_mask: optional mask of log event types to subscribe to
        """
        if not hasattr(subscriber, "handle_log_event"):
            raise TypeError(
                "subscriber must have handle_log_event(self, event) method."
            )
        if self._get_subscriber_info(subscriber) is None:
            self._subscribers.append((subscriber, type_mask))

    def remove_subscriber(self, subscriber):
        """ remove the subscribing object """
        sub_info = self._get_subscriber_info(subscriber)
        if sub_info is not None:
            self._subscribers.remove(sub_info)

    def publish(self, event: LogEvent):
        """ publish a log event to all subscribers on the bus """
        for subscriber, type_mask in self._subscribers:
            if not type_mask or event.type in type_mask:
                subscriber.handle_log_event(event)
