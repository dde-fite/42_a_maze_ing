from pathlib import Path
from ..core.components import BaseComponent, Input, SpriteRenderer
from ..core import EngineManager
from ..core.x11 import keysymdef
from ....generator.src import Maze, Coords, NORTH, WEST, EAST, SOUTH
# from time import time
# from random import uniform


class PlayerMovement(BaseComponent):
    def on_init(self, maze: Maze, cell_size: tuple[int, int]) -> None:
        self.__speed: int = 10
        self.__maze: Maze = maze
        self.__cell_size: tuple[int, int] = cell_size
        self.__cell: Coords = maze.get_entry()
        self.__sprites: dict[str, Path] = {
            "neutral": Path(__file__).resolve().parent.parent / "sprites" / "player" / "neutral.png",
            "up": Path(__file__).resolve().parent.parent / "sprites" / "player" / "up.png",
            "down": Path(__file__).resolve().parent.parent / "sprites" / "player" / "down.png",
            "left": Path(__file__).resolve().parent.parent / "sprites" / "player" / "left.png",
            "right": Path(__file__).resolve().parent.parent / "sprites" / "player" / "right.png"
        }
        self.owner[SpriteRenderer].set_file_path(self.__sprites["neutral"])
        input_comp: Input = self.owner[Input]

        input_comp.on_press(keysymdef.XK_w, self.move_up)
        input_comp.on_press(keysymdef.XK_s, self.move_down)
        input_comp.on_press(keysymdef.XK_a, self.move_left)
        input_comp.on_press(keysymdef.XK_d, self.move_right)
        input_comp.on_press(keysymdef.XK_Up, self.move_up)
        input_comp.on_press(keysymdef.XK_Down, self.move_down)
        input_comp.on_press(keysymdef.XK_Left, self.move_left)
        input_comp.on_press(keysymdef.XK_Right, self.move_right)

    def on_update(self) -> None:
        pos = self.owner.get_rel_pos()
        target_pos = ((self.__cell[0] - 1) * self.__cell_size[0],
                      (self.__cell[1] - 1) * self.__cell_size[1])
        dt = EngineManager.delta_time()
        self.owner.set_pos(
            pos[0] + (target_pos[0] - pos[0]) * dt * self.__speed,
            pos[1] + (target_pos[1] - pos[1]) * dt * self.__speed)

    def on_destroy(self) -> None:
        pass

    def move_up(self) -> None:
        if self.__maze.check_if_can_go(self.__cell, NORTH):
            self.owner[SpriteRenderer].set_file_path(self.__sprites["up"])
            self.__cell = (self.__cell[0], self.__cell[1] - 1)
        else:
            self.owner[SpriteRenderer].set_file_path(self.__sprites["neutral"])

    def move_down(self) -> None:
        if self.__maze.check_if_can_go(self.__cell, SOUTH):
            self.owner[SpriteRenderer].set_file_path(self.__sprites["down"])
            self.__cell = (self.__cell[0], self.__cell[1] + 1)
        else:
            self.owner[SpriteRenderer].set_file_path(self.__sprites["neutral"])

    def move_left(self) -> None:
        if self.__maze.check_if_can_go(self.__cell, WEST):
            self.owner[SpriteRenderer].set_file_path(self.__sprites["left"])
            self.__cell = (self.__cell[0] - 1, self.__cell[1])
        else:
            self.owner[SpriteRenderer].set_file_path(self.__sprites["neutral"])

    def move_right(self) -> None:
        if self.__maze.check_if_can_go(self.__cell, EAST):
            self.owner[SpriteRenderer].set_file_path(self.__sprites["right"])
            self.__cell = (self.__cell[0] + 1, self.__cell[1])
        else:
            self.owner[SpriteRenderer].set_file_path(self.__sprites["neutral"])
