#!/bin/env python3

from typing import Optional
# from __future__ import annotations  # Cell problem...
from math import ceil


class MazeError(Exception):
    pass


NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"
POSSIBLE_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]


class Cell:

    def __init__(self, fixed: bool = False):
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
        if self._state & Maze.CLOSE_WALLS[direction]:
            return False
        return True

    # We open the wall at the direction given if it is possible to do so.
    # Also, if we do open it, we must open the opposite direction
    # from the adyacent one.
    def open_direction(self, direction: str) -> None:
        adyacent = self._adyacent[direction]
        if adyacent is not None and not adyacent._fixed:
            self._state -= self._state & Maze.CLOSE_WALLS[direction]
        else:
            return
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


class Maze:

    OUTPUT_FILE = "maze.txt"

    CLOSE_WALLS = {NORTH: 0b0001, EAST: 0b0010,
                   SOUTH: 0b0100, WEST: 0b1000}

    MIN_FT_WIDTH = 9
    MIN_FT_HEIGHT = 7

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.set_width(width)
        self.set_height(height)
        self.set_entry(entry)
        self.set_exit(exit)
        self._cells: dict[tuple[int, int], Cell] = {}
        self.initiate_cells()
        self._player = Player(self._cells[entry])

    # WIDTH
    def set_width(self, width: int) -> None:
        if width < 1:
            raise MazeError("WIDTH value can't be lower than 1!")
        self._width = width

    def get_width(self) -> int:
        return self._width

    # HEIGHT
    def set_height(self, height: int) -> None:
        if height < 1:
            raise MazeError("HEIGHT value can't be lower than 1!")
        self._height = height

    def get_height(self) -> int:
        return self._height

    # ENTRY
    def set_entry(self, entry: tuple[int, int]) -> None:
        if entry[0] < 1 or entry[0] > self._width:
            raise MazeError("ENTRY point is not inside the maze!")
        if entry[1] < 1 or entry[1] > self._height:
            raise MazeError("ENTRY point is not inside the maze!")
        self._entry = entry

    def get_entry(self) -> tuple[int, int]:
        return self._entry

    # EXIT
    def set_exit(self, exit: tuple[int, int]) -> None:
        if exit[0] < 1 or exit[0] > self._width:
            raise MazeError("EXIT point is not inside the maze!")
        if exit[1] < 1 or exit[1] > self._height:
            raise MazeError("EXIT point is not inside the maze!")
        self._exit = exit

    def get_exit(self) -> tuple[int, int]:
        return self._exit

    # CELLS
    def set_cells(self, cells: dict[tuple[int, int], Cell]) -> None:
        self._cells = cells

    def get_cells(self) -> dict[tuple[int, int], Cell]:
        return self._cells

    def set_cell(self, coord: tuple[int, int], new_cell: Cell) -> None:
        if coord in self._cells.keys():
            self._cells[coord] = new_cell

    def get_cell(self, coord: tuple[int, int]) -> Optional[Cell]:
        if coord in self._cells.keys():
            return self._cells[coord]
        return None

    def get_cell_position(self, cell: Cell) -> Optional[tuple[int, int]]:
        for key, value in self._cells.items():
            if value == cell:
                return key
        return None

    def __generate_ft_logo(self) -> None:
        if (self._width < Maze.MIN_FT_WIDTH
                or self._height < Maze.MIN_FT_HEIGHT):
            return
        ft_logo: tuple = (  # type: ignore
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

    def initiate_cells(self) -> None:
        # Initiates all cells, with all the walls on them closed
        # at the start (done by the Cell constructor).
        # Also stablishing their adyacent cells.
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Initiating new cells for each coordinate in the maze
                self._cells.update({(x, y): Cell()})
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Stablihing adyacent cells for each cell
                current_cell = self._cells[(x, y)]
                if x == 1:
                    current_cell._adyacent[WEST] = None
                else:
                    current_cell._adyacent[WEST] = self._cells[(x - 1, y)]
                if y == 1:
                    current_cell._adyacent[NORTH] = None
                else:
                    current_cell._adyacent[NORTH] = self._cells[(x, y - 1)]
                if x == self._width:
                    current_cell._adyacent[EAST] = None
                else:
                    current_cell._adyacent[EAST] = self._cells[(x + 1, y)]
                if y == self._height:
                    current_cell._adyacent[SOUTH] = None
                else:
                    current_cell._adyacent[SOUTH] = self._cells[(x, y + 1)]
        # Generating 42 logo (the function checks if it can be done itself)
        self.__generate_ft_logo()

    # PLAYER
    def set_player(self, player: Player) -> None:
        self._player = player

    def get_player(self) -> Player:
        return self._player

    def move_player(self, direction: str) -> bool:
        return self._player.move_to(direction)

    def put_player_at(self, coordinates: tuple[int, int]) -> None:
        # Moves the player to a specific cell
        if self.get_cell(coordinates) is not None:
            self._player.set_cell(self.get_cell(coordinates))

    def get_player_coordinates(self) -> tuple[int, int]:
        return self.get_cell_position(self._player.get_cell())

    # OUTPUT_FILE
    @classmethod
    def get_output_file(cls) -> str:
        return cls.OUTPUT_FILE

    def print_output(self):
        try:
            with open(Maze.get_output_file(), "w") as f:
                for height in range(1, self._height + 1):
                    for width in range(1, self._width + 1):
                        f.write(str(format(self._cells[(width, height)]._state, 'x')) + " ")
                    f.write("\n")
                f.write("\n")
                f.write(f"Entry point: ({self._entry[0]}, {self._entry[1]})\n")
                f.write(f"Exit point: ({self._exit[0]}, {self._exit[1]})\n")
                f.write("Player's position: "
                        f"{self.get_player_coordinates()}\n")
        except FileNotFoundError:
            # This error should never happen, since open with 'w' doesn't raise
            # FileNotFoundError, it creates it in case it doesn't exist.
            # But just in case ...
            print("ERROR: output file not found")


if __name__ == "__main__":
    print("\nCHECK COMMENTS IN CODE FOR ANY EXPLANATION!\n\n")
    try:
        maze = Maze(20, 20, (2, 2), (10, 10))

        # Printing the entry point for example:
        print("Checking cells...")
        print("State of cell 10,10 (15 means every wall closed, ...):", maze.get_cells()[(10, 10)]._state)
        print("Position in memory from 2,1:", maze.get_cells()[(2, 1)])
        print("Position in memory from NORTH of 2,2:", maze.get_cells()[(2, 2)].get_adyacent()[NORTH])
        print("They are the same :)")

        print("\nMoving the player...")
        player = maze.get_player()
        print("Player at cell:", maze.get_cell_position(player.get_cell()))
        print("Can we go to NORTH?", player.get_cell().check_if_can_go(NORTH))
        print("Did we move?", maze.move_player(NORTH))
        print("Player after trying to move NORTH:", maze.get_cell_position(player.get_cell()))

        print("\nTesting to check if moving is possible...")
        # 2 examples to see if a wall is closed or not
        if 0b0000 & Maze.CLOSE_WALLS[NORTH]:  # NORTH = 0b0001
            print("North is closed")
        if 0b0001 & Maze.CLOSE_WALLS[NORTH]:
            print("North is closed")
        # This way we can see if some cell is closed in some direction
        if maze.get_cells()[(1, 2)]._state & Maze.CLOSE_WALLS[NORTH]:
            print("North direction is closed")
        # To open a cell wall, we can do this
        maze.get_cells()[(3, 3)]._state -= maze.get_cells()[(3, 3)]._state & Maze.CLOSE_WALLS[NORTH]  # Consider making a function for this
        print(maze.get_cells()[(3, 3)]._state)

        # Opening a cell wall with the function
        print("\nTesting opening walls...")
        print("Cell 2,2 state:", maze.get_cells()[(2, 2)]._state)
        print("Cell 2,3 state:", maze.get_cells()[(2, 2)]._state)
        print("OPENING SOUTH OF 2,2 ...")
        maze.get_cells()[(2, 2)].open_direction(SOUTH)
        print("Cell 2,2 state after function:", maze.get_cells()[(2, 2)]._state)
        print("Cell 2,3 state after function:", maze.get_cells()[(2, 3)]._state)

        # Checking if move is possible
        print("\nTesting going in different directions...")
        print("Can we go SOUTH from 2,2? ",
              maze.get_cells()[(2, 2)].check_if_can_go(SOUTH))
        print("Can we go NORTH from 2,2? ",
              maze.get_cells()[(2, 2)].check_if_can_go(NORTH))
        print("Can we go SOUTH from 2,3? ",
              maze.get_cells()[(2, 3)].check_if_can_go(SOUTH))
        print("Can we go NORTH from 2,3? ",
              maze.get_cells()[(2, 3)].check_if_can_go(NORTH))

        # Moving the player again
        print("\nMoving the player again...")
        print("Player starting position:", maze.get_cell_position(player.get_cell()))
        print("Player cell state:", player.get_cell()._state)

        print("Can we go to NORTH?", player.get_cell().check_if_can_go(NORTH))
        maze.move_player(NORTH)
        print("Player after moving to NORTH:", maze.get_cell_position(player.get_cell()))

        print("Can we go to SOUTH?", player.get_cell().check_if_can_go(SOUTH))
        maze.move_player(SOUTH)
        print("Player after moving to SOUTH:", maze.get_cell_position(player.get_cell()))
    except MazeError as e:
        print("ERROR:", e)
