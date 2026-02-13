from ..core.scenes import BaseScene
from ..nodes import BgMaze, MazeRoot
from ..nodes.buttons import (BackButton, ShowPathButton, ColorButton,
                             RegenButton, StartButton)


class Maze(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            BgMaze(),
            MazeRoot(),
            BackButton(),
            ShowPathButton(),
            ColorButton(),
            RegenButton(),
            StartButton()
        ])
