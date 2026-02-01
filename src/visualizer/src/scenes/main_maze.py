from ..core.scenes import BaseScene
from ..nodes import Background


class MainMaze(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            Background(),
        ])
