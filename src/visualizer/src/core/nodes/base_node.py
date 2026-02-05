from typing import Type, TYPE_CHECKING, Callable, TypeVar, Any
from ..engine_manager import EngineManager
from ..exceptions import EngineElementNotFound

if TYPE_CHECKING:
    from ..components import BaseComponent
    from .. import Window

TComponent = TypeVar('TComponent', bound='BaseComponent')


class BaseNode:
    def __init__(self, name: str, pos: tuple[int, int],
                 window: Window | None = None):
        self._name: str = name
        self._pos: tuple[float, float] = pos
        self._parent_node: BaseNode | None = None
        self._subnodes: list[BaseNode] = []
        self._components: list[BaseComponent] = []
        self._window: Window

        if window:
            self._window = window
        else:
            self._window = EngineManager.get_main_window()

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_pos(self) -> tuple[float, float]:
        if self._parent_node:
            parent_x, parent_y = self._parent_node.get_pos()
            return (self._pos[0] + parent_x, self._pos[1] + parent_y)
        return self._pos

    def get_rel_pos(self) -> tuple[float, float]:
        return self._pos

    def set_pos(self, x: float, y: float) -> None:
        self._pos = (x, y)

    def get_parent_node(self) -> BaseNode | None:
        return self._parent_node

    def set_parent_node(self, node: BaseNode | None) -> None:
        self._parent_node = node

    def get_subnode(self, name: str) -> BaseNode | None:
        for c in self._subnodes:
            if c.get_name() == name:
                return c
        print(f"{name} not found in: {self._name}")
        return None

    def add_subnode(self, node: BaseNode) -> None:
        self._subnodes.append(node)
        node.set_parent_node(self)

    def remove_subnode(self, name: str) -> None:
        to_remove = self.get_subnode(name)
        if to_remove:
            self._subnodes.remove(to_remove)
            to_remove.set_parent_node(None)

    def component(self, component: Type[TComponent]
                  ) -> TComponent:
        for c in self._components:
            if isinstance(c, component):
                return c
        raise EngineElementNotFound("Component does not exist")

    def get_component(self, component: Type[TComponent]
                      ) -> TComponent | None:
        for c in self._components:
            if isinstance(c, component):
                return c
        return None

    def add_component(self, component: Type[BaseComponent], *args: Any
                      ) -> None:
        instance = component()
        instance.set_owner(self)
        self._components.append(instance)
        instance.on_init(*args)

    def remove_component(self, component: Type[TComponent]) -> None:
        to_remove = self.get_component(component)
        if to_remove:
            self._components.remove(to_remove)

    def get_window(self) -> Window:
        return self._window

    def on_destroy(self) -> None:
        for c in self._components:
            c.on_destroy()
        self._components.clear()
        if self._parent_node:
            self._parent_node.remove_subnode(self._name)

    def expose_update(self) -> Callable[[], None]:
        return self.__on_update

    def __on_update(self) -> None:
        for c in self._components:
            c.on_update()
        for snode in self._subnodes:
            snode.expose_update()()
