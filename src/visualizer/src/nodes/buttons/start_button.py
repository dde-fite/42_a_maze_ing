from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager
from ...components import MazeManager
from ...core.components.sprite_renderer import SpriteRenderer


class StartButton(SpriteButton):
    def __init__(self, name: str = "StartButton",
                 pos: tuple[int, int] = (1339, 72)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "start_button.png", self.action)
        self.__active: bool = True

    def reset(self):
        self.__active = True
        self[SpriteRenderer].set_file_path(Path(__file__).parent.parent.parent / "sprites" / "buttons" / "start_button.png")

    def action(self):
        if not self.__active:
            return
        self.__active = False
        self[SpriteRenderer].set_file_path(None)
        manager = EngineManager.get_actual_scene().node(
            "MazeRoot")[MazeManager]
        manager.spawn_player()
