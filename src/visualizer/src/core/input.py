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
    def add_listener_on_release(cls, key: keysymdef,
                                callback: Callable[[], Any]) -> None:
        EventManager.add_listener(f"on_release_{key}", callback)

    @classmethod
    def remove_listener_on_press(cls, key: keysymdef,
                                 callback: Callable[[], Any]) -> None:
        EventManager.remove_listener(f"on_press_{key}", callback)

    @classmethod
    def remove_listener_on_hold(cls, key: keysymdef,
                                callback: Callable[[], Any]) -> None:
        EventManager.remove_listener(f"on_hold_{key}", callback)

    @classmethod
    def remove_listener_on_release(cls, key: keysymdef,
                                   callback: Callable[[], Any]) -> None:
        EventManager.remove_listener(f"on_release_{key}", callback)

    @classmethod
    def trigger_press(cls, key: keysymdef, *args: Any) -> None:
        EventManager.trigger_event(f"on_press_{key}")
        cls.__pressed.add(key)

    @classmethod
    def trigger_release(cls, key: keysymdef, *args: list[Any]) -> None:
        EventManager.trigger_event(f"on_release_{key}")
        cls.__pressed.discard(key)

    @classmethod
    def trigger_button_press(cls, button: int, *args: Any) -> None:
        cls.trigger_press(button + keysymdef.XK_Pointer_Button1 - 1)

    @classmethod
    def trigger_button_release(cls, button: int, *args: Any) -> None:
        cls.trigger_release(button + keysymdef.XK_Pointer_Button1 - 1)
