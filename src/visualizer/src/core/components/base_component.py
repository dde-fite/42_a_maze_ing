from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from ..nodes import BaseNode
from ..exceptions import EngineNoReference

TNode = TypeVar('TNode', bound=BaseNode)


class BaseComponent(ABC, Generic[TNode]):
    def __init__(self) -> None:
        self.__owner: TNode | None = None

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
    def owner(self) -> TNode:
        if self.__owner is None:
            raise EngineNoReference("Component has no owner")
        return self.__owner

    def set_owner(self, owner: TNode) -> None:
        self.__owner = owner
