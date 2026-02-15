from pathlib import Path
from ..core.components import SpriteRenderer
from ..core.nodes import BaseNode


class ErrorMessage(BaseNode):
    def __init__(self, name: str = "ErrorMessage",
                 pos: tuple[int, int] = (593, 486)):
        super().__init__(name, pos)
        self += (SpriteRenderer,
                 Path(__file__).resolve().parent.parent / "sprites" / "error.png")
