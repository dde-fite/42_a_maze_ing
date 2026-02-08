#!/bin/env python3

class Cell:

    def __init__(self, fixed: bool = False):
        from ..maze import NORTH, EAST, SOUTH, WEST
        self._visited = False   # To know if we already went through this cell
        self._state = 0b1111    # State of the walls from that cell
        self._adjacent: dict[str, Cell | None] = {NORTH: None, EAST: None,
                                                  SOUTH: None, WEST: None}
        self._fixed = fixed     # To know if it is a modifiable cell

    # VISITED -----------------------------------------------------------------
    def is_visited(self) -> bool:
        return self._visited

    def set_visited(self, value: bool) -> None:
        self._visited = value

    # STATE -------------------------------------------------------------------
    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int) -> None:
        self._state = state

    # ADJACENT CELLS ----------------------------------------------------------
    def get_adjacent(self) -> dict[str, "Cell | None"]:
        return self._adjacent

    # FIXED -------------------------------------------------------------------
    def is_fixed(self) -> bool:
        return self._fixed

    def set_fixed(self, fixed: bool) -> None:
        self._fixed = fixed

    # OTHER FUNCTIONS ---------------------------------------------------------
    def check_if_can_go(self, direction: str) -> bool:
        """
        Checks if there is a wall in the given direction.

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
        from ..maze import Maze
        if self._state & Maze.WALLS[direction]:
            return False
        return True

    def open_direction(self, direction: str) -> None:
        """
        Opens the wall from the cell in the given direction if possible,
        aswell as the opposite direction wall from the adjacent cell.

        Parameters
        ----------
        direction: str
            The direction where the wall to be broken is.

        Notes
        -----
        If the cell in the given direction is fixed or doesn't exist,
        the wall won't be opened.
        """
        from ..maze import Maze, NORTH, EAST, SOUTH, WEST
        adjacent = self._adjacent[direction]
        if adjacent is None or adjacent._fixed:
            return
        self._state -= self._state & Maze.WALLS[direction]
        if direction == NORTH:
            self._adjacent[NORTH]._state -= (self._adjacent[NORTH]._state &
                                             Maze.WALLS[SOUTH])
        if direction == EAST:
            self._adjacent[EAST]._state -= (self._adjacent[EAST]._state &
                                            Maze.WALLS[WEST])
        if direction == SOUTH:
            self._adjacent[SOUTH]._state -= (self._adjacent[SOUTH]._state &
                                             Maze.WALLS[NORTH])
        if direction == WEST:
            self._adjacent[WEST]._state -= (self._adjacent[WEST]._state &
                                            Maze.WALLS[EAST])
