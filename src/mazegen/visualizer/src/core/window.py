from ctypes import c_void_p
import cv2
import numpy as np
from .mlx import MlxContext
from .exceptions import MlxException
from .sprite import Sprite
from .input import InputManager
from .x11 import X


class Window:
    """Represents an Mlx Window, spawning a window when instantiated and \
        closing it when not needed.

    It also provides functions for easy handling of drawing processes.

    Attributes:
        __name (str): Name of the window in the title bar.
        __size: (tuple[int, int]): Size of the window. It is not updated when \
            resized.
        __ptr: (c_void_p): Pointer to the Mlx window.

    Raises:
        MlxException: In case of an error from Mlx.
    """
    def __init__(self, name: str, size: tuple[int, int]):
        self.__name: str = name
        self.__size: tuple[int, int] = size
        self.__ptr: c_void_p = MlxContext.get_mlx().mlx_new_window(
                            MlxContext.get_mlx_ptr(), size[0], size[1],
                            name)
        self.__active: bool = True
        if not self.__ptr:
            raise MlxException(f"Error creating '{name}' window")
        MlxContext.get_mlx().mlx_hook(
            self.__ptr, X.KeyPress, X.KeyPressMask,
            InputManager.trigger_press, None)
        MlxContext.get_mlx().mlx_hook(
            self.__ptr, X.KeyRelease, X.KeyReleaseMask,
            InputManager.trigger_release, None)
        MlxContext.get_mlx().mlx_hook(
            self.__ptr, X.ButtonPress, X.ButtonPressMask,
            InputManager.trigger_button_press, None)
        MlxContext.get_mlx().mlx_hook(
            self.__ptr, X.ButtonRelease, X.ButtonReleaseMask,
            InputManager.trigger_button_release, None)
        self.__mlxbuffer = MlxContext.get_mlx().mlx_new_image(
            MlxContext.get_mlx_ptr(), self.__size[0], self.__size[1])
        if not self.__mlxbuffer:
            raise MlxException("Error creating the buffer")
        self.__mlxbuffer_data = MlxContext.get_mlx().mlx_get_data_addr(
                self.__mlxbuffer)

        self.__img_buffer: np.ndarray = np.zeros(
            (self.__size[1], self.__size[0], 4), np.uint8)
        self.__img_buffer[:, :, 3] = 255

    def on_pre_update(self) -> None:
        self.__img_buffer[:, :, :3] = 0

    def on_update(self) -> None:
        if not self.__active:
            return
        if self.__mlxbuffer_data[2] == 1:
            self.__img_buffer = cv2.cvtColor(self.__img_buffer,
                                             cv2.COLOR_BGRA2RGBA)
        self.__mlxbuffer_data[0][:] = self.__img_buffer.tobytes()
        MlxContext.get_mlx().mlx_clear_window(
                    MlxContext.get_mlx_ptr(), self.__ptr)
        MlxContext.get_mlx().mlx_put_image_to_window(
            MlxContext.get_mlx_ptr(), self.__ptr, self.__mlxbuffer, 0, 0)

    def get_name(self) -> str:
        return self.__name

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def get_ptr(self) -> c_void_p:
        return self.__ptr

    def get_mouse_pos(self) -> tuple[int, int]:
        pos = MlxContext.get_mlx().mlx_mouse_get_pos(self.__ptr)
        return (pos[1], pos[2])

    def draw_sprite(self, sprite: Sprite,
                    pos: tuple[int, int]) -> None:
        x, y = int(pos[0]), int(pos[1])
        size = sprite.size

        dx1, dy1 = max(x, 0), max(y, 0)
        dx2, dy2 = min(x + size[0], self.__size[0]), min(y + size[1],
                                                         self.__size[1])
        if dx1 >= dx2 or dy1 >= dy2:
            return

        sx1, sy1 = dx1 - x, dy1 - y
        sx2, sy2 = sx1 + (dx2-dx1), sy1 + (dy2-dy1)

        roi = self.__img_buffer[dy1:dy2, dx1:dx2, :3]
        part = sprite.image[sy1:sy2, sx1:sx2, :3]

        alpha = sprite.alpha
        if alpha is not None:
            a = alpha[sy1:sy2, sx1:sx2]
            roi[:] = (a * part + (1-a) * roi)
        else:
            roi[:] = part

    def destroy_window(self) -> None:
        self.__active = False
        MlxContext.get_mlx().mlx_destroy_image(
            MlxContext.get_mlx_ptr(), self.__mlxbuffer)
        MlxContext.get_mlx().mlx_destroy_window(
            MlxContext.get_mlx_ptr(), self.__ptr)
        del (self.__img_buffer)
