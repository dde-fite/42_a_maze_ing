from time import time
from ..core.components import BaseComponent, SpriteRenderer


class WinMessController(BaseComponent):
    def on_init(self) -> None:
        self.__sprite_ren = self.owner[SpriteRenderer]
        self.__next_time: float = time() + 0.6

    def on_update(self) -> None:
        if time() >= self.__next_time:
            if self.__sprite_ren.active:
                self.__sprite_ren.active = False
            else:
                self.__sprite_ren.active = True
            self.__next_time = time() + 0.6

    def on_destroy(self) -> None:
        pass
