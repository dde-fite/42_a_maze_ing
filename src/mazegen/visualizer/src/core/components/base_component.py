from abc import ABC, abstractmethod
from typing import Any
from ..nodes import BaseNode
from ..exceptions import EngineNoReference


class BaseComponent(ABC):
    def __init__(self) -> None:
        self.__owner: BaseNode | None = None
        self._active: bool = True

    @abstractmethod
    def on_init(self, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def on_update(self) -> None:
        ...

    @abstractmethod
    def on_destroy(self) -> None:
        ...

    def on_deactivate(self) -> None:
        pass

    def on_activate(self) -> None:
        pass

    @property
    def owner(self) -> BaseNode:
        if self.__owner is None:
            raise EngineNoReference("Component has no owner")
        return self.__owner

    def set_owner(self, owner: BaseNode) -> None:
        self.__owner = owner

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        self._active = active
        if active:
            self.on_activate()
        else:
            self.on_deactivate()
