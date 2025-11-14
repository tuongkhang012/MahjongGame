from enum import Enum


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


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
    CHII = 3
    SKIP = 4


class ActionType(Enum):
    RON = 0
    KAN = 1
    PON = 2
    CHII = 3
    SKIP = 4
    DISCARD = 5
