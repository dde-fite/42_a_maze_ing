from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager


class PlayButton(SpriteButton):
    def __init__(self, name: str = "PlayButton",
                 pos: tuple[int, int] = (856, 536)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "play_button.png", self.action)

    def action(self):
        EngineManager.load_scene("Maze")
