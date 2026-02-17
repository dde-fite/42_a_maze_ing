from .src import ConfigValidator, Maze, Coords
from typing import cast


class MazeGenerator:

    @staticmethod
    def generate(config_file: str) -> Maze:
        # Stablishing values for the maze.
        config = ConfigValidator.read_config(config_file)

        width: int = cast(int,
                          config[ConfigValidator.AvailableKeys.WIDTH.value])
        height: int = cast(int,
                           config[ConfigValidator.AvailableKeys.HEIGHT.value])
        entry: Coords = (
            cast(Coords, config[ConfigValidator.AvailableKeys.ENTRY.value]))
        exit: Coords = (
            cast(Coords, config[ConfigValidator.AvailableKeys.EXIT.value]))
        output_file: str = cast(
            str, config[ConfigValidator.AvailableKeys.OUTPUT_FILE.value])
        ft_logo: bool = (
            cast(bool, config[ConfigValidator.AvailableKeys.FT_LOGO.value]))
        perfect: bool = (
            cast(bool, config[ConfigValidator.AvailableKeys.PERFECT.value]))
        seed_num: int = (
            cast(int, config[ConfigValidator.AvailableKeys.SEED.value]))
        path_finder: bool = (
            cast(bool,
                 config[ConfigValidator.AvailableKeys.PATH_FINDER.value]))
        scale: bool = (
            cast(bool,
                 config[ConfigValidator.AvailableKeys.FT_LOGO_SCALE.value]))

        maze = Maze(width=width,
                    height=height,
                    entry=entry,
                    exit=exit,
                    output_file=output_file,
                    ft_logo=ft_logo,
                    perfect=perfect,
                    seed_num=seed_num,
                    path_finder=path_finder,
                    ft_logo_scale=scale
                    )
        # maze.print_output()
        return maze
