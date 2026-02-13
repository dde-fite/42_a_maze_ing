from pathlib import Path
from ..core.nodes import BaseNode
from ..core.components import SpriteRenderer


class ExitCell(BaseNode):
    def __init__(self,
                 pos: tuple[int, int],
                 scale: float = 1.0):
        super().__init__("ExitCell", pos)
        self += (SpriteRenderer,
                 Path(__file__).parent.parent / "sprites" / "exit.png",
                 scale)
