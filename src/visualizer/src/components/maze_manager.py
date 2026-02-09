from ..core.components import BaseComponent
from ....generator.src import MazeError
from ....maze_generator import MazeGenerator
from ..core.sprite import SpriteManager, Sprite
from pathlib import Path


class MazeManager(BaseComponent):
    def on_init(self) -> None:
        from ..nodes import CellNode
        print("\nGenerating a new perfect maze...")
        try:
            maze = MazeGenerator.generate("config.txt")
            sprite: Sprite = SpriteManager.load_sprite(Path(__file__).parent.parent / "sprites" / "walls" / "up-right-down-left.png")
            s_size = sprite.size
            m_size = (maze.get_width(), maze.get_height())
            total_size = (s_size[0] * m_size[0], s_size[1] * m_size[1])
            maze.print_output()
            i: int = 0
            for pos, cell in maze.get_cells().items():
                self.owner.add_subnode(CellNode(f"Cell {i}", pos, cell))
                i += 1
        except MazeError as e:
            print("ERROR:", e)

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass
