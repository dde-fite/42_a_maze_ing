#!/bin/env python3

# QUICK EXAMPLE TO SEE THE GENERATION OF A RANDOM MAZE WITH THE MAZE CLASS

from maze_class import Maze, Cell, POSSIBLE_DIRECTIONS, print_output
import random


# This function is just for some testing,
# returns a tuple with all the possible byte combinations.
def get_possible_wall_combinations() -> tuple[int]:
    north_close = {0b0001, 0b0011, 0b0101, 0b1001,
                   0b0111, 0b1011, 0b1101, 0b1111}
    east_close = {0b0010, 0b0011, 0b0110, 0b1010,
                  0b0111, 0b1011, 0b1110, 0b1111}
    south_close = {0b0100, 0b0101, 0b0110, 0b1100,
                   0b0111, 0b1110, 0b1101, 0b1111}
    west_close = {0b1000, 0b1001, 0b1010, 0b1100,
                  0b1011, 0b1101, 0b1110, 0b1111}
    all_close = {0b1111}
    all_open = {0b0000}
    return tuple(north_close.union(east_close, south_close, west_close,
                                   all_close, all_open))


# Returns a maze dictionary (coordinates: byte combination),
# with the byte combination being random
def get_maze_dict(maze: Maze) -> dict[tuple[int, int]: int]:
    maze_dict = {}
    combinations = get_possible_wall_combinations()
    for height in range(1, maze.get_height() + 1):
        for width in range(1, maze.get_width() + 1):
            maze_dict.update({(height, width): random.choice(combinations)})
    return maze_dict


def can_go_somewhere(maze: Maze) -> bool:
    for dir in POSSIBLE_DIRECTIONS:
        print(f"Checking if we can go {dir}...")
        adyacent = maze.get_player().get_cell().get_adyacent()[dir]
        if adyacent is not None and not adyacent.is_visited():
            print(f"WE CAN GO {dir}")
            return True
    print("Can't go anywhere :(")
    return False


if __name__ == "__main__":
    maze = Maze(20, 20, (1, 1), (20, 20))
    maze_dict = get_maze_dict(maze)

    print("Printing random maze generated (coordinates: wall value):",
          maze_dict)
    print("Printing possible wall combination values (not hex):",
          get_possible_wall_combinations())
    try:
        with open(Maze.get_output_file(), "w") as f:
            for height in range(1, maze.get_height() + 1):
                for width in range(1, maze.get_width() + 1):
                    f.write(str(format(maze_dict[(height, width)], 'x')))
                f.write("\n")
    except FileNotFoundError:
        # This error should never happen, since open with 'w' doesn't raise
        # FileNotFoundError, it creates it in case it doesn't exist.
        # But just in case ...
        print("ERROR: output file not found")

    # Generating a new perfect maze
    print("\nGenerating a new perfect maze...")
    maze = Maze(5, 5, (2, 2), (5, 4))
    maze.put_player_at((1, 1))
    passed_cells: dict[int, tuple[int, int]] = {}
    i = 0
    while True:
        direction = random.choice(POSSIBLE_DIRECTIONS)
        print("===============")
        print(i)
        print("Cell at " + direction + ":", maze.get_player().get_cell().get_adyacent()[direction])
        if maze.get_player().get_cell().get_adyacent()[direction] is not None:
            print("Visited?", maze.get_player().get_cell().get_adyacent()[direction].is_visited())
            print("Coordinates:", maze.get_cell_position(maze.get_player().get_cell().get_adyacent()[direction]))
        if (maze.get_player().get_cell().get_adyacent()[direction] is not None and
                not maze.get_player().get_cell().get_adyacent()[direction].is_visited()):
            maze.get_player().get_cell().open_direction(direction)
            print("Did we move? ", maze.move_player(direction))
            maze.get_player().get_cell().set_visited(True)
            passed_cells[i] = maze.get_player_coordinates()
            i += 1
        elif can_go_somewhere(maze):
            continue
        elif i > 0:
            i -= 1
            maze.put_player_at(passed_cells[i])
        else:
            break
    print_output(maze)
