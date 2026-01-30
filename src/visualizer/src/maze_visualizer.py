from mlx import Mlx
from typing import TYPE_CHECKING, Any
from .exceptions import MlxException, MlxNotFound
from .nodes import Background

# if TYPE_CHECKING:
#     from src.generator.src.maze_class import Maze # Cell


class MlxManager:
    __mlx: Mlx
    __mlx_ptr: int
    __windows: list[MlxWindow] = []

    @classmethod
    def init_mlx(cls) -> None:
        cls.__mlx = Mlx()
        cls.__mlx_ptr = cls.__mlx.mlx_init()

    @classmethod
    def get_mlx(cls) -> Mlx:
        if not cls.__mlx:
            raise MlxNotFound("Mlx is not initiated")
        else:
            return cls.__mlx

    @classmethod
    def get_mlx_ptr(cls) -> int | None:
        if not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        else:
            return cls.__mlx_ptr

    @classmethod
    def close_mlx(cls) -> None:
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        else:
            cls.__mlx.mlx_release(cls.__mlx_ptr)

    @classmethod
    def create_window(cls, name: str, size: tuple[int, int]) -> MlxWindow:
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        elif cls.get_window(name):
            raise MlxException(f"'{name}' window already exist")
        else:
            window = cls.MlxWindow(name, size)
            cls.__windows.append(window)
        return window

    @classmethod
    def get_window(cls, name: str) -> MlxWindow | None:
        for window in cls.__windows:
            if window.get_name() == name:
                return window
        return None

    @classmethod
    def destroy_window(cls, name: str) -> None:
        window = cls.get_window(name)
        if not cls.__mlx or not cls.__mlx_ptr:
            raise MlxNotFound("Mlx is not initiated")
        elif not window:
            raise MlxException(f"Can not destroy '{name}' because is no "
                               "instanciated")
        else:
            window.destroy_window()

    class MlxWindow:
        def __init__(self, name: str, size: tuple[int, int]):
            self.__name = name
            self.__size: tuple[int, int] = size
            self.__ptr: int = MlxManager.get_mlx().mlx_new_window(
                                MlxManager.get_mlx_ptr(), size[0], size[1],
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
            MlxManager.get_mlx().mlx_clear_window(MlxManager.get_mlx_ptr(),
                                                  self.__ptr)

        def destroy_window(self) -> None:
            MlxManager.get_mlx().mlx_destroy_window(
                MlxManager.get_mlx_ptr, self.__ptr)


class MazeVisualizer:
    # test
    @staticmethod
    def show_visualizer() -> None:
        MlxManager.init_mlx()
        mlx = MlxManager.get_mlx()
        mlx_ptr = MlxManager.get_mlx_ptr()
        try:
            main_window = MlxManager.create_window("a_maze_ing", (1920, 1080))
        except MlxException:
            exit(1)
        main_window.clear_window()
        background = Background(main_window)
        # img = m.mlx_xpm_file_to_image(mlx_ptr, "sprites/background.xpm")
        # print(img)
        # print(m.mlx_mouse_get_pos(win_ptr))
        # m.mlx_put_image_to_window(mlx_ptr, win_ptr, img[0], 1, 1)
        # m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
        # (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
        # print(f"Got screen size: {w} x {h} .")

        # stuff = [1, 2]
        # m.mlx_mouse_hook(win_ptr, mymouse, None)
        # m.mlx_key_hook(win_ptr, mykey, stuff)

        mlx.mlx_loop(mlx_ptr)


MazeVisualizer.show_visualizer()