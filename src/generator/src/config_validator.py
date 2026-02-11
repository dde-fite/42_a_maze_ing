#!/bin/env python3

from enum import Enum
import sys
from .maze import Maze
from .exceptions import ConfigError
from .gen_types import Config_Value


class ConfigValidator:

    class AvailableKeys(Enum):
        WIDTH = "WIDTH"
        HEIGHT = "HEIGHT"
        ENTRY = "ENTRY"
        EXIT = "EXIT"
        OUTPUT_FILE = "OUTPUT_FILE"
        PERFECT = "PERFECT"
        SEED = "SEED"
        # Some extra keys could be added here
        FT_LOGO = "FT_LOGO"
        FT_LOGO_SCALE = "FT_LOGO_SCALE"
        PATH_FINDER = "PATH_FINDER"

        DEFAULT_VALUES = {WIDTH: 0, HEIGHT: 0,
                          ENTRY: (0, 0), EXIT: (0, 0),
                          OUTPUT_FILE: None,
                          PERFECT: None, SEED: None,
                          FT_LOGO: True, PATH_FINDER: False,
                          FT_LOGO_SCALE: False}

    @classmethod
    def __parse_width(cls, value: str) -> int:
        try:
            width = int(value)
        except ValueError:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.AvailableKeys.WIDTH.value}. Only single "
                              "integers are accepted!")
        return width

    @classmethod
    def __parse_height(cls, value: str) -> int:
        try:
            height = int(value)
        except ValueError:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.AvailableKeys.HEIGHT.value}. Only single "
                              "integers are accepted!")
        return height

    @classmethod
    def __parse_entry(cls, value: str) -> tuple[int, int]:
        try:
            split = value.split(",")
            if len(split) != 2:
                raise ValueError(f"Given value '{value}' doesn't work "
                                 f"for {cls.AvailableKeys.ENTRY.value}. "
                                 "There can "
                                 "be only one ',' in the value!")
            try:
                x = int(split[0])
                y = int(split[1])
            except ValueError:
                raise ConfigError(f"Given value '{value}' doesn't "
                                  f"work for {cls.AvailableKeys.ENTRY.value}. "
                                  "Only integers are accepted as possible "
                                  "values for the coordinates!")
        except Exception as e:
            raise ConfigError(e)
        return (x, y)

    @classmethod
    def __parse_exit(cls, value: str) -> tuple[int, int]:
        try:
            split = value.split(",")
            if len(split) != 2:
                raise ValueError(f"Given value '{value}' doesn't work "
                                 f"for {cls.AvailableKeys.EXIT.value}. "
                                 "There can "
                                 "be only one ',' in the value!")
            try:
                x = int(split[0])
                y = int(split[1])
            except ValueError:
                raise ConfigError(f"Given value '{value}' doesn't "
                                  f"work for {cls.AvailableKeys.EXIT.value}. "
                                  "Only integers are accepted as possible "
                                  "values for the coordinates!")
        except Exception as e:
            raise ConfigError(e)
        return (x, y)

    @classmethod
    def __parse_output_file(cls, value: str) -> str:
        # 'file_name.a', 'file_name', ... case
        if not value.endswith(".txt"):
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. "
                              "The output file must be a .txt!")
        # 'file name.txt' case
        if ' ' in value:
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. "
                              "No spaces are allowed in the name!")
        # 'file..name....txt', 'file.....name.txt', ... case
        if ".." in value:
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. No"
                              " consecutive dots are allowed for a file name!")
        # '.txt' case
        if len(value) == 4:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. "
                              "Only extension file type was given!")
        return value

    @classmethod
    def __parse_perfect(cls, value: str) -> bool:
        if value != "True" and value != "False":
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. "
                              "Only 'True' or 'False' are accepted values!")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            # This should never happen
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.OUTPUT_FILE.value}. "
                              "Only 'True' or 'False' are accepted values!")

    @classmethod
    def __parse_seed(cls, value: str) -> int:
        try:
            seed = int(value)
        except ValueError:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.AvailableKeys.SEED.value}. Only single "
                              "integers are accepted!")
        return seed

    @classmethod
    def __parse_ft_logo(cls, value: str) -> bool:
        if value != "True" and value != "False":
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.FT_LOGO.value}. "
                              "Only 'True' or 'False' are accepted values!")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            # This should never happen
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.AvailableKeys.FT_LOGO.value}. "
                              "Only 'True' or 'False' are accepted values!")

    @classmethod
    def __parse_path_finder(cls, value: str) -> bool:
        if value != "True" and value != "False":
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.PATH_FINDER.value}. "
                              "Only 'True' or 'False' are accepted values!")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            # This should never happen
            raise ConfigError(f"Given value '{value}' doesn't "
                              "work for "
                              f"{cls.AvailableKeys.PATH_FINDER.value}. "
                              "Only 'True' or 'False' are accepted values!")

    @classmethod
    def __parse_ft_logo_scale(cls, value: str) -> bool:
        if value != "True" and value != "False":
            raise ConfigError(f"Given value '{value}' doesn't work for "
                              f"{cls.AvailableKeys.FT_LOGO_SCALE.value}. "
                              "Only 'True' or 'False' are accepted values!")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            # This should never happen
            raise ConfigError(f"Given value '{value}' doesn't "
                              "work for "
                              f"{cls.AvailableKeys.FT_LOGO_SCALE.value}. "
                              "Only 'True' or 'False' are accepted values!")

    @classmethod
    def __parse_config(cls, key: str, value: str) -> (
            tuple[str, Config_Value]):
        if key not in cls.AvailableKeys.__members__:
            raise ValueError(f"Given key '{key}' is not available!")
        if ' ' in value:
            raise ConfigError("Spaces are not allowed in the line!")
        value = value.rstrip("\n")  # We substract the '\n'
        match key:
            case cls.AvailableKeys.WIDTH.value:
                result = cls.__parse_width(value)
            case cls.AvailableKeys.HEIGHT.value:
                result = cls.__parse_height(value)
            case cls.AvailableKeys.ENTRY.value:
                result = cls.__parse_entry(value)
            case cls.AvailableKeys.EXIT.value:
                result = cls.__parse_exit(value)
            case cls.AvailableKeys.OUTPUT_FILE.value:
                result = cls.__parse_output_file(value)
            case cls.AvailableKeys.PERFECT.value:
                result = cls.__parse_perfect(value)
            case cls.AvailableKeys.SEED.value:
                result = cls.__parse_seed(value)
            case cls.AvailableKeys.FT_LOGO.value:
                result = cls.__parse_ft_logo(value)
            case cls.AvailableKeys.PATH_FINDER.value:
                result = cls.__parse_path_finder(value)
            case cls.AvailableKeys.FT_LOGO_SCALE.value:
                result = cls.__parse_ft_logo_scale(value)
        return (key, result)

    @classmethod
    def read_config(cls, config_file: str = "config.txt"
                    ) -> dict[str, Config_Value]:
        available_keys = {}
        for key in cls.AvailableKeys:
            if key is cls.AvailableKeys.DEFAULT_VALUES:
                break
            available_keys[key.value] = (
                cls.AvailableKeys.DEFAULT_VALUES.value[key.value])
        try:
            with open(config_file, "r") as f:
                config_file_line = f.readline()
                while (config_file_line):
                    # print("Read line:", config_file_line)
                    if config_file_line.strip(' ').startswith("#"):
                        # Comment line case
                        config_file_line = f.readline()
                        continue
                    if config_file_line.strip(' ') == "\n":
                        # Empty line case
                        config_file_line = f.readline()
                        continue
                    if '=' not in config_file_line:
                        # Not key=value line case
                        raise ConfigError("Lines must follow 'key=value' "
                                          "structure!")
                    split = config_file_line.split("=")
                    if len(split) != 2 or split[1] == '\n':
                        # Not just key=value line or key='\n' line
                        raise ConfigError("Lines must follow 'key=value' "
                                          "structure!")
                    result = cls.__parse_config(split[0], split[1])
                    available_keys[result[0]] = result[1]
                    config_file_line = f.readline()
        except FileNotFoundError:
            print("File was not found")
            sys.exit(1)
        return available_keys


def main():
    config_file = "config.txt"
    config = ConfigValidator.read_config(config_file)
    print("\nAvailable keys:")
    print(config)
    maze = Maze(width=config[ConfigValidator.AvailableKeys.WIDTH.value],
                height=config[ConfigValidator.AvailableKeys.HEIGHT.value],
                entry=config[ConfigValidator.AvailableKeys.ENTRY.value],
                exit=config[ConfigValidator.AvailableKeys.EXIT.value],
                output_file=config[
                    ConfigValidator.AvailableKeys.OUTPUT_FILE.value],
                ft_logo=config[ConfigValidator.AvailableKeys.FT_LOGO.value],
                perfect=config[ConfigValidator.AvailableKeys.PERFECT.value],
                seed_num=config[ConfigValidator.AvailableKeys.SEED.value],
                path_finder=config[
                    ConfigValidator.AvailableKeys.PATH_FINDER.value],
                ft_logo_scale=config[
                    ConfigValidator.AvailableKeys.FT_LOGO_SCALE.value]
                )
    # Generate the maze with the read config
    maze.print_output()


if __name__ == "__main__":
    # import cProfile
    # cProfile.run("main()")
    main()
