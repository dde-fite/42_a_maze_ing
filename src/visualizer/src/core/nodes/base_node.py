from ..engine_manager import EngineManager
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .components import BaseComponent


class BaseNode:
    def __init__(self, name: str, pos: tuple[int, int],
                 window: Window | None = None):
        self._name: str = name
        self._pos: tuple[int, int] = pos
        self._components: list[Type[BaseComponent]] = []
        self._window: Window
        if not window:
            self._window = EngineManager.get_main_window()
        else:
            self._window = window

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_pos(self) -> tuple[int, int]:
        return self.__pos

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.__pos = pos
        for c in self._components:
            c.set_pos(pos)

    def get_component(self, component: Type[BaseComponent]
                      ) -> Type[BaseComponent] | None:
        for c in self._components:
            if isinstance(c, component):
                return c
        return None

    def add_component(self, component: Type[BaseComponent]) -> None:
        self._components.append(component)
