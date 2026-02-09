from ..core.components import BaseComponent, Input
from ..core import EngineManager
from ..core.x11 import keysymdef
# from time import time
# from random import uniform


class PlayerMovement(BaseComponent):
    def on_init(self) -> None:
        input_comp: Input = self.owner.component(Input)

        input_comp.on_hold(keysymdef.XK_w, self.move_up)
        input_comp.on_hold(keysymdef.XK_s, self.move_down)
        input_comp.on_hold(keysymdef.XK_a, self.move_left)
        input_comp.on_hold(keysymdef.XK_d, self.move_right)

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def move_up(self) -> None:
        actual_x, actual_y = self.owner.get_pos()
        self.owner.set_pos(
            actual_x, actual_y - (800 * EngineManager.get_delta_time()))

    def move_down(self) -> None:
        actual_x, actual_y = self.owner.get_pos()
        self.owner.set_pos(
            actual_x, actual_y + (800 * EngineManager.get_delta_time()))

    def move_left(self) -> None:
        actual_x, actual_y = self.owner.get_pos()
        self.owner.set_pos(
            actual_x - (800 * EngineManager.get_delta_time()), actual_y)

    def move_right(self) -> None:
        actual_x, actual_y = self.owner.get_pos()
        self.owner.set_pos(actual_x + (800 * EngineManager.get_delta_time()),
                           actual_y)
