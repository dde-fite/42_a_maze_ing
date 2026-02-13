from ..nodes.footprint import Footprint
from time import time
from ..core.components import BaseComponent

TIME_TO_FILL = 3


class FootprintsSpawner(BaseComponent):
    def on_init(self, sprite_size: tuple[int, int],
                scale: float, pathway: list[tuple[int, int]]) -> None:
        self.__sprite_size: tuple[int, int] = sprite_size
        self.__scale: float = scale
        self.__pathway: list[tuple[int, int]] = list(reversed(pathway))
        self.__next_spawn = time()
        self.__cooldown: float = TIME_TO_FILL / len(self.__pathway)

    def on_update(self) -> None:
        while len(self.__pathway) > 1 and time() >= self.__next_spawn:
            self.__next_spawn = self.__next_spawn + self.__cooldown
            pos = self.__pathway.pop()
            pos = (self.__sprite_size[0] * (pos[0] - 1),
                   self.__sprite_size[1] * (pos[1] - 1))
            footprint = Footprint("Footprint",
                                  pos,
                                  self.__scale)
            self.owner.add_subnode(footprint)

    def on_destroy(self) -> None:
        pass
