from typing import TypeAlias, Union

# Alias

# Maze and Cells
Coords: TypeAlias = tuple[int, int]
Cell: TypeAlias = dict[str, Union[int, bool]]
Pathway: TypeAlias = list[Coords]

# Config
Config_Value: TypeAlias = Union[int, str, tuple[Coords], bool]
