from typing import cast
from pathlib import Path
from ..core.components import BaseComponent, SpriteRenderer
from ....generator.src import Cell, Player, MazeError


class CellComponent(BaseComponent):
    def on_init(self) -> None:
        from ..nodes import CellNode
        self.__owner_cell = cast(CellNode, self.owner)
        self.__sprite_renderer = self.__owner_cell.component(SpriteRenderer)
        self.__walls_folder = Path(__file__).parent.parent / "sprites" / "walls"
        self.__cell = self.__owner_cell.cell
        self.__is_fixed: bool = False
        if self.__cell["fixed"]:
            self.__is_fixed = True
            self.__sprite_renderer.set_file_path(self.__walls_folder.joinpath("fixed.png"))
        self.__state = self.__cell["state"]

    def on_update(self) -> None:
        if self.__is_fixed:
            return
        state = self.__cell["state"]
        if self.__state != state:
            return
        if state == 0b0000:
            self.__sprite_renderer.set_file_path(None)
            return
        name: str = ""
        if state & 0b0001:
            name = "-".join([name, "up"])
        if state & 0b0010:
            name = "-".join([name, "right"])
        if state & 0b0100:
            name = "-".join([name, "down"])
        if state & 0b1000:
            name = "-".join([name, "left"])
        name = name.removeprefix("-")
        name += ".png"
        self.__sprite_renderer.set_file_path(self.__walls_folder.joinpath(name))

    def on_destroy(self) -> None:
        pass
