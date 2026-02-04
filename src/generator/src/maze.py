#!/bin/env python3

from .exceptions import MazeError
from .player import Player
from .cell import Cell
from typing import Union
import threading

# Other imports...
from math import ceil
from random import choice, randrange, random
from typing import Optional
import sys


NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"
POSSIBLE_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
OPPOSITE_DIRECTIONS = {NORTH: SOUTH, EAST: WEST,
                       SOUTH: NORTH, WEST: EAST}


class Maze:

    OUTPUT_FILE = "maze.txt"

    CLOSE_WALLS = {NORTH: 0b0001, EAST: 0b0010,
                   SOUTH: 0b0100, WEST: 0b1000}

    MIN_FT_WIDTH = 9
    MIN_FT_HEIGHT = 7

    WALL_OPENING_CHANCE = 1 / 100
    PATH_ATTEMPTS = 5

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 ft_logo: bool = True, perfect: bool = True) -> None:
        self.set_width(width)
        self.set_height(height)
        self._ft_logo = ft_logo
        self._perfect = perfect
        self._cells: dict[tuple[int, int], Cell] = {}
        self.initiate_cells()
        self.set_entry(entry)
        self.set_exit(exit)
        self._player = Player(self._cells[entry])
        self._pathway: list[tuple[int, int]] = {}
        self._possible_pathways: list[tuple[int, int]] = []

        # Generating cells with the algorithm in the Generator class
        cell_generation, self._pathway = Generator.dfs_generation(
            self._width, self._height, self._entry, self._exit, self._ft_logo)

        # If not perfect:
        if not self._perfect:

            # Open walls
            cell_generation = Generator.open_random_walls(
                cell_generation, self._width, self._height)

            # Find paths
            # threads: list[threading.Thread] = []
            # for _ in range(0, Maze.PATH_ATTEMPTS):
            #     threads.append(threading.Thread(
            #         target=Generator.path_finder,
            #         args=(self._width, self._height,
            #               self._entry, self._exit,
            #               cell_generation)))
            # for t in threads:
            #     t.start()
            # for t in threads:
            #     t.join()
            self._possible_pathways = Generator.path_finder(
                self._width, self._height,
                self._entry, self._exit,
                cell_generation)
            # self._possible_pathways = Generator.PATHS

        # Stablishing the values for each cell
        for y in range(1, self._height + 1):
            for x in range(1, self._width + 1):
                cell_generated = cell_generation[x, y]
                self._cells[x, y].set_state(cell_generated["state"])
                # self._cells[x, y].set_visited(cell_generated["visited"])
                self._cells[x, y].set_fixed(cell_generated["fixed"])

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
        if self._cells[entry]._fixed:
            raise MazeError("ENTRY point is in a protected cell!")
        self._entry = entry

    def get_entry(self) -> tuple[int, int]:
        return self._entry

    # EXIT --------------------------------------------------------------------
    def set_exit(self, exit: tuple[int, int]) -> None:
        if exit[0] < 1 or exit[0] > self._width:
            raise MazeError("EXIT point is not inside the maze!")
        if exit[1] < 1 or exit[1] > self._height:
            raise MazeError("EXIT point is not inside the maze!")
        if self._cells[exit]._fixed:
            raise MazeError("EXIT point is in a protected cell!")
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
        ft_logo: tuple[tuple[int, int]] = (  # type: ignore
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
        if self._ft_logo:
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

    # PATHFINDER --------------------------------------------------------------
    def get_shortest_path(self) -> Optional[list[tuple[int, int]]]:
        if len(self._possible_pathways) > 0:
            return min(self._possible_pathways, key=len)
        return None

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
                f.write("Original Pathway----------------------\n")
                for coord in self._pathway:
                    f.write(f"{coord} | ")
                f.write("\n")
                f.write("Pathways found------------------------\n")
                i = 0
                for path in self._possible_pathways:
                    f.write(f"=== {i} ===\n")
                    for coord in path:
                        f.write(f"{coord} | ")
                    f.write("\n")
                    i += 1
                f.write("Shortest path-------------------------\n")
                shortest_path = self.get_shortest_path()
                if shortest_path:
                    for coord in shortest_path:
                        f.write(f"{coord} | ")
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
            direction = choice(directions)  # From random package
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
                i -= 1
                self.put_player_at(passed_cells[i - 1])
                passed_cells.pop(i)
                directions = reset_directions()
            else:
                break

    # Not finished
    def open_random_walls(self):
        # TODO: DELETE THIS FUNCTION IF NOT NEEDED. DEPRECATED
        for cell in self._cells.values():
            if randrange(0, 5) == 0:
                open = True
            else:
                open = False
            if open:
                direction = choice(POSSIBLE_DIRECTIONS)
                if (cell._adyacent[direction] and
                        not cell._adyacent[direction].is_fixed()):
                    print("Opened", direction)
                    cell.open_direction(direction)


class Generator:
    # TODO: Structure the class methods in a more clear and efficient way

    PATHS = []

    @staticmethod
    def __get_ft_logo_cells(width: int, height: int) -> Optional[
            list[tuple[int, int]]]:
        # TODO: Change the ft_logo related cells for the different sizes!
        if (width < Maze.MIN_FT_WIDTH
                or height < Maze.MIN_FT_HEIGHT):
            return
        SIZE_1 = (Maze.MIN_FT_WIDTH, Maze.MIN_FT_HEIGHT)
        SIZE_2 = (Maze.MIN_FT_WIDTH * 3, Maze.MIN_FT_HEIGHT * 3)
        SIZE_3 = (Maze.MIN_FT_WIDTH * 9, Maze.MIN_FT_HEIGHT * 9)
        # BIGGEST SIZE
        if width > SIZE_3[0] and height > SIZE_3[1]:
            ft_logo: tuple[tuple[int, int]] = (  # type: ignore
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
        # MEDIUM SIZE
        elif width > SIZE_2[0] and height > SIZE_2[1]:
            ft_logo: tuple[tuple[int, int]] = (  # type: ignore
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
        # SMALL SIZE
        elif width > SIZE_1[0] and height > SIZE_1[1]:
            ft_logo: tuple[tuple[int, int]] = (  # type: ignore
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
        else:
            return
        center_point = (ceil(width / 2),
                        ceil(height / 2))
        cells = []
        for cell in ft_logo:
            cells.append((center_point[0] + cell[0],
                         center_point[1] + cell[1]))
        return cells

    @staticmethod
    def __get_adyacent_cells(point: tuple[int, int],
                             width: int, height: int) -> dict[
                               str, Optional[tuple[int, int]]]:
        adyacent_cells = {}
        if point[0] == 1:
            adyacent_cells[WEST] = None
        else:
            adyacent_cells[WEST] = (point[0] - 1, point[1])
        if point[0] == width:
            adyacent_cells[EAST] = None
        else:
            adyacent_cells[EAST] = (point[0] + 1, point[1])
        if point[1] == 1:
            adyacent_cells[NORTH] = None
        else:
            adyacent_cells[NORTH] = (point[0], point[1] - 1)
        if point[1] == height:
            adyacent_cells[SOUTH] = None
        else:
            adyacent_cells[SOUTH] = (point[0], point[1] + 1)
        return adyacent_cells

    @classmethod
    def dfs_generation(cls, width: int, height: int,
                       entry: tuple[int, int],
                       exit: tuple[int, int],
                       ft_logo: bool = True
                       ) -> tuple[dict, list]:
        # dict returned: dict[tuple[int, int], dict[str, Union[int, bool]]]
        # list returned: list[tuple[int, int]]
        # TODO: Try to reduce functions usage and improve dictionary structures

        # Initializing cells
        cells: dict[tuple[int, int], dict[str, Union[int, bool]]] = {}
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                cells[(x, y)] = {"state": 0b1111, "visited": False,
                                 "fixed": False}

        # Stablishing fixed cells
        if ft_logo:
            ft_logo_cells = cls.__get_ft_logo_cells(width, height)
            if ft_logo_cells:
                for cell in ft_logo_cells:
                    cells[cell]["fixed"] = True

        # Initializing other variables
        point = entry
        cells[point]["visited"] = True
        directions = [NORTH, EAST, SOUTH, WEST]
        passed_cells: list[tuple[int, int]] = [point]
        exit_path = []
        op = OPPOSITE_DIRECTIONS

        # Generating full maze
        while True:
            dir = choice(directions)  # From random package

            # Stablishing adyacent
            adyacents = cls.__get_adyacent_cells(point, width, height)
            if adyacents[dir]:
                adyacent = cells[adyacents[dir]]
            else:
                adyacent = None

            # Logic
            if adyacent and not adyacent["visited"] and not adyacent["fixed"]:
                # Changing current cell state
                cells[point]["state"] -= Maze.CLOSE_WALLS[dir]

                # Changing adyacent cell state
                adyacent["state"] -= Maze.CLOSE_WALLS[op[dir]]
                adyacent["visited"] = True

                # Updating variables
                point = adyacents[dir]
                passed_cells.append(point)
                # directions = POSSIBLE_DIRECTIONS.copy()
                directions = [NORTH, EAST, SOUTH, WEST]
                if point == exit:
                    exit_path = passed_cells.copy()
            else:
                # Not being able to move that direction
                directions.remove(dir)
            if point == entry and len(directions) == 0:
                # Finishing the algorithm
                break
            if len(directions) == 0:
                # Running out of possible directions
                point = passed_cells[-2]
                if len(passed_cells) > 0:
                    passed_cells.pop()  # Deleting last
                # directions = POSSIBLE_DIRECTIONS.copy()
                directions = [NORTH, EAST, SOUTH, WEST]
        return (cells, exit_path)

    @classmethod
    def path_finder_mutex(cls, width: int, height: int,
                          entry: tuple[int, int], exit: tuple[int, int],
                          cells:
                          dict[tuple[int, int], dict[
                          str, Union[int, bool]]]) -> list[tuple[int, int]]:
        mutex = threading.Lock()

        points = []
        point = entry
        points.append(point)

        directions = [NORTH, EAST, SOUTH, WEST]
        pathways = []
        passed_cells = [point]
        wrong_cells: list[tuple[int, int]] = []

        # while attempts < Maze.PATH_ATTEMPTS:
        while True:
            dir = choice(directions)

            # Stablishing adyacent
            adyacents = cls.__get_adyacent_cells(point, width, height)
            if adyacents[dir]:
                adyacent = cells[adyacents[dir]]
            else:
                adyacent = None

            # Checking if we can move that direction
            if adyacent is None:
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            elif cells[point]["state"] & Maze.CLOSE_WALLS[dir]:
                # We can't
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            elif (adyacents[dir] in passed_cells or
                    adyacents[dir] in wrong_cells):
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            else:
                point = adyacents[dir]
                passed_cells.append(point)
                directions = [NORTH, EAST, SOUTH, WEST]
                if point == exit:
                    with mutex:
                        print("Hilo iniciado")
                        # if passed_cells not in pathways:
                        if passed_cells not in cls.PATHS:
                            pathways.append(passed_cells.copy())
                            cls.PATHS.append(passed_cells)
                        # print(f"Attempt {attempts}:", passed_cells)
                    break
                    # attempts += 1
                    # point = entry
                    # passed_cells.clear()
                    # passed_cells.append(point)
        # print(pathways)
        return pathways

    @classmethod
    def path_finder(cls, width: int, height: int,
                    entry: tuple[int, int], exit: tuple[int, int],
                    cells:
                    dict[tuple[int, int], dict[
                        str, Union[int, bool]]]) -> list[tuple[int, int]]:
        attempts = 0
        points = []
        point = entry
        points.append(point)

        directions = [NORTH, EAST, SOUTH, WEST]
        pathways = []
        passed_cells = [point]
        wrong_cells: list[tuple[int, int]] = []

        while attempts < Maze.PATH_ATTEMPTS:
            dir = choice(directions)

            # Stablishing adyacent
            adyacents = cls.__get_adyacent_cells(point, width, height)
            if adyacents[dir]:
                adyacent = cells[adyacents[dir]]
            else:
                adyacent = None

            # Checking if we can move that direction
            if adyacent is None:
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            elif cells[point]["state"] & Maze.CLOSE_WALLS[dir]:
                # We can't
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            elif (adyacents[dir] in passed_cells or
                    adyacents[dir] in wrong_cells):
                directions.remove(dir)
                if len(directions) == 0:
                    directions = [NORTH, EAST, SOUTH, WEST]
                    point = passed_cells[-2]
                    wrong_cells.append(passed_cells[-1])
                    passed_cells.pop()
            else:
                point = adyacents[dir]
                passed_cells.append(point)
                directions = [NORTH, EAST, SOUTH, WEST]
                if point == exit:
                    if passed_cells not in pathways:
                        pathways.append(passed_cells.copy())
                    # print(f"Attempt {attempts}:", passed_cells)
                    attempts += 1
                    point = entry
                    passed_cells.clear()
                    passed_cells.append(point)
        # print(pathways)
        return pathways

    @classmethod
    def open_random_walls(cls, cells: dict[tuple[int, int], dict[
                            str, Union[int, bool]]],
                          width: int,
                          height: int):
        op = OPPOSITE_DIRECTIONS
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if cells[(x, y)]["fixed"]:
                    continue
                dir = choice(POSSIBLE_DIRECTIONS)
                # result = randrange(0, 10)
                # if result == 0:
                if random() < Maze.WALL_OPENING_CHANCE:
                    adyacents = cls.__get_adyacent_cells((x, y), width, height)
                    if (adyacents[dir] and
                            not cells[adyacents[dir]]["fixed"] and
                            cells[(x, y)]["state"] & Maze.CLOSE_WALLS[dir]):
                        # If adyacent exists and has the wall to open:

                        # Changing current cell state
                        cells[(x, y)]["state"] -= Maze.CLOSE_WALLS[dir]

                        # Changing adyacent cell state
                        cells[adyacents[dir]]["state"] -= (
                            Maze.CLOSE_WALLS[op[dir]])
        return cells


if __name__ == "__main__":
    # Generating a new perfect maze
    print("\nGenerating a new perfect maze...")
    try:
        maze = Maze(100, 100, (1, 1), (15, 15))
    except MazeError as e:
        print("ERROR:", e)
        sys.exit(1)
    # maze.random_generation()
    maze.print_output()
