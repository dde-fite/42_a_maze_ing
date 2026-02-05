from ..core.scenes import BaseScene
from ..nodes import BgMaze, Player


class Maze(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            BgMaze(),
            Player()
        ])
