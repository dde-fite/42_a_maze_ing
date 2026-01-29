#!/bin/env python3

from .src import Maze, Cell, Player, MazeError


# So flake8 doesn't cry
if __name__ == "__main__":
    print(Maze.__name__)
    print(Cell.__name__)
    print(Player.__name__)
    print(MazeError.__name__)
