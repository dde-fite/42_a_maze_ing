from pathlib import Path
from ..core.components import SpriteRenderer
from ..core.nodes import BaseNode


class BgMaze(BaseNode):
    def __init__(self, name: str = "Background",
                 pos: tuple[int, int] = (0, 0)):
        super().__init__(name, pos)
        super().add_component(
            SpriteRenderer,
            Path(__file__).resolve().parent.parent / "sprites" / "bg_maze.xpm")
