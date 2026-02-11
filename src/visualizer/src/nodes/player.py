from pathlib import Path
from ..core.components import SpriteRenderer, Input
from ..core.nodes import BaseNode
from ..components import PlayerMovement


class Player(BaseNode):
    def __init__(self, name: str = "Player",
                 pos: tuple[int, int] = (960, 540)):
        super().__init__(name, pos)
        self += (SpriteRenderer,
                 Path(__file__).resolve().parent.parent / "sprites" / "player.png")
        self += Input
        self += PlayerMovement
