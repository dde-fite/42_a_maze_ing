from abc import ABC, abstractmethod
from typing import Any
from ..nodes import BaseNode
from ..exceptions import EngineNoReference


class BaseComponent(ABC):
    def __init__(self) -> None:
        self.__owner: BaseNode | None = None

    @abstractmethod
    def on_init(self, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def on_update(self) -> None:
        ...

    @abstractmethod
    def on_destroy(self) -> None:
        ...

    @property
    def owner(self) -> BaseNode:
        if self.__owner is None:
            raise EngineNoReference("Component has no owner")
        return self.__owner

    def set_owner(self, owner: BaseNode) -> None:
        self.__owner = owner
