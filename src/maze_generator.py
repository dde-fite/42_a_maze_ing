#!/bin/env python3

# QUICK EXAMPLE TO SEE THE GENERATION OF A RANDOM MAZE WITH THE MAZE CLASS

from maze_class import Maze
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
