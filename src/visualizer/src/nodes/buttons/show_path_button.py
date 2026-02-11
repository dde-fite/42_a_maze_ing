from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class ShowPathButton(SpriteButton):
    def __init__(self, name: str = "ShowPathButton",
                 pos: tuple[int, int] = (1577, 94)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "show_button.png", self.action)

    def action(self):
        EngineManager.load_scene("MainMenu")
