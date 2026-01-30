from abc import ABC, abstractmethod


class BaseComponent(ABC):
    def __init__(self, pos: tuple[int, int]) -> None:
        self._pos = pos

    @abstractmethod
    def set_pos(self, pos: tuple[int, int]) -> None:
        ...
