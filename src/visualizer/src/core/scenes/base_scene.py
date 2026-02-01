from abc import ABC, abstractmethod
from ..nodes import BaseNode


class BaseScene(ABC):
    @abstractmethod
    def __init__(self, nodes: list[BaseNode] | None = None) -> None:
        self.__nodes: list[BaseNode]
        if nodes:
            self.__nodes = nodes
        else:
            self.__nodes = []

    def get_nodes(self) -> list[BaseNode]:
        return self.__nodes

    def get_node(self, name: str) -> BaseNode | None:
        for n in self.__nodes:
            if n.get_name() == name:
                return n
        print(f"{name} not found in: {self.__name}")
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
