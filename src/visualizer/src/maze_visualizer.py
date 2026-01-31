from typing import TYPE_CHECKING, Any
from .core import EngineManager
from .core.mlx import MlxContext
from .nodes import Background

# if TYPE_CHECKING:
#     from src.generator.src.maze_class import Maze # Cell


class MazeVisualizer:
    # test
    @staticmethod
    def show_visualizer() -> None:
        MlxContext.init()
        main_window = EngineManager.create_window("a_maze_ing", (1920, 1080))
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

        mlx = MlxContext.get_mlx()
        mlx_ptr = MlxContext.get_mlx_ptr()
        mlx.mlx_loop(mlx_ptr)


MazeVisualizer.show_visualizer()
