*This project has been created as part of the 42 curriculum by jvizcain, dde-fite*

<p align="center">
    <img align="center" src="media/42_a_maze_ing.jpg">
    <h1 align="center">42_a_maze_ing</h1>
</p>

<p align="center">
    <img alt="Static Badge" src="https://img.shields.io/badge/pending/100-yellow?logo=42&logoColor=white">
</p>

<p align="center">
This work is published under the terms of <a href="LICENSE"><b>MIT license</b></a>
</p>

<div align="center">
    <h2>Maze generator with visualizer built using Python and MiniLibX.</h2>
    <!-- <img src="media/preview.gif"> -->
</div>

## Description

### GENERATION ALGORITHM

Recursive Backtracking is one of the most popular and intuitive algorithms for generating perfect mazes (mazes without loops and with exactly one path between any two cells if it is perfect). It is based on a depth-first search (DFS) strategy and produces long, winding corridors with a natural-looking structure.

### Core Idea

Every cell from the maze starts with all walls closed.
The algorithm explores the maze by:

Starting from the start point cell.

Randomly visiting one of its unvisited neighboring cells.

Removing the wall between the current cell and the chosen neighbor.

Recursively repeating the process from the neighbor.

Backtracking when no unvisited neighbors remain.

This continues until all cells have been visited.

### Step-by-Step Algorithm

1. **Initialize the grid**.

    Create a grid where each cell is surrounded by walls.

    Mark all cells as unvisited.

    Choose a starting cell (starting point can be used).

    Mark it as visited.

    Add this cell to the list of visited cells.

2. **If the current cell has unvisited neighbors**:

    Randomly select one.

    Remove the wall between the current cell and the chosen neighbor.

    Mark the neighbor as visited.

    Push the current cell onto the stack.

    Move to the neighbor.

3. **Otherwise**:

    Pop the last cell of the list of visited cells (backtrack).

    The current cell will now be the previous one.

The algorithm ends when the current point is the starting point and there is no possible way to move to (meaning that all cells were already visited).

## Instructions

## Resources

We used the example of this page to understand how the algorithm used for the generation works:

https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking