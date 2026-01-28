#!/bin/env python3

from enum import Enum
from typing import Union
import sys
from maze_class import Maze


class ConfigError(Exception):
    pass


class AvailableKeys(Enum):
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"
    # Some extra keys could be added here

    @classmethod
    def convert_input(cls, key: str, value: str) -> (
            tuple[str, Union[int, str, tuple[int, int], bool]]):
        if key not in cls.__members__:
            raise ValueError(f"Given key '{key}' is not available!")
        if ' ' in value:
            raise ConfigError("NO SPACES")
        value = value.rstrip("\n")  # We substract the '\n'
        match key:
            case cls.WIDTH.value:
                try:
                    result = int(value)
                except ValueError:
                    raise ConfigError(f"Given value '{value}' doesn't work "
                                      f"for {cls.WIDTH}!")
            case cls.HEIGHT.value:
                try:
                    result = int(value)
                except ValueError:
                    raise ConfigError(f"Given value '{value}' doesn't work "
                                      f"for {cls.HEIGHT}!")
            case cls.ENTRY.value:
                try:
                    split = value.split(",")
                    if len(split) != 2:
                        raise ValueError(f"Given value '{value}' doesn't work "
                                         f"for {cls.ENTRY}")
                    try:
                        x = int(split[0])
                        y = int(split[1])
                        result = (x, y)
                    except ValueError:
                        raise ConfigError(f"Given value '{value}' doesn't "
                                          f"work for {cls.ENTRY}")
                except Exception as e:
                    raise ConfigError(e)
            case cls.EXIT.value:
                try:
                    split = value.split(",")
                    if len(split) != 2:
                        raise ValueError(f"Given value '{value}' doesn't work "
                                         f"for {cls.EXIT}")
                    try:
                        x = int(split[0])
                        y = int(split[1])
                        result = (x, y)
                    except ValueError:
                        raise ConfigError(f"Given value '{value}' doesn't "
                                          f"work for {cls.EXIT}")
                except Exception as e:
                    raise ConfigError(e)
            case cls.OUTPUT_FILE.value:
                if not value.endswith(".txt") or value.count(".") != 1:
                    raise ConfigError(f"Given value '{value}' doesn't "
                                      f"work for {cls.OUTPUT_FILE}")
                result = value
            case cls.PERFECT.value:
                if value != "True" and value != "False":
                    raise ConfigError(f"Given value '{value}' doesn't "
                                      f"work for {cls.OUTPUT_FILE}")
                if value == "True":
                    result = True
                elif value == "False":
                    result = False
                else:
                    # This should never happen
                    raise ConfigError(f"Given value '{value}' doesn't "
                                      f"work for {cls.OUTPUT_FILE}")
        return (key, result)


if __name__ == "__main__":
    config_file = "config.txt"
    available_keys = {}
    for key in AvailableKeys:
        available_keys[key.value] = 0
    try:
        with open(config_file, "r") as f:
            config_file_line = f.readline()
            while (config_file_line):
                print("Read line:", config_file_line)
                if config_file_line.startswith("#"):
                    config_file_line = f.readline()
                    continue
                if '=' not in config_file_line:
                    raise ValueError("Incorrect config 1!")
                split = config_file_line.split("=")
                if len(split) != 2 or split[1] == '\n':
                    raise ValueError("Incorrect config 2!")
                result = AvailableKeys.convert_input(split[0], split[1])
                available_keys[result[0]] = result[1]
                # print(available_keys)
                config_file_line = f.readline()
    except FileNotFoundError:
        print("File was not found")
        sys.exit(1)
    print("\nAvailable keys:")
    print(available_keys)
    maze = Maze(available_keys[AvailableKeys.WIDTH.value],
                available_keys[AvailableKeys.HEIGHT.value],
                available_keys[AvailableKeys.ENTRY.value],
                available_keys[AvailableKeys.EXIT.value])
    maze.random_generation()
    maze.print_output()
