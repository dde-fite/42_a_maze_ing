from .mlx import MlxContext
from .exceptions import MlxException


class Window:
    def __init__(self, name: str, size: tuple[int, int]):
        self.__name = name
        self.__size: tuple[int, int] = size
        self.__ptr: int = MlxContext.get_mlx().mlx_new_window(
                            MlxContext.get_mlx_ptr(), size[0], size[1],
                            name)
        if not self.__ptr:
            raise MlxException(f"Error creating '{name}' window")

    def get_name(self) -> str:
        return self.__name

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def get_ptr(self) -> int:
        return self.__ptr

    def clear_window(self) -> None:
        MlxContext.get_mlx().mlx_clear_window(MlxContext.get_mlx_ptr(),
                                              self.__ptr)

    def destroy_window(self) -> None:
        MlxContext.get_mlx().mlx_destroy_window(
            MlxContext.get_mlx_ptr, self.__ptr)
