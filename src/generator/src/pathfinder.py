#!/bin/env python3

# Main imports
from .maze import Maze
from .types import Coords, Pathway
from .predefined import POSSIBLE_DIRECTIONS

# Other imports
from random import shuffle


class PathFinder:

    @classmethod
    def path_finder_dfs(cls, maze: Maze):
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
        cells = maze.get_cells()

        attempts = 0
        point = entry

        directions = list(POSSIBLE_DIRECTIONS)
        pathways: list[Pathway] = []
        passed_cells: list[Coords] = [point]
        wrong_cells: set[Coords] = set()
        adjacents = maze.get_adjacent_cells(point)

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
                    adjacents = maze.get_adjacent_cells(point)
                    moved = True
                    break
            if not moved:
                passed_cells.pop()
                if point != exit:
                    wrong_cells.add(point)
                point = passed_cells[-1]
                adjacents = maze.get_adjacent_cells(point)
            elif point == exit:
                attempts += 1
                if passed_cells not in pathways:
                    pathways.append(passed_cells.copy())
                passed_cells.clear()
                point = entry
                passed_cells.append(entry)
                adjacents = maze.get_adjacent_cells(point, width, height)
        return pathways
