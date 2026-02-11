#!/bin/env python3

from .exceptions import MazeError
from .player import Player

from .gen_types import Coords, Cell, Pathway
from .predefined import NORTH, SOUTH, EAST, WEST

# Other imports...
from math import ceil
from random import choice, random, seed
from typing import Optional
import sys


class Maze:

    WALLS = {NORTH: 0b0001, EAST: 0b0010,
             SOUTH: 0b0100, WEST: 0b1000}

    MIN_FT_WIDTH = 9
    MIN_FT_HEIGHT = 7

    WALL_OPENING_CHANCE = 1 / 100
    PATH_ATTEMPTS = 10

    def __init__(self, width: int, height: int,
                 entry: Coords, exit: Coords,
                 output_file: str = "maze.txt",
                 ft_logo: bool = True, perfect: bool = False,
                 path_finder: bool = False,
                 seed_num: int = 0
                 ) -> None:
        from .pathfinder import PathFinder

        # First checking
        if not width:
            raise MazeError("No width provided!")
        if not height:
            raise MazeError("No height provided!")
        if not entry:
            raise MazeError("No entry provided!")
        if not exit:
            raise MazeError("No exit provided!")
        if not output_file:
            raise MazeError("No output file provided!")
        if ft_logo is None:
            ft_logo = True
        if perfect is None:
            perfect = False
        if path_finder is None:
            path_finder = False
        if seed_num is None:
            seed_num = 0

        # Seed that will be used
        if seed_num:
            seed(seed_num)

        # Bases init
        self.__base_fields_init(width, height, ft_logo, entry, exit)
        self._output_file = output_file
        self._pathway: Pathway
        self._directions_followed: list[str]
        # cell_generation: dict[Coords, Cell_State]

        # Extras init
        self._perfect = perfect
        self._player = Player(self._cells[entry])
        self._possible_pathways: list[Pathway] = []

        # Generating cells with the algorithm in the Generator class
        # if seed_num:
        #     seed(seed_num)
        # cell_generation, self._pathway, self._directions_followed = (
        #     Generator.dfs_generation(self))

        # If not perfect:
        if not self._perfect:

            # Open walls
            self._cells = self.open_random_walls()

            # Finding paths:
            # Recursive
            if path_finder:
                print("Looking for paths...")
                self._possible_pathways: list[Pathway] = (
                    PathFinder.path_finder_dfs(self))

            else:
                print("No pathfinder added!")

        print("Maze successfully generated!")

    # BASE INITIATION ---------------------------------------------------------
    def __base_fields_init(self, width: int, height: int, ft_logo: bool,
                           entry: Coords, exit: Coords):
        """
        Initiates all the class fields that are essential for any maze to work.
        """
        from .generator import Generator

        self.set_width(width)
        self.set_height(height)
        self.set_entry(entry)
        self.set_exit(exit)
        self._ft_logo = ft_logo
        self._cells, self._pathway, self._directions_followed = (
            Generator.dfs_generation(self))

    # WIDTH -------------------------------------------------------------------
    def set_width(self, width: int) -> None:
        if width < 1:
            raise MazeError("WIDTH value can't be lower than 1!")
        self._width = width

    def get_width(self) -> int:
        return self._width

    # HEIGHT ------------------------------------------------------------------
    def set_height(self, height: int) -> None:
        if height < 1:
            raise MazeError("HEIGHT value can't be lower than 1!")
        self._height = height

    def get_height(self) -> int:
        return self._height

    # ENTRY -------------------------------------------------------------------
    def set_entry(self, entry: Coords) -> None:
        if entry[0] < 1 or entry[0] > self._width:
            raise MazeError("ENTRY point is not inside the maze!")
        if entry[1] < 1 or entry[1] > self._height:
            raise MazeError("ENTRY point is not inside the maze!")
        self._entry = entry

    def get_entry(self) -> Coords:
        return self._entry

    # EXIT --------------------------------------------------------------------
    def set_exit(self, exit: Coords) -> None:
        if exit[0] < 1 or exit[0] > self._width:
            raise MazeError("EXIT point is not inside the maze!")
        if exit[1] < 1 or exit[1] > self._height:
            raise MazeError("EXIT point is not inside the maze!")
        if exit == self._entry:
            raise MazeError("ENTRY point and EXIT point are in the same cell!")
        self._exit = exit

    def get_exit(self) -> Coords:
        return self._exit

    # CELLS -------------------------------------------------------------------
    def set_cells(self, cells: dict[Coords, Cell]) -> None:
        self._cells = cells

    def get_cells(self) -> dict[Coords, Cell]:
        return self._cells

    def set_cell(self, coord: Coords, new_cell: Cell) -> None:
        """
        Sets the given ``Cell`` as the new instance in the given coordinate.
        """
        if coord in self._cells.keys():
            self._cells[coord] = new_cell

    def get_cell(self, coord: Coords) -> Optional[Cell]:
        """
        Returns the ``Cell`` instance in the given coordinate if found.
        """
        if coord in self._cells.keys():
            return self._cells[coord]
        return None

    def get_cell_position(self, cell: Cell) -> Optional[Coords]:
        """
        Returns the coordinate of the given ``Cell`` instance.
        """
        for key, value in self._cells.items():
            if value == cell:
                return key
        return None

    def get_adjacent_cells(self, point: Coords) -> dict[
                               str, Optional[Coords]]:
        """
        Calculates where the adjacent cell coordinates should be
        from the point given.

        Returns
        -------
        adjacent_cells: dict[str, Optional[Coords]]
            A dictionary with a coordinate(or None if not found)
            for each direction.
        """
        # TODO: Improve docstring
        adjacent_cells: dict[str, Optional[Coords]] = {}
        if point[0] == 1:
            adjacent_cells[WEST] = None
        else:
            adjacent_cells[WEST] = (point[0] - 1, point[1])
        if point[0] == self._width:
            adjacent_cells[EAST] = None
        else:
            adjacent_cells[EAST] = (point[0] + 1, point[1])
        if point[1] == 1:
            adjacent_cells[NORTH] = None
        else:
            adjacent_cells[NORTH] = (point[0], point[1] - 1)
        if point[1] == self._height:
            adjacent_cells[SOUTH] = None
        else:
            adjacent_cells[SOUTH] = (point[0], point[1] + 1)
        return adjacent_cells

    # PLAYER ------------------------------------------------------------------
    def set_player(self, player: Player) -> None:
        self._player = player

    def get_player(self) -> Player:
        return self._player

    def __check_if_can_go(self, direction: str) -> bool:
        """
        Checks if there is a wall in the given direction from the
        player's cell.

        Parameters
        ----------
        direction: str
            The direction to check.

        Returns
        -------
        True
            If there is no wall in the given direction.
        False
            If there is a wall in the given direction.
        """
        player = self._player
        player_cell: Cell = self.get_cell(player.get_coordinates())
        if not player_cell:
            return False
        if player_cell["state"] & Maze.WALLS[direction]:
            return False
        return True

    def move_player(self, direction: str) -> bool:
        """
        It will try to move the player to the given direction by using
        the ``move_to`` method from the ``Player`` class.

        Returns
        -------
        True
            If the player moved.
        False
            If the player didn't move.
        """
        if self.__check_if_can_go(direction):
            adyacent = self.get_adjacent_cells(self._player)[direction]
            if adyacent is None:
                return False
            self._player.set_coordinates(adyacent)
            return True
        return False

    def put_player_at(self, coordinates: Coords) -> None:
        """
        Puts the player at a specific coordinate if possible.

        Notes
        -----
        This method completely ignores walls. It's a quick way
        to stablish the position of the player.
        """
        if self.get_cell(coordinates) is not None:
            self._player.set_coordinates(self.get_cell(coordinates))

    def get_player_coordinates(self) -> Coords:
        return self._player.get_coordinates()

    # FT_LOGO -----------------------------------------------------------------
    def get_ft_logo(self) -> bool:
        return self._ft_logo

    def get_ft_logo_cells(self) -> Optional[
            tuple[Coords]]:
        """
        Calculates where the 42 logo should be placed.
        If it can be placed, calculates where the center of the maze is and
        returns a tuple with all the coordinates
        for the 42 logo cells.

        Notes
        -----
        If the logo can't be placed (not enough size), nothing will be done.
        """
        from .ft_logo_cells import FtLogoCells

        scale = FtLogoCells.choose_logo_scale(self._width, self._height)
        if scale == 0:
            return
        ft_logo = FtLogoCells.scale_logo(scale)
        center_point = (ceil(self._width / 2),
                        ceil(self._height / 2))
        cells: list[Coords] = []
        for cell in ft_logo:
            cells.append((center_point[0] + cell[0],
                         center_point[1] + cell[1]))
        return tuple(cells)

    # PERFECT -----------------------------------------------------------------
    def get_perfect(self) -> bool:
        return self._perfect

    def open_random_walls(self) -> dict[Coords, Cell]:
        # TODO: Improve the logic of this function
        from .predefined import POSSIBLE_DIRECTIONS, OPPOSITE_DIRECTIONS

        # Initializing variables
        cells = self._cells
        width = self._width
        height = self._height
        op = OPPOSITE_DIRECTIONS

        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if cells[(x, y)]["fixed"]:
                    continue
                dir = choice(POSSIBLE_DIRECTIONS)
                if random() < Maze.WALL_OPENING_CHANCE:
                    adjacents = self.get_adjacent_cells((x, y))
                    if (adjacents[dir] and
                            not cells[adjacents[dir]]["fixed"] and
                            cells[(x, y)]["state"] & Maze.WALLS[dir]):
                        # If adjacent exists and has the wall desired to open:

                        # Changing current cell state
                        cells[(x, y)]["state"] -= Maze.WALLS[dir]

                        # Changing adjacent cell state
                        cells[adjacents[dir]]["state"] -= (
                            Maze.WALLS[op[dir]])
        return cells

    # PATHFINDER --------------------------------------------------------------
    def get_shortest_path(self) -> Optional[Pathway]:
        """
        Gets the shortest path from all of the found ones.

        Notes
        -----
        it only makes sense to use this method if the pathfinder
        was used. Otherwise, no paths were searched so ``None``
        will be returned.
        """
        if len(self._possible_pathways) > 0:
            return min(self._possible_pathways, key=len)
        return None

    # OUTPUT_FILE -------------------------------------------------------------
    def get_output_file(self) -> str:
        return self._output_file

    def print_output(self) -> None:
        """
        Writes in the given ``output_file`` the maze in a format which
        turns the wall state from each cell to hexadecimal.
        It also writes the original pathway found.
        """
        # TODO: Finish description when project is fully finished.
        # Add the directions followed to the exit too.
        print("Printing in the output file...")
        try:
            with open(self._output_file, "w") as f:
                for height in range(1, self._height + 1):
                    for width in range(1, self._width + 1):
                        f.write(
                            str(format(self._cells[(width, height)]["state"],
                                'X')))
                    f.write("\n")
                f.write("\n")
                # Entry point
                f.write(f"{self._entry[0]}, {self._entry[1]}\n")

                # Exit point
                f.write(f"{self._exit[0]}, {self._exit[1]}\n")

                # Directions followed
                for direction in self._directions_followed:
                    f.write(direction)
                f.write("\n")

                # Optional ------------------------------------------
                # f.write("Player's position: "
                #         f"{self.get_player_coordinates()}\n")
                f.write("Original Pathway----------------------\n")
                for coord in self._pathway:
                    f.write(f"{coord} | ")
                f.write("\n")
                f.write("Pathways found------------------------\n")
                i = 0
                for path in self._possible_pathways:
                    f.write(f"=== {i} ===\n")
                    for coord in path:
                        f.write(f"{coord} | ")
                    f.write("\n")
                    i += 1
                f.write("Shortest path-------------------------\n")
                shortest_path = self.get_shortest_path()
                if shortest_path:
                    for coord in shortest_path:
                        f.write(f"{coord} | ")
                print("")
        except FileNotFoundError:
            # This error should never happen, since open with 'w' doesn't raise
            # FileNotFoundError, it creates it in case it doesn't exist.
            # But just in case ...
            print("ERROR: output file not found")


if __name__ == "__main__":
    print("=== Maze Generation Example ===")
    print("\nGenerating a new maze...")
    try:
        maze = Maze(10, 10, (1, 1), (10, 10))
    except MazeError as e:
        print("ERROR:", e)
        sys.exit(1)
    maze.print_output()
