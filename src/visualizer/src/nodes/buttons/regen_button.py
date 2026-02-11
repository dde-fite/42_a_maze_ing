from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class RegenButton(SpriteButton):
    def __init__(self, name: str = "RegenButton",
                 pos: tuple[int, int] = (1654, 172)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "regen_button.png", self.action)

    def action(self):
        EngineManager.load_scene("MainMenu")
