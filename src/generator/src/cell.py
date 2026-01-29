#!/bin/env python3

class Cell:

    def __init__(self, fixed: bool = False):
        from .maze import NORTH, EAST, SOUTH, WEST
        self._visited = False   # To know if we already went through this cell
        self._state = 0b1111    # State of the walls from that cell
        self._adyacent: dict[str, Cell | None] = {NORTH: None, EAST: None,
                                                  SOUTH: None, WEST: None}
        self._fixed = fixed     # To know if it is a modifiable cell

    # VISITED
    def is_visited(self) -> bool:
        return self._visited

    def set_visited(self, value: bool) -> None:
        self._visited = value

    # STATE
    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int) -> None:
        self._state = state

    # ADYACENT CELLS
    def get_adyacent(self) -> dict[str, "Cell | None"]:
        return self._adyacent

    # FIXED
    def is_fixed(self) -> bool:
        return self._fixed

    def set_fixed(self, fixed: bool) -> None:
        self._fixed = fixed

    # Other functions
    # Checks if a wall un the given direction is closed or not,
    # returning True if it is closed (can't go through),
    # False if it is not (can go through)
    def check_if_can_go(self, direction: str) -> bool:
        from .maze import Maze
        if self._state & Maze.CLOSE_WALLS[direction]:
            return False
        return True

    # We open the wall at the direction given if it is possible to do so.
    # Also, if we do open it, we must open the opposite direction
    # from the adyacent one.
    def open_direction(self, direction: str) -> None:
        from .maze import Maze, NORTH, EAST, SOUTH, WEST
        adyacent = self._adyacent[direction]
        if adyacent is None or adyacent._fixed:
            return
        self._state -= self._state & Maze.CLOSE_WALLS[direction]
        if direction == NORTH:
            self._adyacent[NORTH]._state -= (self._adyacent[NORTH]._state &
                                             Maze.CLOSE_WALLS[SOUTH])
        if direction == EAST:
            self._adyacent[EAST]._state -= (self._adyacent[EAST]._state &
                                            Maze.CLOSE_WALLS[WEST])
        if direction == SOUTH:
            self._adyacent[SOUTH]._state -= (self._adyacent[SOUTH]._state &
                                             Maze.CLOSE_WALLS[NORTH])
        if direction == WEST:
            self._adyacent[WEST]._state -= (self._adyacent[WEST]._state &
                                            Maze.CLOSE_WALLS[EAST])
