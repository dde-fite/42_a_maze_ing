#!/bin/env python3

if __name__ == "__main__":
    config_file = "config.txt"
    try:
        with open(config_file, "r") as f:
            config_file = f.readline()
            while (config_file):
                pass  # Do some logic like we did with gnl
    except FileNotFoundError:
        print("File was not found")
