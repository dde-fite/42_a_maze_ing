# Delete this file

# If you want all the classes from the package:
import generator as gen

# If you only want one specific class:
# from generator import Maze


maze = gen.Maze(20, 10, (4, 4), (6, 6))
maze.random_generation()
maze.print_output()
