#!/bin/env python3

# Main imports
from .maze import Maze
from .gen_types import Coords, Cell, Pathway
from .exceptions import MazeError
from .predefined import POSSIBLE_DIRECTIONS, OPPOSITE_DIRECTIONS

# Other imports
from random import shuffle


class Generator:

    @classmethod
    def dfs_generation(cls, maze: Maze) -> tuple[
                dict[Coords, Cell], Pathway, list[str]]:
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
        cells: dict[Coords, Cell] = {}
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                cells[(x, y)] = {"state": 0b1111, "visited": False,
                                 "fixed": False}

        # Stablishing fixed cells
        if ft_logo:
            ft_logo_cells = maze.get_ft_logo_cells()
            if ft_logo_cells:
                for cell in ft_logo_cells:
                    cells[cell]["fixed"] = True
            del ft_logo_cells

        # Checking if entry or exit are in the logo
        if cells[entry]["fixed"]:
            raise MazeError("ENTRY point is in a protected cell!")
        if cells[exit]["fixed"]:
            raise MazeError("EXIT point is in a protected cell!")

        # Initializing other variables
        point = entry
        cells[point]["visited"] = True
        directions = list(POSSIBLE_DIRECTIONS)
        passed_cells: Pathway = [point]
        directions_followed: list[str] = []
        exit_path: Pathway | None = None
        path_dir: list[str] | None = None
        op = OPPOSITE_DIRECTIONS
        adjacents = maze.get_adjacent_cells(point)
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
                        directions_followed.append(dir)
                        if point == exit:
                            exit_path = passed_cells.copy()
                            path_dir = directions_followed.copy()

                        # Recalcing adjacents
                        adjacents = maze.get_adjacent_cells(point)

                        advanced = True
                        break
            # Going backwards if point didn't advanced
            if not advanced:
                passed_cells.pop()
                directions_followed.pop()
                point = passed_cells[-1]
                adjacents = maze.get_adjacent_cells(point)
        return (cells, exit_path, path_dir)
