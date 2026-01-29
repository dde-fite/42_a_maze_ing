#!/bin/env python3

from enum import Enum
from typing import Union
import sys
from .maze import Maze


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
    def __convert_width(cls, value: str) -> int:
        try:
            width = int(value)
        except ValueError:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.WIDTH.value}. Only single "
                              "integers are accepted!")
        return width

    @classmethod
    def __convert_height(cls, value: str) -> int:
        try:
            height = int(value)
        except ValueError:
            raise ConfigError(f"Given value '{value}' doesn't work for"
                              f"{cls.HEIGHT.value}. Only single "
                              "integers are accepted!")
        return height

    @classmethod
    def __convert_entry(cls, value: str) -> tuple[int, int]:
        try:
            split = value.split(",")
            if len(split) != 2:
                raise ValueError(f"Given value '{value}' doesn't work "
                                 f"for {cls.ENTRY.value}. There can be only "
                                 "one ',' in the value!")
            try:
                x = int(split[0])
                y = int(split[1])
            except ValueError:
                raise ConfigError(f"Given value '{value}' doesn't "
                                  f"work for {cls.ENTRY.value}. Only integers "
                                  "are accepted as possible values for "
                                  "the coordinates!")
        except Exception as e:
            raise ConfigError(e)
        return (x, y)

    @classmethod
    def __convert_exit(cls, value: str) -> tuple[int, int]:
        try:
            split = value.split(",")
            if len(split) != 2:
                raise ValueError(f"Given value '{value}' doesn't work "
                                 f"for {cls.EXIT.value}. There can be only "
                                 "one ',' in the value!")
            try:
                x = int(split[0])
                y = int(split[1])
            except ValueError:
                raise ConfigError(f"Given value '{value}' doesn't "
                                  f"work for {cls.EXIT.value}. Only integers "
                                  "are accepted as possible values for "
                                  "the coordinates!")
        except Exception as e:
            raise ConfigError(e)
        return (x, y)

    @classmethod
    def __convert_output_file(cls, value: str) -> str:
        # 'file_name.a', 'file_name', ... case
        if not value.endswith(".txt"):
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE.value}. The output "
                              "file must be a .txt!")
        # 'file name.txt' case
        if ' ' in value:
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE.value}. No spaces "
                              "are allowed in the name!")
        # 'file..name....txt', 'file.....name.txt', ... case
        if ".." in value:
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE.value}. No "
                              "consecutive dots are allowed for a file name!")
        # '.txt' case
        if len(value) == 4:
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE.value}. Only "
                              "extension file type was given!")
        return value

    @classmethod
    def __convert_perfect(cls, value: str) -> bool:
        if value != "True" and value != "False":
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE}. Only 'True' or "
                              "'False' are accepted values!")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            # This should never happen
            raise ConfigError(f"Given value '{value}' doesn't "
                              f"work for {cls.OUTPUT_FILE}. Only 'True' or "
                              "'False' are accepted values!")

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
                result = cls.__convert_width(value)
            case cls.HEIGHT.value:
                result = cls.__convert_height(value)
            case cls.ENTRY.value:
                result = cls.__convert_entry(value)
            case cls.EXIT.value:
                result = cls.__convert_exit(value)
            case cls.OUTPUT_FILE.value:
                result = cls.__convert_output_file(value)
            case cls.PERFECT.value:
                result = cls.__convert_perfect(value)
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
