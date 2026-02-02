from typing import Any, Callable
from .x11 import keysymdef
from .events import EventManager


class InputManager:

    __pressed: set[keysymdef] = set()

    @classmethod
    def on_update(cls) -> None:
        for key in cls.__pressed:
            EventManager.trigger_event(f"on_hold_{key}")

    @classmethod
    def add_listener_on_press(cls, key: keysymdef, callback: Callable[[], Any]
                              ) -> None:
        EventManager.add_listener(f"on_press_{key}", callback)

    @classmethod
    def add_listener_on_hold(cls, key: keysymdef, callback: Callable[[], Any]
                             ) -> None:
        EventManager.add_listener(f"on_hold_{key}", callback)

    @classmethod
    def remove_listener_on_press(cls, key: keysymdef,
                                 callback: Callable[[], Any]) -> None:
        EventManager.remove_listener(f"on_press_{key}", callback)

    @classmethod
    def remove_listener_on_hold(cls, key: keysymdef,
                                callback: Callable[[], Any]) -> None:
        EventManager.remove_listener(f"on_hold_{key}", callback)

    @classmethod
    def trigger_key_press(cls, key: keysymdef, param: Any = None) -> None:
        EventManager.trigger_event(f"on_press_{key}")
        cls.__pressed.add(key)

    @classmethod
    def trigger_key_release(cls, key: keysymdef, param: Any = None) -> None:
        cls.__pressed.remove(key)
