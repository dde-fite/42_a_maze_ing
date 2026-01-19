#!/bin/env python3

# QUICK EXAMPLE TO SEE THE GENERATION OF A RANDOM MAZE WITH THE MAZE CLASS
from maze_class import Maze, POSSIBLE_DIRECTIONS, print_output
import random


def can_go_somewhere(maze: Maze) -> bool:
    for dir in POSSIBLE_DIRECTIONS:
        # print(f"Checking if we can go {dir}...")
        adyacent = maze.get_player().get_cell().get_adyacent()[dir]
        if (adyacent is not None and adyacent.is_visited() is False and
                adyacent.is_fixed() is False):
            # print(f"WE CAN GO {dir}")
            return True
    print("Can't go anywhere :(")
    return False


if __name__ == "__main__":
    # Generating a new perfect maze
    print("\nGenerating a new perfect maze...")
    maze = Maze(20, 20, (2, 2), (5, 4))
    maze.put_player_at((1, 1))
    passed_cells: dict[int, tuple[int, int]] = {}
    i = 0
    player = maze.get_player()
    player_cell = player.get_cell()
    # WITH THIS CODE WE GENERATE ALL THE MAZE WAYS
    while True:
        # Printing passed cells
        print("-------------")
        for move, cell in passed_cells.items():
            print(f"Move num: {move}\nCell coords: {cell}")
        # Algorithm...
        direction = random.choice(POSSIBLE_DIRECTIONS)
        player = maze.get_player()
        player_cell = player.get_cell()
        adyacent = player_cell.get_adyacent()[direction]
        print("===============")
        print("PLAYER'S POSITION:", maze.get_cell_position(player_cell))
        print("Cell at " + direction + ":", adyacent)
        # Uncomment to see process
        # if adyacent is not None:
        #     print("Visited?", adyacent.is_visited())
        #     print("Coordinates:", maze.get_cell_position(adyacent))
        #     print(f"Is {direction} fixed?", adyacent.is_fixed())
        #     print(f"Is {direction} visited?", adyacent.is_visited())
        if (adyacent is not None and
                not adyacent.is_visited() and not adyacent.is_fixed()):
            player_cell.open_direction(direction)
            move = maze.move_player(direction)
            print("Did we move? ", move)
            if move:
                player = maze.get_player()
                player_cell = player.get_cell()
                player_cell.set_visited(True)
            passed_cells[i] = maze.get_player_coordinates()
            i += 1
        elif can_go_somewhere(maze):
            continue
        elif len(passed_cells) > 1:
            maze.put_player_at(passed_cells[i - 2])
            i -= 1
            passed_cells.pop(i)
        else:
            break
    print_output(maze)
