from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class ColorButton(SpriteButton):
    def __init__(self, name: str = "BackButton",
                 pos: tuple[int, int] = (1677, 72),):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "color_button.png", self.action)

    def action(self):
        EngineManager.load_scene("MainMenu")
