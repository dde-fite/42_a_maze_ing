#!/bin/env python3

# CONSIDER MAKING THE VARIABLE 'PLAYER' FROM THE MAZE CLASS AS ANOTHER CLASS (position, color, number of moves, ...)

import random


class MazeError(Exception):
    pass


class Cell:

    def __init__(self):
        self._passed = False  # To know if we already went through this cell
        self._color = "Red"  # Color of the walls from that cell
        self._state = 0b1111  # State of the walls from that cell
        self._adyacent: dict[str, Cell | None] = {"NORTH": None, "EAST": None,
                                                  "SOUTH": None, "WEST": None}  # Adyacent cells in each direction

    # This function was done quikly might be wrong. We must check if the wall can be broken
    def open_direction(self, direction: str) -> None:
        if direction == "NORTH" and self._adyacent["NORTH"] is not None:
            self._state -= self._state & Maze.CLOSE_WALLS["NORTH"]
            self._adyacent["NORTH"]._state -= self._state & Maze.CLOSE_WALLS["SOUTH"]
        if direction == "EAST" and self._adyacent["EAST"] is not None:
            self._state -= self._state & Maze.CLOSE_WALLS["EAST"]
            self._adyacent["EAST"]._state -= self._state & Maze.CLOSE_WALLS["WEST"]
        if direction == "SOUTH" and self._adyacent["SOUTH"] is not None:
            self._state -= self._state & Maze.CLOSE_WALLS["SOUTH"]
            self._adyacent["SOUTH"]._state -= self._state & Maze.CLOSE_WALLS["NORTH"]
        if direction == "WEST" and self._adyacent["WEST"] is not None:
            self._state -= self._state & Maze.CLOSE_WALLS["WEST"]
            self._adyacent["WEST"]._state -= self._state & Maze.CLOSE_WALLS["EAST"]

    def check_if_can_go(self, direction: str) -> bool:
        if direction == "NORTH" and self._state & Maze.CLOSE_WALLS["NORTH"]:
            return False
        if direction == "EAST" and self._state & Maze.CLOSE_WALLS["EAST"]:
            return False
        if direction == "SOUTH" and self._state & Maze.CLOSE_WALLS["SOUTH"]:
            return False
        if direction == "WEST" and self._state & Maze.CLOSE_WALLS["WEST"]:
            return False
        return True


class Maze:

    OUTPUT_FILE = "maze.txt"

    CLOSE_WALLS = {"NORTH": 0b0001, "EAST": 0b0010,
                   "SOUTH": 0b0100, "WEST": 0b1000}

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.set_width(width)
        self.set_height(height)
        self.set_entry(entry)
        self.set_exit(exit)
        self._cells: dict[tuple[int, int], Cell] = {}
        self.initiate_cells()
        self._player = list(self._entry) # Must be a list so it can change

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

    def initiate_cells(self) -> None:
        # Initiates all cells, with all the walls on them closed (done by the Cell constructor).
        # Also stablishing their adyacent cells.
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Initiating new cells for each coordinate in the maze
                self._cells.update({(x, y): Cell()})
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                # Stablihing adyacent cells for each cell
                if x == 1:
                    self._cells[(x, y)]._adyacent["WEST"] = None
                else:
                    self._cells[(x, y)]._adyacent["WEST"] = self._cells[(x - 1, y)]
                if y == 1:
                    self._cells[(x, y)]._adyacent["NORTH"] = None
                else:
                    self._cells[(x, y)]._adyacent["NORTH"] = self._cells[(x, y - 1)]
                if x == self._width:
                    self._cells[(x, y)]._adyacent["EAST"] = None
                else:
                    self._cells[(x, y)]._adyacent["EAST"] = self._cells[(x + 1, y)]
                if y == self._height:
                    self._cells[(x, y)]._adyacent["SOUTH"] = None
                else:
                    self._cells[(x, y)]._adyacent["SOUTH"] = self._cells[(x, y + 1)]

    # PLAYER
    def set_player(self, new_position: list[int]):
        self._player = new_position

    def get_player(self) -> list[int]:
        return self._player

    def move_player(self, direction: str) -> bool:
        player_pos = tuple(self._player)
        if direction == "WEST":
            if self._player[0] == 1:
                return False
            elif self._cells[player_pos].check_if_can_go("WEST"):
                self._player[0] -= 1
                return True
            return False
        elif direction == "NORTH":
            if self._player[1] == 1:
                return False
            elif self._cells[player_pos].check_if_can_go("NORTH"):
                self._player[1] -= 1
                return True
            return False
        elif direction == "EAST":
            if self._player[0] == self._width:
                return False
            elif self._cells[player_pos].check_if_can_go("EAST"):
                self._player[0] += 1
                return True
            return False
        elif direction == "SOUTH":
            if self._player[1] == self._height:
                return False
            elif self._cells[player_pos].check_if_can_go("SOUTH"):
                self._player[1] += 1
                return True
            return False
        return False

    # OUTPUT_FILE
    @classmethod
    def get_output_file(cls):
        return cls.OUTPUT_FILE


def move_player(maze: Maze, move_to: tuple[int, int]) -> None:
    maze.set_player(list(move_to))


if __name__ == "__main__":
    print("\nCHECK COMMENTS IN CODE FOR ANY EXPLANATION!\n\n")
    try:
        maze = Maze(20, 20, (2, 2), (10, 10))
        # Printing the entry point for example:
        print("Checking cells...")
        print("State of cell 10,10 (15 means every wall closed, ...):", maze._cells[(10, 10)]._state)
        print("Position in memory from 2,1:", maze.get_cells()[(2, 1)])
        print("Position in memory from NORTH of 2,2:", maze.get_cells()[(2, 2)]._adyacent["NORTH"])
        print("They are the same :)")

        print("\nMoving the player...")
        print("Player starting position:", maze.get_player())
        maze.move_player("NORTH")
        print("Can we go to NORTH?", maze.get_cells()[tuple(maze._player)].check_if_can_go("NORTH"))
        print("Player after moving to NORTH:", maze.get_player())

        print("\nTesting to check if moving is possible...")
        # 2 examples to see if a wall is closed or not
        if 0b0000 & Maze.CLOSE_WALLS["NORTH"]:  # NORTH = 0b0001
            print("North is closed")
        if 0b0001 & Maze.CLOSE_WALLS["NORTH"]:
            print("North is closed")
        # This way we can see if some cell is closed in some direction
        if maze.get_cells()[(1, 2)]._state & Maze.CLOSE_WALLS["NORTH"]:
            print("North direction is closed")
        # To open a cell wall, we can do this
        maze.get_cells()[(1, 1)]._state -= maze.get_cells()[(1, 1)]._state & Maze.CLOSE_WALLS["NORTH"]  # Consider making a function for this
        print(maze.get_cells()[(1, 1)]._state)

        # Opening a cell wall with the function
        print("\nTesting opening walls...")
        print("Cell 2,2 state:", maze.get_cells()[(2, 2)]._state)
        print("Cell 2,3 state:", maze.get_cells()[(2, 2)]._state)
        print("OPENING SOUTH OF 2,2 ...")
        maze.get_cells()[(2, 2)].open_direction("SOUTH")
        print("Cell 2,2 state after function:", maze.get_cells()[(2, 2)]._state)
        print("Cell 2,3 state after function:", maze.get_cells()[(2, 3)]._state)

        # Checking if move is possible
        print("\nTesting going in different directions...")
        print("Can we go SOUTH from 2,2? ",
              maze.get_cells()[(2, 2)].check_if_can_go("SOUTH"))
        print("Can we go NORTH from 2,2? ",
              maze.get_cells()[(2, 2)].check_if_can_go("NORTH"))
        print("Can we go SOUTH from 2,3? ",
              maze.get_cells()[(2, 3)].check_if_can_go("SOUTH"))
        print("Can we go NORTH from 2,3? ",
              maze.get_cells()[(2, 3)].check_if_can_go("NORTH"))

        # Moving the player again
        print("\nMoving the player again...")
        print("Player starting position:", maze.get_player())
        print("Player cell state:", maze.get_cells()[tuple(maze._player)]._state)

        print("Can we go to NORTH?", maze.get_cells()[tuple(maze._player)].check_if_can_go("NORTH"))
        maze.move_player("NORTH")
        print("Player after moving to NORTH:", maze.get_player())

        print("Can we go to SOUTH?", maze.get_cells()[tuple(maze._player)].check_if_can_go("SOUTH"))
        maze.move_player("SOUTH")
        print("Player after moving to SOUTH:", maze.get_player())

        # Moving the player randomly until it finds the exit...
        print("\nMoving the player randomly...")
        POSSIBLE_MOVES = ("NORTH", "EAST", "SOUTH", "WEST")
        print("Player's position at the beginning:", maze.get_player())
        print("======================================")
        moves = 0
        while tuple(maze.get_player()) != maze.get_exit() and moves < 1000000:
            player_position = tuple(maze.get_player())
            direction = random.choice(POSSIBLE_MOVES)
            print("Direction chosen:", direction)
            maze.get_cells()[player_position].open_direction(direction)
            maze.move_player(direction)
            print("Player's new position:", maze.get_player())
            moves += 1
            print("=================================")
        print("Exit was at:", maze.get_exit())
        print("Player last position is at:", maze.get_player())
        print("Total moves:", moves)
        print("\nCOMMENT THE LAST WHILE TO SEE OTHER PART OF THE CODE!")
        try:
            with open(Maze.get_output_file(), "w") as f:
                for height in range(1, maze.get_height() + 1):
                    for width in range(1, maze.get_width() + 1):
                        f.write(str(format(maze.get_cells()[(width, height)]._state, 'x')) + " ")
                    f.write("\n")
        except FileNotFoundError:
            # This error should never happen, since open with 'w' doesn't raise
            # FileNotFoundError, it creates it in case it doesn't exist.
            # But just in case ...
            print("ERROR: output file not found")
    except MazeError as e:
        print("ERROR:", e)
