#!/bin/env python3

from .types import Coords


class Player:

    def __init__(self, coords: Coords) -> None:
        self._coords = coords

    def get_coordinates(self) -> Coords:
        return self._coords

    def set_coordinates(self, coords: Coords) -> None:
        self._coords = coords


if __name__ == "__main__":
    player = Player((12, 10))
    print(player.get_coordinates())
