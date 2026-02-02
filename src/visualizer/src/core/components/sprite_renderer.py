from pathlib import Path
from typing import TYPE_CHECKING
from .base_component import BaseComponent
from ..nodes import BaseNode
from .. import SpriteManager, Sprite


if TYPE_CHECKING:
    from .. import Window


class SpriteRenderer(BaseComponent):
    def __init__(self, owner: BaseNode, file_path: Path,
                 is_active: bool):
        super().__init__(owner)
        self.__file_path: Path | None = None
        self.__is_active: bool = False
        self.__sprite: Sprite | None = None
        self.set_file_path(file_path)
        self.set_active(is_active)

    def on_update(self) -> None:
        if self.__is_active and self.__sprite:
            self._owner.get_window().draw_sprite(
                self.__sprite, self._owner.get_pos())

    def on_destroy(self) -> None:
        self.__unload_sprite()

    def get_file_path(self) -> Path | None:
        return self.__file_path

    def set_file_path(self, file_path: Path) -> None:
        if not file_path.is_file():
            raise FileNotFoundError(f"Can't found sprite '{file_path}'")
        self.__unload_sprite()
        self.__file_path = file_path
        self.__load_sprite()

    def get_size(self) -> tuple[int, int]:
        if self.__sprite:
            return self.__sprite.get_size()
        return (0, 0)

    def get_active(self) -> bool:
        return self.__is_active

    def set_active(self, is_active: bool) -> None:
        self.__is_active = is_active

    def get_window(self) -> Window:
        return self.__window

    def set_window(self, window: Window) -> None:
        self.__window = window

    def __load_sprite(self) -> None:
        if not self.__file_path:
            return
        self.__sprite = SpriteManager.load_sprite(self.__file_path, self)

    def __unload_sprite(self) -> None:
        if self.__file_path and self.__sprite:
            SpriteManager.unload_sprite(self.__file_path, self)
        self.__sprite = None
