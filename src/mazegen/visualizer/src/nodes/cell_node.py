from ..core.nodes import BaseNode
from ..core.components import SpriteRenderer
from ..components import CellComponent
from ....generator import Cell


class CellNode(BaseNode):
    def __init__(self, name: str,
                 pos: tuple[int, int],
                 cell: Cell,
                 scale: float = 1.0):
        super().__init__(name, pos)
        self.__cell: Cell = cell
        self += (SpriteRenderer, None, scale)
        self += (CellComponent)

    @property
    def cell(self) -> Cell:
        return self.__cell
