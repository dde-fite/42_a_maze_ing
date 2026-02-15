from typing import Callable, Any, TYPE_CHECKING
from .base_component import BaseComponent
from ..input import InputManager
from ..x11 import keysymdef


class Input(BaseComponent):
    def on_init(self) -> None:
        self.__press_listeners: list[tuple[keysymdef, Callable[[], Any]]] = []
        self.__hold_listeners: list[tuple[keysymdef, Callable[[], Any]]] = []
        self.__release_listeners: list[tuple[keysymdef,
                                             Callable[[], Any]]] = []

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        self.__unload_listeners()
        self.__press_listeners.clear()
        self.__hold_listeners.clear()
        self.__release_listeners.clear()

    def on_activate(self) -> None:
        self.__load_listeners()

    def on_deactivate(self) -> None:
        self.__unload_listeners()

    def on_press(self, key: keysymdef, callback: Callable[[], Any]) -> None:
        InputManager.add_listener_on_press(key, callback)
        self.__press_listeners.append((key, callback))

    def on_hold(self, key: keysymdef, callback: Callable[[], Any]) -> None:
        InputManager.add_listener_on_hold(key, callback)
        self.__hold_listeners.append((key, callback))

    def on_release(self, key: keysymdef, callback: Callable[[], Any]) -> None:
        InputManager.add_listener_on_release(key, callback)
        self.__release_listeners.append((key, callback))

    def remove_listener_on_press(self, key: keysymdef,
                                 callback: Callable[[], Any]) -> None:
        InputManager.remove_listener_on_press(key, callback)
        self.__press_listeners.remove((key, callback))

    def remove_listener_on_hold(self, key: keysymdef,
                                callback: Callable[[], Any]) -> None:
        InputManager.remove_listener_on_hold(key, callback)
        self.__hold_listeners.remove((key, callback))

    def remove_listener_on_release(self, key: keysymdef,
                                   callback: Callable[[], Any]) -> None:
        InputManager.remove_listener_on_release(key, callback)
        self.__release_listeners.remove((key, callback))

    def __unload_listeners(self):
        for listener in self.__hold_listeners:
            InputManager.remove_listener_on_hold(*listener)
        for listener in self.__press_listeners:
            InputManager.remove_listener_on_press(*listener)
        for listener in self.__release_listeners:
            InputManager.remove_listener_on_release(*listener)

    def __load_listeners(self):
        for listener in self.__hold_listeners:
            InputManager.add_listener_on_hold(*listener)
        for listener in self.__press_listeners:
            InputManager.add_listener_on_press(*listener)
        for listener in self.__release_listeners:
            InputManager.add_listener_on_release(*listener)
