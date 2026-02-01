from pathlib import Path
from ctypes import c_void_p
from typing import TYPE_CHECKING
from ..mlx import MlxContext
from ..exceptions import MlxException
from .base_component import BaseComponent
from ..nodes import BaseNode
from .. import EngineManager


if TYPE_CHECKING:
    from .. import Window


class SpriteRenderer(BaseComponent):
    def __init__(self, owner: BaseNode, file_path: Path,
                 is_active: bool):
        super().__init__(owner)
        self.__file_path: Path | None = None
        self.__is_active: bool = False
        self.__ptr: c_void_p | None = None
        self.set_file_path(file_path)
        self.set_active(is_active)
        if self.__is_active and self.__ptr:
            self._owner.get_window().draw_image(
                self.__ptr, self._owner.get_pos())

    def on_update(self) -> None:
        if self.__is_active and self.__ptr:
            self._owner.get_window().draw_image(
                self.__ptr, self._owner.get_pos())

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
        self.__ptr = MlxContext.get_mlx().mlx_xpm_file_to_image(
            MlxContext.get_mlx_ptr(), str(self.__file_path))[0]
        if not self.__ptr:
            raise MlxException(f"Error creating '{self.__file_path}' image")

    def __unload_sprite(self) -> None:
        if self.__ptr:
            MlxContext.get_mlx().mlx_destroy_image(MlxContext.get_mlx_ptr,
                                                   self.__ptr)
        self.__ptr = None
