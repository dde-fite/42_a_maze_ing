from .maze_generator import MazeGenerator
from .visualizer import MazeVisualizer


if __name__ == "__main__":
    maze = MazeGenerator.generate("config.txt")
    maze.print_output()
    MazeVisualizer.show_visualizer()
