from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class CloseButton(SpriteButton):
    def __init__(self, name: str = "PlayButton",
                 pos: tuple[int, int] = (873, 650),):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "close_button.xpm", self.action)

    def action(self):
        EngineManager.exit()
