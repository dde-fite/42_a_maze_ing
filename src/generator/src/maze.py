#!/bin/env python3

from .exceptions import MazeError
from .player import Player
from .cell import Cell
from .types import Coords, Cell_State, Pathway

# Other imports...
from math import ceil
from random import choice, random, shuffle, seed
from typing import Optional
import sys


NORTH = "NORTH"
SOUTH = "SOUTH"
EAST = "EAST"
WEST = "WEST"
POSSIBLE_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
OPPOSITE_DIRECTIONS = {NORTH: SOUTH, EAST: WEST,
                       SOUTH: NORTH, WEST: EAST}


class Maze:

    WALLS = {NORTH: 0b0001, EAST: 0b0010,
             SOUTH: 0b0100, WEST: 0b1000}

    MIN_FT_WIDTH = 9
    MIN_FT_HEIGHT = 7

    WALL_OPENING_CHANCE = 1 / 5
    PATH_ATTEMPTS = 10

    def __init__(self, width: int, height: int,
                 entry: Coords, exit: Coords,
                 output_file: str = "maze.txt",
                 ft_logo: bool = True, perfect: bool = False,
                 path_finder: bool = False,
                 seed_num: int = 0
                 ) -> None:
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
        if not ft_logo:
            ft_logo = True
        if not perfect:
            perfect = False
        if not path_finder:
            path_finder = False
        if not seed_num:
            seed_num = 0

        # Bases init
        self.__base_fields_init(width, height, ft_logo, entry, exit)
        self._output_file = output_file
        self._pathway: Pathway
        self._directions_followed: list[str]
        cell_generation: dict[Coords, Cell_State]

        # Extras init
        self._perfect = perfect
        self._player = Player(self._cells[entry])
        self._possible_pathways: list[Pathway] = []

        # Generating cells with the algorithm in the Generator class
        if seed_num:
            seed(seed_num)
        cell_generation, self._pathway, self._directions_followed = (
            Generator.dfs_generation(self))

        # If not perfect:
        if not self._perfect:

            # Open walls
            cell_generation = Generator.open_random_walls(self,
                                                          cell_generation)

            # Finding paths:
            # Recursive
            if path_finder:
                print("Looking for paths...")
                self._possible_pathways: list[Pathway] = (
                    Generator.path_finder(self, cell_generation))

            else:
                print("No pathfinder added!")

        # Stablishing the values for each cell
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                cell_generated = cell_generation[x, y]
                self._cells[x, y].set_state(cell_generated["state"])
                # self._cells[x, y].set_visited(cell_generated["visited"])
                self._cells[x, y].set_fixed(cell_generated["fixed"])

        print("Maze successfully generated!")

    # BASE INITIATION ---------------------------------------------------------
    def __base_fields_init(self, width: int, height: int, ft_logo: bool,
                           entry: Coords, exit: Coords):
        """
        Initiates all the class fields that are essential for any maze to work.
        """
        self.set_width(width)
        self.set_height(height)
        self._ft_logo = ft_logo
        self._cells: dict[Coords, Cell] = {}
        self.__initiate_cells()
        self.set_entry(entry)
        self.set_exit(exit)

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
        if self._cells[entry]._fixed:
            raise MazeError("ENTRY point is in a protected cell!")
        self._entry = entry

    def get_entry(self) -> Coords:
        return self._entry

    # EXIT --------------------------------------------------------------------
    def set_exit(self, exit: Coords) -> None:
        if exit[0] < 1 or exit[0] > self._width:
            raise MazeError("EXIT point is not inside the maze!")
        if exit[1] < 1 or exit[1] > self._height:
            raise MazeError("EXIT point is not inside the maze!")
        if self._cells[exit]._fixed:
            raise MazeError("EXIT point is in a protected cell!")
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

    def __initiate_cells(self) -> None:
        """
        Creates ``Cell`` instances for each slot in the maze.

        Notes
        -----
        Each cell will have all its walls closed and will set
        all of its adjacent instances.
        """
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Initiating new cells for each coordinate in the maze
                self._cells[(x, y)] = Cell()
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Stablihing adjacent cells for each cell
                current_cell = self._cells[(x, y)]
                if x == 1:
                    current_cell._adjacent[WEST] = None
                else:
                    current_cell._adjacent[WEST] = self._cells[(x - 1, y)]
                if y == 1:
                    current_cell._adjacent[NORTH] = None
                else:
                    current_cell._adjacent[NORTH] = self._cells[(x, y - 1)]
                if x == self._width:
                    current_cell._adjacent[EAST] = None
                else:
                    current_cell._adjacent[EAST] = self._cells[(x + 1, y)]
                if y == self._height:
                    current_cell._adjacent[SOUTH] = None
                else:
                    current_cell._adjacent[SOUTH] = self._cells[(x, y + 1)]

        # Generating 42 logo (the function checks if it can be done itself)
        if self._ft_logo:
            self.__generate_ft_logo()

    def __generate_ft_logo(self) -> None:
        """
        Calculates where the 42 logo should be placed.
        If it can be placed, it will set the ``fixed``value
        from each cell where the logo should be to True.

        Notes
        -----
        If the logo can't be placed (not enough size), nothing will be done.
        """
        if (self._width < Maze.MIN_FT_WIDTH
                or self._height < Maze.MIN_FT_HEIGHT):
            return
        ft_logo: tuple[tuple[int, int]] = (  # type: ignore
                (-1, 0),
                (-2, 0),
                (-3, 0),
                (-3, -1),
                (-3, -2),
                (-1, 1),
                (-1, 2),
                (1, 0),
                (2, 0),
                (3, 0),
                (3, -1),
                (3, -2),
                (2, -2),
                (1, -2),
                (1, 1),
                (1, 2),
                (2, 2),
                (3, 2)
            )
        center_point = (ceil(self._width / 2),
                        ceil(self._height / 2))
        for pix in ft_logo:
            ft_cell = self.get_cell((center_point[0] + pix[0],
                                    center_point[1] + pix[1]))
            if ft_cell is None:
                # This should never happen because
                # we won't get a cell that doesn't exist
                raise MazeError("Unexpected error")
            else:
                ft_cell.set_fixed(True)

    # PLAYER ------------------------------------------------------------------
    def set_player(self, player: Player) -> None:
        self._player = player

    def get_player(self) -> Player:
        return self._player

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
        return self._player.move_to(direction)

    def put_player_at(self, coordinates: Coords) -> None:
        """
        Puts the player at a specific coordinate if possible.

        Notes
        -----
        This method completely ignores walls. It's a quick way
        to stablish the position of the player.
        """
        if self.get_cell(coordinates) is not None:
            self._player.set_cell(self.get_cell(coordinates))

    def get_player_coordinates(self) -> Coords:
        return self.get_cell_position(self._player.get_cell())

    # FT_LOGO -----------------------------------------------------------------
    def get_ft_logo(self) -> bool:
        return self._ft_logo

    # PERFECT -----------------------------------------------------------------
    def get_perfect(self) -> bool:
        return self._perfect

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
                        f.write(str(format(self._cells[(width, height)]._state,
                                           'X')) + " ")  # TODO: DELETE THE ' '
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
                f.write("Player's position: "
                        f"{self.get_player_coordinates()}\n")
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


class Generator:
    # TODO: Structure the class methods in a more clear and efficient way

    @staticmethod
    def __get_ft_logo_cells(width: int, height: int) -> Optional[
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
        from .ft_logo_cells import Ft_Logo_Cells

        scale = Ft_Logo_Cells.choose_logo_scale(width, height)
        if scale == 0:
            return
        ft_logo = Ft_Logo_Cells.scale_logo(scale)
        center_point = (ceil(width / 2),
                        ceil(height / 2))
        cells: list[Coords] = []
        for cell in ft_logo:
            cells.append((center_point[0] + cell[0],
                         center_point[1] + cell[1]))
        return tuple(cells)

    @staticmethod
    def __get_adjacent_cells(point: Coords,
                             width: int, height: int) -> dict[
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
        if point[0] == width:
            adjacent_cells[EAST] = None
        else:
            adjacent_cells[EAST] = (point[0] + 1, point[1])
        if point[1] == 1:
            adjacent_cells[NORTH] = None
        else:
            adjacent_cells[NORTH] = (point[0], point[1] - 1)
        if point[1] == height:
            adjacent_cells[SOUTH] = None
        else:
            adjacent_cells[SOUTH] = (point[0], point[1] + 1)
        return adjacent_cells

    @classmethod
    def dfs_generation(cls, maze: Maze) -> tuple[
                dict[Coords, Cell_State], Pathway, list[str]]:
        """
        Generate a perfect maze using a depth-first search (DFS) algorithm.

        The algorithm starts at the maze entry point and recursively explores
        unvisited neighboring cells, carving passages between them. Fixed cells
        are skipped during generation.

        Parameters
        ----------
        maze : Maze
            Maze configuration including dimensions, entry/exit points and
            optional fixed cells.

        Returns
        -------
        cells : dict[Coords, Cell_State]
            Mapping of cell coordinates to their final state after generation.
        exit_path : Pathway or None
            Path from entry to exit if reachable, otherwise ``None``.
        directions_followed: list[str]
            List of every direction that was followed to reach the end.
        Notes
        -----
        This implementation uses an iterative DFS with backtracking and random
        neighbor selection to ensure maze randomness.

        References
        ----------
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Depth-first_search

        """
        # Initializing variables
        width = maze.get_width()
        height = maze.get_height()
        ft_logo = maze.get_ft_logo()
        entry = maze.get_entry()
        exit = maze.get_exit()

        # Initializing cells
        cells: dict[Coords, Cell_State] = {}
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                cells[(x, y)] = {"state": 0b1111, "visited": False,
                                 "fixed": False}

        # Stablishing fixed cells
        if ft_logo:
            ft_logo_cells = cls.__get_ft_logo_cells(width, height)
            if ft_logo_cells:
                for cell in ft_logo_cells:
                    cells[cell]["fixed"] = True

        # Initializing other variables
        point = entry
        cells[point]["visited"] = True
        directions = list(POSSIBLE_DIRECTIONS)
        passed_cells: Pathway = [point]
        directions_followed: list[str] = []
        exit_path: Pathway | None = None
        op = OPPOSITE_DIRECTIONS
        adjacents = cls.__get_adjacent_cells(point, width, height)
        advanced = True

        # Not being able to move any direction and being at the starting point
        # will mean that we already checked every possible way
        print("Generating maze with dfs algorithm...")
        while not (point == entry and not advanced):
            advanced = False

            # Randomizing directions order
            shuffle(directions)

            for dir in directions:
                if adjacents[dir]:
                    adjacent_cell = adjacents[dir]
                    ad_cell_data = cells[adjacent_cell]  # adjacent cell data
                    if (not ad_cell_data["visited"] and
                            not ad_cell_data["fixed"]):
                        # Changing current cell state
                        cells[point]["state"] -= Maze.WALLS[dir]

                        # Changing adjacent cell state
                        ad_cell_data["state"] -= (
                            Maze.WALLS[op[dir]])
                        ad_cell_data["visited"] = True

                        # Updating stuff
                        point = adjacent_cell
                        passed_cells.append(point)
                        directions_followed.append(dir[0])
                        if point == exit:
                            exit_path = passed_cells.copy()

                        # Recalcing adjacents
                        adjacents = cls.__get_adjacent_cells(
                            point, width, height)

                        advanced = True
                        break
            # Going backwards if point didn't advanced
            if not advanced:
                passed_cells.pop()
                point = passed_cells[-1]
                adjacents = cls.__get_adjacent_cells(point, width, height)
        return (cells, exit_path, directions_followed)

    @classmethod
    def path_finder(cls, maze: Maze,
                    cells:
                    dict[Coords, Cell_State]) -> list[Pathway]:
        """
        Find possible paths from the maze entry to the exit.

        This method explores the maze using a randomized depth-first traversal
        constrained by the current cell wall configuration. Multiple distinct
        paths may be discovered, up to a predefined attempt limit.

        Parameters
        ----------
        maze : Maze
            Maze instance providing dimensions and entry/exit coordinates.
        cells : dict[Coords, Cell_State]
            Mapping of cell coordinates to their current state, including wall
            configuration.

        Returns
        -------
        pathways : list[Pathway]
            List of unique paths from entry to exit. Each path is represented
            as an ordered sequence of coordinates. At least one path will
            always be found if the cell states were not changed.

        Notes
        -----
        - The search is bounded by ``Maze.PATH_ATTEMPTS`` to avoid infinite
        loops.
        - Paths are discovered using random direction ordering, so results
        are non-deterministic.
        - Cells marked as dead ends are temporarily excluded from exploration
        to improve performance.

        See Also
        --------
        dfs_generation : Maze generation using depth-first search.
        """
        # Initializing variables
        width = maze.get_width()
        height = maze.get_height()
        entry = maze.get_entry()
        exit = maze.get_exit()

        attempts = 0
        point = entry

        directions = list(POSSIBLE_DIRECTIONS)
        pathways: list[Pathway] = []
        passed_cells: list[Coords] = [point]
        wrong_cells: set[Coords] = set()
        adjacents = cls.__get_adjacent_cells(point, width, height)

        print("Finding possible paths...")
        while attempts < Maze.PATH_ATTEMPTS:
            moved = False
            shuffle(directions)

            for dir in directions:
                if not adjacents[dir] or adjacents[dir] in passed_cells:
                    continue
                if cells[point]["state"] & Maze.WALLS[dir]:
                    continue
                elif (adjacents[dir] not in wrong_cells):
                    point = adjacents[dir]
                    passed_cells.append(point)
                    adjacents = cls.__get_adjacent_cells(point, width, height)
                    moved = True
                    break
            if not moved:
                passed_cells.pop()
                if point != exit:
                    wrong_cells.add(point)
                point = passed_cells[-1]
                adjacents = cls.__get_adjacent_cells(point, width, height)
            elif point == exit:
                attempts += 1
                if passed_cells not in pathways:
                    pathways.append(passed_cells.copy())
                passed_cells.clear()
                point = entry
                passed_cells.append(entry)
                adjacents = cls.__get_adjacent_cells(point, width, height)
        return pathways

    @classmethod
    def open_random_walls(cls, maze: Maze, cells: dict[Coords, Cell_State]
                          ) -> dict[Coords, Cell_State]:
        # TODO: Improve the logic of this function
        # Initializing variables
        width = maze.get_width()
        height = maze.get_height()
        op = OPPOSITE_DIRECTIONS

        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if cells[(x, y)]["fixed"]:
                    continue
                dir = choice(POSSIBLE_DIRECTIONS)
                if random() < Maze.WALL_OPENING_CHANCE:
                    adjacents = cls.__get_adjacent_cells((x, y), width, height)
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


if __name__ == "__main__":
    print("=== Maze Generation Example ===")
    print("\nGenerating a new maze...")
    try:
        maze = Maze(10, 10, (1, 1), (10, 10))
    except MazeError as e:
        print("ERROR:", e)
        sys.exit(1)
    maze.print_output()
