from ..core.nodes import BaseNode
from ..core.components import SpriteRenderer
from ..components import CellComponent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....generator.src import Cell


class CellNode(BaseNode):
    def __init__(self, name: str,
                 pos: tuple[int, int],
                 cell: Cell):
        super().__init__(name, pos)
        self.__cell: Cell = cell
        super().add_component(SpriteRenderer)
        super().add_component(CellComponent)

    @property
    def cell_fixed(self) -> bool:
        return self.__cell.is_fixed()

    @property
    def cell_state(self) -> int:
        return self.__cell.get_state()
