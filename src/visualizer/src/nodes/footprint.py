from ..core.nodes import BaseNode
from ..core.components import SpriteRenderer


class Footprint(BaseNode):
    def __init__(self, name: str,
                 pos: tuple[int, int],
                 scale: float = 1.0):
        super().__init__(name, pos)
        super().add_component(SpriteRenderer, None, scale)
