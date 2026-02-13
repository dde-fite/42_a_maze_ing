from pathlib import Path
from ..core.components import SpriteRenderer, Input
from ..core.nodes import BaseNode
from ..components.player_movement import PlayerMovement
from ....generator.src import Maze


class Player(BaseNode):
    def __init__(self, maze: Maze,
                 cell_size: tuple[int, int],
                 scale: float):
        super().__init__("Player", (0, 0))
        self += (SpriteRenderer,
                 None,
                 scale)
        self += Input
        self += (PlayerMovement, maze, cell_size)
