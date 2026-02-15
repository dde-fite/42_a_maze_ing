from .generator import MazeGenerator  # noqa: F401
from .visualizer import MazeVisualizer  # noqa: F401
import sys


def check_environment() -> None:
    if sys.prefix == sys.base_prefix:
        print("You are not using the virtual environment.")
        print("It is recommended to do so.")
        print("Activate it doing the following command:")
        print("source .venv/bin/activate")
        print("\n(Fish and csh is also supported)")
        exit(1)


def main() -> None:
    check_environment()

    if len(sys.argv) < 2:
        print("Not enough arguments were given! "
              "Config file is required."
              "\nUsage: a_maze_ing <config file>: python3 a_maze_ing.py "
              "config.txt")
        return
    elif len(sys.argv) > 2:
        print("Too many arguments were given! "
              "Only config file is required."
              "\nUsage: a_maze_ing <config file>: python3 a_maze_ing.py "
              "config.txt")
        return
    MazeVisualizer.show_visualizer()


if __name__ == "__main__":
    main()
