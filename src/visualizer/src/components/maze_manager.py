from ..core.components import BaseComponent
from ....generator.src import MazeError
from ....generator import MazeGenerator
from ..core.sprite import SpriteManager, Sprite
from ..core.engine_manager import EngineManager
from pathlib import Path
import sys

X0_WORKING_POS = 150
X1_WORKING_POS = 1770
Y0_WORKING_POS = 200
Y1_WORKING_POS = 972


class MazeManager(BaseComponent):
    def on_init(self) -> None:
        self.__maze_generated: bool = False
        from ..nodes import CellNode
        try:
            self.__maze = MazeGenerator.generate(sys.argv[1])
        except MazeError:
            return
        self.__maze.print_output()
        closed_wall = Path(__file__).parent.parent / "sprites" / "walls" / "up-right-down-left.png"
        sprite: Sprite = SpriteManager.load_sprite(closed_wall, self)
        cells = (self.__maze.get_width(), self.__maze.get_height())
        self.__sprite_size, self.__scale = self.calculate_size(sprite.size, cells)
        SpriteManager.unload_sprite(closed_wall, self)
        self.center_root(self.__sprite_size, cells)
        self.spawn_entry_exit()
        for pos, cell in self.__maze.get_cells().items():
            self.owner.add_subnode(CellNode(
                f"Cell {pos}",
                ((pos[0] - 1) * self.__sprite_size[0],
                 (pos[1] - 1) * self.__sprite_size[1]),
                cell,
                self.__scale))
        self.__maze_generated: bool = True
        self.spawn_player()

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def regenerate(self) -> None:
        from ..nodes.buttons.show_path_button import ShowPathButton
        button = EngineManager.get_actual_scene()["ShowPathButton"]
        if isinstance(button, ShowPathButton):
            button.reset()
        for children in self.owner.subnodes:
            self.owner.remove_subnode(children)
            children.on_destroy()
        self.on_init()

    def center_root(self, sprite_size: tuple[int, int],
                    cells: tuple[int, int]) -> None:
        window_x, window_y = self.owner.get_window().get_size()
        x1 = cells[0] * sprite_size[0]
        y1 = cells[1] * sprite_size[1]
        root_x = (window_x - x1) / 2
        root_y = (window_y - y1) / 2
        self.owner.set_pos(root_x, root_y)

    def calculate_size(self, sprite_size: tuple[int, int],
                       cells: tuple[int, int]
                       ) -> tuple[tuple[int, int], float]:
        x_expected_size = ((X1_WORKING_POS - X0_WORKING_POS) * sprite_size[0])\
                / (cells[0] * sprite_size[0])
        y_expected_size = ((Y1_WORKING_POS - Y0_WORKING_POS) * sprite_size[1])\
            / (cells[1] * sprite_size[1])
        scale = min(x_expected_size / sprite_size[0], y_expected_size
                    / sprite_size[1])
        new_sprite_size = (int(sprite_size[0] * scale),
                           int(sprite_size[1] * scale))
        return (new_sprite_size, scale)

    def spawn_entry_exit(self) -> None:
        from ..nodes.exit_cell import ExitCell
        from ..nodes.start_cell import StartCell
        start_pos = self.__maze.get_entry()
        exit_pos = self.__maze.get_exit()
        self.owner.add_subnode(ExitCell(
                                ((exit_pos[0] - 1) * self.__sprite_size[0],
                                 (exit_pos[1] - 1) * self.__sprite_size[1]),
                                self.__scale))
        self.owner.add_subnode(StartCell(
                                ((start_pos[0] - 1) * self.__sprite_size[0],
                                 (start_pos[1] - 1) * self.__sprite_size[1]),
                                self.__scale))

    def spawn_player(self) -> None:
        from ..nodes.player import Player
        if not self.owner.get_subnode("Player"):
            self.owner.add_subnode(Player(self.__maze, self.__sprite_size, self.__scale))

    def spawn_footprints(self) -> None:
        from ..nodes.footprint_root import FootprintRoot
        if self.__maze_generated and self.owner.get_subnode("FootprintRoot"):
            return
        self.owner.add_subnode(FootprintRoot(self.__sprite_size, self.__scale,
                                             self.__maze.get_pathway()))

    def destroy_footprints(self) -> None:
        footprints = self.owner.get_subnode("FootprintRoot")
        if footprints:
            self.owner.remove_subnode(footprints)
