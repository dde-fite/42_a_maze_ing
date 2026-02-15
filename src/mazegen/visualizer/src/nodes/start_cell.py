from pathlib import Path
from ..core.nodes import BaseNode
from ..core.components import SpriteRenderer


class StartCell(BaseNode):
    def __init__(self,
                 pos: tuple[int, int],
                 scale: float = 1.0):
        super().__init__("StartCell", pos)
        self += (SpriteRenderer,
                 Path(__file__).parent.parent / "sprites" / "start.png",
                 scale)
