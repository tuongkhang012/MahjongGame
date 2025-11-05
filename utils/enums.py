from enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class TilesType(Enum):
    MAN = 1
    SOU = 2
    PIN = 3
    WIND = 4
    DRAGON = 5
    AKA = 6
