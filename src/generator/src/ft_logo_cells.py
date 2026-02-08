#!/bin/env python3

from .types import Coords
from .maze import Maze


class Ft_Logo_Cells():

    # These variables will only be used in this class
    __MIN_DIM_1 = 30
    __MIN_DIM_2 = 75
    __MIN_DIM_3 = 150

    __SCALE_1 = 1
    __SCALE_2 = 2
    __SCALE_3 = 3
    __SCALE_4 = 4

    DEFAULT_CELLS: tuple[Coords] = (
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

    # TODO: IMPROVE THIS DOCUMENTATION
    @classmethod
    def scale_logo(cls, scale: int) -> tuple[Coords]:
        """
        Adjusts the default 42 logo cells to the given scale.
        While the default 42 logo being a 1x1 cell combination
        of coordinates, the 42 logo scaled to 2 means that
        the 42 logo is a 2x2 cell combination of coordinates.
        If the 1x1 has a cell in the 1,1, the 2x2 will have cells
        in the 1,1, 1,2, 2,1, 2,2

        Parameters
        ----------
        scale: int
            The scale used for the logo.

        Returns
        -------
        scaled_cells: tuple[Coords]
            The new coordinates of the scaled 42 logo.
        """
        if scale <= 0:
            raise ValueError("Ft logo scale must be done with a positive "
                             "number!")
        scaled_cells: set[Coords] = set()
        for rel_x, rel_y in cls.DEFAULT_CELLS:
            block_origin_x = rel_x * scale
            block_origin_y = rel_y * scale
            for offset_x in range(scale):
                for offset_y in range(scale):
                    scaled_cells.add((block_origin_x + offset_x,
                                      block_origin_y + offset_y))
        return tuple(scaled_cells)

    @classmethod
    def choose_logo_scale(cls, maze_width: int, maze_height: int) -> int:
        """
        Chooses a scale for the 42 logo that adjusts correctly to the width
        and height of the maze.

        Parameters
        ----------
        maze_width: int
            The width of the maze.
        maze_height: int
            The height of the maze.

        Returns
        -------
        A scale that seems right to the given maze size.
        """
        if maze_width < Maze.MIN_FT_WIDTH or maze_height < Maze.MIN_FT_HEIGHT:
            return 0

        min_dimension = min(maze_width, maze_height)

        if min_dimension < cls.__MIN_DIM_1:
            return cls.__SCALE_1
        elif min_dimension < cls.__MIN_DIM_2:
            return cls.__SCALE_2
        elif min_dimension < cls.__MIN_DIM_3:
            return cls.__SCALE_3
        else:
            return cls.__SCALE_4


if __name__ == "__main__":
    print("Default cell coordinates:", Ft_Logo_Cells.DEFAULT_CELLS)
    print("Scaling to 2:", Ft_Logo_Cells.scale_logo(2))
    print("Scaling to 3:", Ft_Logo_Cells.scale_logo(3))
