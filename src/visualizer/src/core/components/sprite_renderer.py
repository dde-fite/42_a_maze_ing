from pathlib import Path
from .base_component import BaseComponent
from ..sprite import SpriteManager, Sprite


class SpriteRenderer(BaseComponent):
    def on_init(self, file_path: Path | None = None):
        self.__file_path: Path | None = None
        self.__sprite: Sprite | None = None
        self.set_file_path(file_path)

    def on_update(self) -> None:
        if self.__sprite and self.owner:
            self.owner.get_window().draw_sprite(
                self.__sprite, self.owner.get_pos())

    def on_destroy(self) -> None:
        self.__unload_sprite()

    def get_file_path(self) -> Path | None:
        return self.__file_path

    def set_file_path(self, file_path: Path | None) -> None:
        if file_path == self.__file_path:
            return
        if file_path is None:
            self.__unload_sprite()
            return
        if not file_path.is_file():
            raise FileNotFoundError(f"Can't found sprite '{file_path}'")
        self.__unload_sprite()
        self.__file_path = file_path
        self.__load_sprite()

    @property
    def size(self) -> tuple[int, int]:
        if self.__sprite:
            return self.__sprite.size
        return (0, 0)

    def __load_sprite(self) -> None:
        if not self.__file_path:
            return
        self.__sprite = SpriteManager.load_sprite(self.__file_path, self)

    def __unload_sprite(self) -> None:
        if self.__file_path and self.__sprite:
            SpriteManager.unload_sprite(self.__file_path, self)
        self.__sprite = None
