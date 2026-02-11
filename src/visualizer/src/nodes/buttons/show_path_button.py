from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager
from ...components import MazeManager


class ShowPathButton(SpriteButton):
    def __init__(self, name: str = "ShowPathButton",
                 pos: tuple[int, int] = (1577, 94)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "show_button.png", self.action)

    def action(self):
        manager = EngineManager.get_actual_scene().node(
            "MazeRoot")[MazeManager]
        manager.spawn_footprints()
