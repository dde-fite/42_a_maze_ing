from typing import Callable, Any
from ..base_component import BaseComponent
from .. import Input, SpriteRenderer
from ...x11 import keysymdef

# PENDING!!


class Button(BaseComponent):

    def on_init(self, callback: Callable[[], Any] | None):
        self.__callback: Callable[[], Any] | None = callback
        self.owner.component(Input).on_release(
            keysymdef.XK_Pointer_Button1, self.on_click)

    def on_update(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_click(self) -> None:
        if self.__callback:
            mouse = self.owner.get_window().get_mouse_pos()
            pos = self.owner.get_pos()
            size = self.owner.component(SpriteRenderer).get_size()
            if (pos[0] < mouse[0] < pos[0] + size[0] and
                    pos[1] < mouse[1] < pos[1] + size[1]):
                self.__callback()

    def set_callback(self, callback: Callable[[], Any] | None):
        self.__callback = callback
