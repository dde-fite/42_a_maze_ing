from ..core.nodes import BaseNode
from ..components.footprints_spawner import FootprintsSpawner


class FootprintRoot(BaseNode):
    def __init__(self, sprite_size: tuple[int, int],
                 scale: float, pathway: list[tuple[int, int]]):
        super().__init__("FootprintRoot", (0, 0))
        self += (FootprintsSpawner, sprite_size, scale, pathway)
