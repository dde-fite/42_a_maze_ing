from pathlib import Path
from ...core.nodes import SpriteButton
from ...core import EngineManager
from ...components import MazeManager
from ...core.components.sprite_renderer import SpriteRenderer


class ShowPathButton(SpriteButton):
    def __init__(self, name: str = "ShowPathButton",
                 pos: tuple[int, int] = (1577, 94)):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "show_button.png", self.action)
        self.__active: bool = False

    def reset(self):
        self.__active = False
        self[SpriteRenderer].set_file_path(Path(__file__).parent.parent.parent / "sprites" / "buttons" / "show_button.png")

    def action(self):
        if not self.__active:
            self.__active = True
            self[SpriteRenderer].set_file_path(Path(__file__).parent.parent.parent / "sprites" / "buttons" / "hide_button.png")
            manager = EngineManager.get_actual_scene().node(
                "MazeRoot")[MazeManager]
            manager.spawn_footprints()
        else:
            self.__active = False
            self[SpriteRenderer].set_file_path(Path(__file__).parent.parent.parent / "sprites" / "buttons" / "show_button.png")
            manager = EngineManager.get_actual_scene().node(
                "MazeRoot")[MazeManager]
            manager.destroy_footprints()
