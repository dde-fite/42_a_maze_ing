from pathlib import Path
from ..core.components import SpriteRenderer
from ..core.nodes import BaseNode


class Background(BaseNode):
    def __init__(self, name: str = "Background",
                 pos: tuple[int, int] = (0, 0)):
        super().__init__(name, pos)
        self.add_component(SpriteRenderer(
            pos, Path(__file__).resolve().parent.parent / "sprites" / "background.xpm", True))
