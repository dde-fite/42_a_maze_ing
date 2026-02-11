from .src import ConfigValidator, Maze


class MazeGenerator:

    @staticmethod
    def generate(config_file: str) -> Maze:
        config = ConfigValidator.read_config(config_file)
        maze = Maze(width=config[
                        ConfigValidator.AvailableKeys.WIDTH.value],
                    height=config[
                        ConfigValidator.AvailableKeys.HEIGHT.value],
                    entry=config[
                        ConfigValidator.AvailableKeys.ENTRY.value],
                    exit=config[
                        ConfigValidator.AvailableKeys.EXIT.value],
                    output_file=config[
                        ConfigValidator.AvailableKeys.OUTPUT_FILE.value],
                    ft_logo=config[
                        ConfigValidator.AvailableKeys.FT_LOGO.value],
                    perfect=config[
                        ConfigValidator.AvailableKeys.PERFECT.value],
                    seed_num=config[
                        ConfigValidator.AvailableKeys.SEED.value],
                    path_finder=config[
                        ConfigValidator.AvailableKeys.PATH_FINDER.value],
                    ft_logo_scale=config[
                        ConfigValidator.AvailableKeys.FT_LOGO_SCALE.value
                        ]
                    )
        # maze.print_output()
        return maze
