from typing import Any, Callable


class EventManager:
    __listeners: dict[str, set[Callable[[], Any]]] = {}

    @classmethod
    def get_events(cls) -> set[str]:
        events: set[str] = set()
        for e in cls.__listeners.keys():
            events.add(e)
        return events

    @classmethod
    def get_listeners(cls, event: str) -> set[Callable[[], Any]]:
        event_lis = cls.__listeners.get(event)
        if event_lis:
            return event_lis.copy()
        return set()

    @classmethod
    def add_listener(cls, event: str, callback: Callable[[], Any]) -> None:
        event_lis = cls.__listeners.get(event)
        if event_lis:
            event_lis.add(callback)
        else:
            cls.__listeners[event] = {callback}

    @classmethod
    def remove_listener(cls, event: str, callback: Callable[[], Any]) -> None:
        event_lis = cls.__listeners.get(event)
        if event_lis:
            event_lis.remove(callback)

    @classmethod
    def trigger_event(cls, event: str) -> None:
        event_lis = cls.__listeners.get(event)
        if not event_lis:
            return
        for listener in event_lis:
            listener()
