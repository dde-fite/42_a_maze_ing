from pathlib import Path
from ..core.components import SpriteRenderer
from ..core.nodes import BaseNode
from ..components.win_mess_controller import WinMessController


class WinMessage(BaseNode):
    def __init__(self, name: str = "WinMessage",
                 pos: tuple[int, int] = (10, 10)):
        super().__init__(name, pos)
        self += (SpriteRenderer,
                 Path(__file__).resolve().parent.
                 parent / "sprites" / "win.png")
        self += WinMessController
