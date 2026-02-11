from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class CloseButton(SpriteButton):
    def __init__(self, name: str = "CloseButton",
                 pos: tuple[int, int] = (616, 573),):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "close_button.png", self.action)

    def action(self):
        EngineManager.exit()
