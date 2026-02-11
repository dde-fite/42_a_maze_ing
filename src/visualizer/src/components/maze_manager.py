from ..core.components import BaseComponent
from ....generator.src import MazeError
from ....maze_generator import MazeGenerator
from ..core.sprite import SpriteManager, Sprite
from pathlib import Path

X0_WORKING_POS = 150
X1_WORKING_POS = 1770
Y0_WORKING_POS = 200
Y1_WORKING_POS = 972


class MazeManager(BaseComponent):
    def on_init(self) -> None:
        from ..nodes import CellNode
        print("\nGenerating a new perfect maze...")
        try:
            maze = MazeGenerator.generate("config.txt")
            maze.print_output()
            sprite: Sprite = SpriteManager.load_sprite(Path(__file__).parent.parent / "sprites" / "walls" / "up-right-down-left.png", self)
            cells = (maze.get_width(), maze.get_height())
            sprite_size, scale = self.calculate_size(sprite.size, cells)
            self.center_root(sprite_size, cells)
            for pos, cell in maze.get_cells().items():
                self.owner.add_subnode(CellNode(
                    "Cell",
                    ((pos[0] - 1) * sprite_size[0],
                     (pos[1] - 1) * sprite_size[1]),
                    cell,
                    scale))
        except MazeError as e:
            print("ERROR:", e)

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

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
