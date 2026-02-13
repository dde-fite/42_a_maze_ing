from __future__ import annotations
from typing import Type, TYPE_CHECKING, Any, TypeVar, Iterator, overload
from ..exceptions import EngineElementNotFound

if TYPE_CHECKING:
    from ..components import BaseComponent
    from .. import Window

TComponent = TypeVar('TComponent', bound='BaseComponent')


class BaseNode:
    def __init__(self, name: str, pos: tuple[int, int],
                 window: Window | None = None):
        from ..engine_manager import EngineManager

        self._name: str = name
        self._pos: tuple[float, float] = pos
        self._active: bool = True
        self._parent_node: BaseNode | None = None
        self._subnodes: list[BaseNode] = []
        self._components: list[BaseComponent] = []
        self._window: Window
        self.__destroy: bool = False

        if window:
            self._window = window
        else:
            self._window = EngineManager.get_main_window()

    # -------------------- update and destroy --------------------

    def on_update(self) -> None:
        if not self._active:
            return
        if not self.__destroy:
            for c in self._components:
                c.on_update()
            for snode in self._subnodes:
                snode.on_update()

    def on_destroy(self) -> None:
        self.__destroy = True
        for c in self._components:
            c.on_destroy()
        self._components.clear()
        if self._parent_node:
            self._parent_node.remove_subnode(self._name)

    # -------------------- properties --------------------

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

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        self.active = active

    def get_window(self) -> Window:
        return self._window

    # -------------------- subnodes --------------------

    @property
    def parent_node(self) -> BaseNode | None:
        return self._parent_node

    @parent_node.setter
    def parent_node(self, node: BaseNode | None) -> None:
        self._parent_node = node

    def __iter__(self) -> Iterator[BaseNode]:
        return iter(self._subnodes)

    @property
    def subnodes(self) -> list[BaseNode]:
        return self._subnodes.copy()

    def subnode(self, name: str) -> BaseNode:
        for c in self._subnodes:
            if c.get_name() == name:
                return c
        raise EngineElementNotFound(f"{name} not found in: {self._name}")

    def get_subnode(self, name: str) -> BaseNode | None:
        for c in self._subnodes:
            if c.get_name() == name:
                return c
        return None

    def add_subnode(self, node: BaseNode) -> None:
        self._subnodes.append(node)
        node.parent_node = self

    def remove_subnode(self, node: BaseNode) -> None:
        if node in self._subnodes:
            self._subnodes.remove(node)
            node.on_destroy()

    # -------------------- components --------------------

    def __contains__(self, component: Type[TComponent]):
        for c in self._components:
            if isinstance(c, component):
                return True
        return False

    def __getitem__(self, component: Type[TComponent]
                    ) -> TComponent:
        for c in self._components:
            if isinstance(c, component):
                return c
        raise EngineElementNotFound("Component does not exist")

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

    @overload
    def __add__(self, component: Type[TComponent]) -> TComponent: ...

    @overload
    def __add__(
        self, component: tuple[Type[TComponent], *tuple[Any, ...]]
    ) -> TComponent: ...

    def __add__(
        self,
        component: Type[TComponent] | tuple[Type[TComponent], *tuple[Any, ...]]
    ) -> TComponent:
        if isinstance(component, type):
            component_cls = component
            args = ()
        else:
            component_cls = component[0]
            args = component[1:]
        instance = component_cls()
        instance.set_owner(self)
        self._components.append(instance)
        instance.on_init(*args)
        return instance

    def __iadd__(
        self,
        component: Type[TComponent] | tuple[Type[TComponent], *tuple[Any, ...]]
    ) -> BaseNode:
        self.__add__(component)
        return self

    def add_component(self, component: Type[TComponent], *args: Any
                      ) -> TComponent:
        instance = component()
        instance.set_owner(self)
        self._components.append(instance)
        instance.on_init(*args)
        return instance

    def remove_component(self, component: Type[TComponent]) -> None:
        to_remove = self.get_component(component)
        if to_remove:
            self._components.remove(to_remove)
