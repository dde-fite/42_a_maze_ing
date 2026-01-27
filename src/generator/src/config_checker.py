#!/bin/env python3

from enum import Enum
from typing import Union


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
        if key not in cls:
            raise ValueError(f"Given key '{key}' is not available!")
        match key:
            case cls.WIDTH.value:
                try:
                    result = int(value.rstrip('\n'))
                except Exception:
                    raise ValueError(f"Given value '{value}' doesn't work for "
                                     f"{cls.WIDTH}!")
            case cls.HEIGHT.value:
                try:
                    result = int(value.rstrip('\n'))
                except Exception:
                    raise ValueError(f"Given value '{value}' doesn't work for "
                                     f"{cls.HEIGHT}!")
            case cls.ENTRY.value:
                pass
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
                print(config_file_line)
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
    print("\nAvailable keys:")
    print(available_keys)
