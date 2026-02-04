from .core import EngineManager
from .scenes import MainMenu, Maze


class MazeVisualizer:
    @staticmethod
    def show_visualizer() -> None:
        EngineManager.init("a_maze_ing",
                           (1920, 1080),
                           [MainMenu, Maze])
