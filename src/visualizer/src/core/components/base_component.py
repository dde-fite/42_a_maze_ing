from abc import ABC, abstractmethod
from ..nodes import BaseNode


class BaseComponent(ABC):
    def __init__(self, owner: BaseNode) -> None:
        self._owner: BaseNode = owner

    @abstractmethod
    def on_update(self) -> None:
        ...

    @abstractmethod
    def on_destroy(self) -> None:
        ...
