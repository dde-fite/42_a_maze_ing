from typing import TypeAlias, Union

# Alias

# Maze and Cells
Coords: TypeAlias = tuple[int, int]
Cell_State: TypeAlias = dict[str, Union[int, bool]]
# Cell: TypeAlias = dict[Coords, Cell_State]
Pathway: TypeAlias = list[Coords]

# Config
Config_Value: TypeAlias = Union[int, str, tuple[Coords], bool]
