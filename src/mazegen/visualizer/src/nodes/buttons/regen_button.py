from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager
from ...components import MazeManager


class RegenButton(SpriteButton):
    def __init__(self, name: str = "RegenButton",
                 pos: tuple[int, int] = (1654, 172)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "regen_button.png", self.action)

    def action(self):
        manager = EngineManager.get_actual_scene().node(
            "MazeRoot")[MazeManager]
        manager.regenerate()
