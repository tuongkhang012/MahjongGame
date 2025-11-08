from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class TileType(Enum):
    MAN = 0
    SOU = 1
    PIN = 2
    WIND = 3
    DRAGON = 4


class TileSource(Enum):
    DRAW = 0
    PLAYER = 1


class CallType(Enum):
    RON = 0
    KAN = 1
    PON = 2
    CHI = 3
