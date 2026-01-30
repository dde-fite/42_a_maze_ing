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
        if self._cell.check_if_can_go(direction):
            self.set_cell(self._cell._adyacent[direction])
            return True
        return False

    def can_go_somewhere(self) -> bool:
        from .maze import POSSIBLE_DIRECTIONS
        for dir in POSSIBLE_DIRECTIONS:
            # print(f"Checking if we can go {dir}...")
            adyacent = self.get_cell().get_adyacent()[dir]
            if (adyacent is not None and adyacent.is_visited() is False and
                    adyacent.is_fixed() is False):
                # print(f"WE CAN GO {dir}")
                return True
        # print("Can't go anywhere :(")
        return False

    def can_move_somewhere(self) -> bool:
        from .maze import POSSIBLE_DIRECTIONS
        for dir in POSSIBLE_DIRECTIONS:
            # print(f"Checking if we can go {dir}...")
            adyacent = self.get_cell().get_adyacent()[dir]
            if (adyacent is not None and adyacent.is_visited() is False and
                    adyacent.is_fixed() is False and
                    self.get_cell().check_if_can_go(dir)):
                # print(f"WE CAN GO {dir}")
                return True
        # print("Can't go anywhere :(")
        return False
