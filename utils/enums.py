from enum import Enum


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


class TileType(Enum):
    MAN = 0
    PIN = 1
    SOU = 2
    WIND = 3
    DRAGON = 4


class TileSource(Enum):
    DRAW = 0
    PLAYER = 1


class CallType(Enum):
    TSUMO = 0
    RON = 1
    KAN = 2
    PON = 3
    CHII = 4
    SKIP = 5


class CallName(Enum):
    """
    Name of call (naki) for easier definition
    - CHII: chii
    - PON: pon
    - DAMINKAN: Daminkan
    - ANKAN: ankan
    - KAKAN: kakan (shouminkan)
    - AGARI: agari
    - RON: ron
    """

    CHII = "chii"
    PON = "pon"
    DAMINKAN = "damikan"
    ANKAN = "ankan"
    KAKAN = "kakan"
    AGARI = "agari"
    RON = "ron"


class ActionType(Enum):
    TSUMO = 0
    RON = 1
    KAN = 2
    PON = 3
    CHII = 4
    SKIP = 5
    DRAW = 6
    DISCARD = 7
