from pathlib import Path
from ..core.components import SpriteRenderer
from ..core.nodes import BaseNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MlxWindow


class Background(BaseNode):
    def __init__(self, window: MlxWindow, name: str = "Background",
                 pos: tuple[int, int] = (0, 0)):
        super().__init__(name, pos, window)
        self.add_component(SpriteRenderer(
            pos, Path(__file__).resolve().parent.parent / "sprites" / "background.xpm", True, self._window))
