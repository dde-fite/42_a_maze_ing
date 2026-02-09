from ..core.nodes import BaseNode
from ..components import MazeManager


class MazeRoot(BaseNode):
    def __init__(self, name: str = "MazeRoot",
                 pos: tuple[int, int] = (200, 200)):
        super().__init__(name, pos)
        super().add_component(MazeManager)
