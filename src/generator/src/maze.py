#!/bin/env python3

from .exceptions import MazeError
from .player import Player
from .cell import Cell


# Other imports...
from math import ceil
import random
from typing import Optional
import sys


NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"
POSSIBLE_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]


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
        self._pathway: dict[int, tuple[int, int]] = {}
        self._possible_pathways: list[dict[int, tuple[int, int]]] = {}

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
    def set_entry(self, entry: tuple[int, int]) -> None:
        if entry[0] < 1 or entry[0] > self._width:
            raise MazeError("ENTRY point is not inside the maze!")
        if entry[1] < 1 or entry[1] > self._height:
            raise MazeError("ENTRY point is not inside the maze!")
        self._entry = entry

    def get_entry(self) -> tuple[int, int]:
        return self._entry

    # EXIT --------------------------------------------------------------------
    def set_exit(self, exit: tuple[int, int]) -> None:
        if exit[0] < 1 or exit[0] > self._width:
            raise MazeError("EXIT point is not inside the maze!")
        if exit[1] < 1 or exit[1] > self._height:
            raise MazeError("EXIT point is not inside the maze!")
        self._exit = exit

    def get_exit(self) -> tuple[int, int]:
        return self._exit

    # CELLS -------------------------------------------------------------------
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

    def __reset_cells(self) -> None:
        # Resets the 'visited' value of every Cell
        for cell in self._cells.values():
            cell.set_visited(False)

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

    # PLAYER ------------------------------------------------------------------
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

    # OUTPUT_FILE -------------------------------------------------------------
    @classmethod
    def get_output_file(cls) -> str:
        return cls.OUTPUT_FILE

    def print_output(self) -> None:
        try:
            with open(Maze.get_output_file(), "w") as f:
                for height in range(1, self._height + 1):
                    for width in range(1, self._width + 1):
                        f.write(str(format(self._cells[(width, height)]._state,
                                           'x')) + " ")  # DELETE THE ' '
                    f.write("\n")
                f.write("\n")
                f.write(f"Entry point: ({self._entry[0]}, {self._entry[1]})\n")
                f.write(f"Exit point: ({self._exit[0]}, {self._exit[1]})\n")
                f.write("Player's position: "
                        f"{self.get_player_coordinates()}\n")
                f.write("Pathway----------------------\n")
                for key, value in self._pathway.items():
                    f.write(f"{key}: {value} | ")
        except FileNotFoundError:
            # This error should never happen, since open with 'w' doesn't raise
            # FileNotFoundError, it creates it in case it doesn't exist.
            # But just in case ...
            print("ERROR: output file not found")

    # RANDOM GENERATION ALGORITHM ---------------------------------------------
    def random_generation(self):
        def reset_directions() -> list[str]:
            """
            Function used to get all the possible directions.

            :return: A list with all the directions NORTH, EAST,
            SOUTH, WEST
            :rtype: list[str]
            """
            return [NORTH, EAST, SOUTH, WEST]

        passed_cells: dict[int, tuple[int, int]] = {}
        i = 0
        player = self.get_player()
        player_cell = player.get_cell()
        directions = reset_directions()
        player_cell.set_visited(True)
        passed_cells[i] = self.get_player_coordinates()
        i += 1
        # WITH THIS CODE WE GENERATE ALL THE MAZE WAYS
        while True:
            # Printing passed cells
            # print("-------------")
            # for move, cell in passed_cells.items():
            #     print(f"Move num: {move}\nCell coords: {cell}")

            # Algorithm...
            direction = random.choice(directions)
            player = self.get_player()
            player_cell = player.get_cell()
            adyacent = player_cell.get_adyacent()[direction]
            # print("===============")
            # print("PLAYER'S POSITION:", self.get_cell_position(player_cell))
            # print("Cell at " + direction + ":", adyacent)
            # Uncomment to see process
            # if adyacent is not None:
            #     print("Visited?", adyacent.is_visited())
            #     print("Coordinates:", self.get_cell_position(adyacent))
            #     print(f"Is {direction} fixed?", adyacent.is_fixed())
            #     print(f"Is {direction} visited?", adyacent.is_visited())
            if (adyacent is not None and
                    not adyacent.is_visited() and not adyacent.is_fixed()):
                player_cell.open_direction(direction)
                move = self.move_player(direction)
                # print("Did we move? ", move)
                if move:
                    player = self.get_player()
                    player_cell = player.get_cell()
                    player_cell.set_visited(True)
                    passed_cells[i] = self.get_player_coordinates()
                    if self.get_player_coordinates() == self.get_exit():
                        self._pathway = passed_cells.copy()
                    i += 1
                    directions = reset_directions()
            elif player.can_go_somewhere():
                directions.remove(direction)
                continue
            elif len(passed_cells) > 1:
                self.put_player_at(passed_cells[i - 2])
                i -= 1
                passed_cells.pop(i)
                directions = reset_directions()
            else:
                break

    def open_random_walls(self):
        for cell in self._cells.values():
            if random.randrange(0, 20) == 0:
                open = True
            else:
                open = False
            if open:
                direction = random.choice(POSSIBLE_DIRECTIONS)
                if (cell._adyacent[direction] and
                        not cell._adyacent[direction].is_fixed()):
                    cell.open_direction(direction)

    # PATHFINDER --------------------------------------------------------------
    def find_pathways(self) -> set[dict[int, tuple[int, int]]]:
        def reset_directions() -> list[str]:
            """
            Function used to get all the possible directions.

            :return: A list with all the directions NORTH, EAST,
            SOUTH, WEST
            :rtype: list[str]
            """
            return [NORTH, EAST, SOUTH, WEST]
        self.__reset_cells()
        paths: set[dict[int, tuple[int, int]]] = set()
        passed_cells: dict[int, tuple[int, int]] = {}
        i = 0
        player = self.get_player()
        player_cell = player.get_cell()
        directions = reset_directions()
        player_cell.set_visited(True)
        passed_cells[i] = self.get_player_coordinates()
        back_counter = 0
        removed_cells: list[Cell] = []
        i += 1
        while True:
            print(back_counter)
            print(removed_cells)
            print()
            direction = random.choice(directions)
            player = self.get_player()
            player_cell = player.get_cell()
            adyacent = player_cell.get_adyacent()[direction]
            if (adyacent is not None and not adyacent.is_visited()):
                move = self.move_player(direction)
            else:
                move = False
            if move:
                back_counter = 0
                removed_cells.clear()
                directions = reset_directions()
                player = self.get_player()
                player_cell = player.get_cell()
                player_cell.set_visited(True)
                passed_cells[i] = self.get_player_coordinates()
                if self.get_player_coordinates() == self.get_exit():
                    print("EXIT COORDS:", self._exit)
                    print("PATHWAY FOUND")
                    paths.add(tuple(passed_cells.values()))
                    self.put_player_at(i - 1)
                i += 1
            elif player.can_move_somewhere():
                directions.remove(direction)
                continue
            elif len(passed_cells) > 1:
                back_counter += 1
                if back_counter > 1:
                    removed_cells[0].set_visited(False)
                    removed_cells.pop(0)
                i -= 1
                self.put_player_at(passed_cells[i - 1])
                deleted_cell = self.get_cell(passed_cells.pop(i))
                removed_cells.append(deleted_cell)
                directions = reset_directions()
            else:
                break
        return paths


if __name__ == "__main__":
    # Generating a new perfect maze
    print("\nGenerating a new perfect maze...")
    try:
        maze = Maze(20, 20, (1, 1), (20, 20))
    except MazeError as e:
        print("ERROR:", e)
        sys.exit(1)
    maze.random_generation()
    maze.print_output()
    maze.open_random_walls()
    print(maze.find_pathways())
