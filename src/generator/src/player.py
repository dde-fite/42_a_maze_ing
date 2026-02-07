#!/bin/env python3

from .cell import Cell


class Player:

    def __init__(self, cell: Cell):
        self._cell = cell

    def get_cell(self) -> Cell:
        return self._cell

    def set_cell(self, cell: Cell | None) -> None:
        if cell is None:
            return
        self._cell = cell

    def move_to(self, direction: str) -> bool:
        """
        Tries to move the player to the given direction.

        Parameters
        ----------
        direction: str
            The direction chosen to move the player to.

        Returns
        ----------
        True
            If the player moved to the given direction.
        False
            If the player didn't move to the given direction.
        """
        if self._cell.check_if_can_go(direction):
            if self._cell._adjacent[direction] is None:
                return False
            self.set_cell(self._cell._adjacent[direction])
            return True
        return False
