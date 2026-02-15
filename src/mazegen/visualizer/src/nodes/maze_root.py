from ..core.nodes import BaseNode
from ..components import MazeManager


class MazeRoot(BaseNode):
    def __init__(self, name: str = "MazeRoot",
                 pos: tuple[int, int] = (200, 200)):
        super().__init__(name, pos)
        self.__alt: str | None = None
        self += MazeManager

    @property
    def alt(self) -> str | None:
        return self.__alt

    @alt.setter
    def alt(self, alt: str | None) -> None:
        self.__alt = alt
