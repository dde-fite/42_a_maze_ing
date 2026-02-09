from ..core.components import BaseComponent
from ....generator.src import MazeError
from ....maze_generator import MazeGenerator


class MazeManager(BaseComponent):
    def on_init(self) -> None:
        from ..nodes import CellNode
        print("\nGenerating a new perfect maze...")
        try:
            maze = MazeGenerator.generate("config.txt")
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
