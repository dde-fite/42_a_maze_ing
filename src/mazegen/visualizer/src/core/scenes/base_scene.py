from __future__ import annotations
from abc import ABC, abstractmethod
from ..nodes import BaseNode
from ..exceptions import EngineElementNotFound


class BaseScene(ABC):
    @abstractmethod
    def __init__(self, nodes: list[BaseNode] | None = None) -> None:
        self.__nodes: list[BaseNode]
        if nodes:
            self.__nodes = nodes
        else:
            self.__nodes = []

    def __contains__(self, name: str):
        for n in self.__nodes:
            if n.get_name() == name:
                return True
        return False

    def __getitem__(self, name: str
                    ) -> BaseNode:
        for n in self.__nodes:
            if n.get_name() == name:
                return n
        raise EngineElementNotFound("Component does not exist")

    def get_nodes(self) -> list[BaseNode]:
        return self.__nodes.copy()

    def node(self, name: str) -> BaseNode:
        for n in self.__nodes:
            if n.get_name() == name:
                return n
        raise EngineElementNotFound(f"{name} not found in: "
                                    f"{self.__class__.__mro__[0].__name__}")

    def get_node(self, name: str) -> BaseNode | None:
        for n in self.__nodes:
            if n.get_name() == name:
                return n
        print(f"{name} not found in: {self.__class__.__mro__[0].__name__}")
        return None

    def add_node(self, node: BaseNode) -> None:
        self.__nodes.append(node)

    def remove_node(self, node: BaseNode) -> None:
        node.on_destroy()
        self.__nodes.remove(node)

    def on_unload(self) -> None:
        for n in self.__nodes:
            n.on_destroy()
        self.__nodes.clear()
