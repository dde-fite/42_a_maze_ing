from ..core.scenes import BaseScene
from ..nodes import BgMaze, Player, MazeRoot
from ..nodes.buttons import (BackButton, ShowPathButton, ColorButton,
                             RegenButton)


class Maze(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            BgMaze(),
            Player(),
            MazeRoot(),
            BackButton(),
            ShowPathButton(),
            ColorButton(),
            RegenButton(),
        ])
