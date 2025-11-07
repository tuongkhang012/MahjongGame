from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class TilesType(Enum):
    MAN = 0
    SOU = 1
    PIN = 2
    WIND = 3
    DRAGON = 4


class CallType(Enum):
    Ron = 0
    Kan = 1
    Pon = 2
    Chi = 3
