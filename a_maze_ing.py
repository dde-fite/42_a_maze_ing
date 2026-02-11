from src import MazeVisualizer, MazeGenerator  # noqa: F401
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
        raise Exception("Not enough arguments were given! "
                        "Config file is required.")
    elif len(sys.argv) > 2:
        raise Exception("Too many arguments were given! "
                        "Only config file is required.")
    # config_file = sys.argv[1]
    # maze = MazeGenerator.generate(config_file)
    MazeVisualizer.show_visualizer()


if __name__ == "__main__":
    main()
