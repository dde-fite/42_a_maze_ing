from ctypes import c_void_p
from .mlx import MlxContext
from .exceptions import MlxException
from .sprite import Sprite


class Window:
    def __init__(self, name: str, size: tuple[int, int]):
        self.__name = name
        self.__size: tuple[int, int] = size
        self.__ptr: c_void_p = MlxContext.get_mlx().mlx_new_window(
                            MlxContext.get_mlx_ptr(), size[0], size[1],
                            name)
        if not self.__ptr:
            raise MlxException(f"Error creating '{name}' window")

    def get_name(self) -> str:
        return self.__name

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def get_ptr(self) -> c_void_p:
        return self.__ptr

    def draw_image(self, img_ptr: c_void_p, pos: tuple[int, int]) -> None:
        MlxContext.get_mlx().mlx_put_image_to_window(
            MlxContext.get_mlx_ptr(), self.__ptr, img_ptr,
            int(pos[0]), int(pos[1]))

    def draw_sprite(self, sprite: Sprite, pos: tuple[int, int]) -> None:
        MlxContext.get_mlx().mlx_put_image_to_window(
            MlxContext.get_mlx_ptr(), self.__ptr, sprite.get_ptr(),
            int(pos[0]), int(pos[1]))

    def clear_window(self) -> None:
        MlxContext.get_mlx().mlx_clear_window(MlxContext.get_mlx_ptr(),
                                              self.__ptr)

    def destroy_window(self) -> None:
        MlxContext.get_mlx().mlx_destroy_window(
            MlxContext.get_mlx_ptr, self.__ptr)
