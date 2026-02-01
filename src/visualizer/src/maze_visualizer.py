from .core import EngineManager
from .core.mlx import MlxContext
from .nodes import Background
from .scenes import MainMaze


class MazeVisualizer:
    # test
    @staticmethod
    def show_visualizer() -> None:
        EngineManager.init("a_maze_ing",
                           (1920, 1080),
                           [MainMaze])
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

        mlx = MlxContext.get_mlx()
        mlx_ptr = MlxContext.get_mlx_ptr()
        mlx.mlx_loop(mlx_ptr)

# from typing import TYPE_CHECKING, Any
# from .core import EngineManager, Window
# from .core.mlx import MlxContext
# from .nodes import Background
# from mlx import Mlx
# from pathlib import Path

# # if TYPE_CHECKING:
# #     from src.generator.src.maze_class import Maze # Cell


# class MazeVisualizer:
#     # test
#     @staticmethod
#     def show_visualizer() -> None:
#         MlxContext.init()
#         # m = Mlx()
#         # mlx_ptr = m.mlx_init()
#         main_window = MlxContext.get_mlx().mlx_new_window(MlxContext.get_mlx_ptr(), 1920, 1080, "a_maze_ing")
#         # main_window.clear_window()
#         # print(MlxContext.get_mlx_ptr())
#         # print(main_window.get_ptr())
#         # background = Background(main_window)
#         img_src = Path("src/visualizer/src/sprites/background.xpm")
#         print(str(img_src.absolute()))
#         img = MlxContext.get_mlx().mlx_xpm_file_to_image(MlxContext.get_mlx_ptr(), str(img_src.absolute()))
#         print(img)
#         MlxContext.get_mlx().mlx_put_image_to_window(MlxContext.get_mlx_ptr(), main_window, img[0], 1, 1)
#         # m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
#         # (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
#         # print(f"Got screen size: {w} x {h} .")

#         # stuff = [1, 2]
#         # m.mlx_mouse_hook(win_ptr, mymouse, None)
#         # m.mlx_key_hook(win_ptr, mykey, stuff)

#         # mlx = MlxContext.get_mlx()
#         # mlx_ptr = MlxContext.get_mlx_ptr()
#         MlxContext.get_mlx().mlx_loop(MlxContext.get_mlx_ptr())
