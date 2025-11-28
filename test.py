from enum import Enum

class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __str__(self):
        match self.value:
            case 0:
                return f"East"
            case 1:
                return f"South"
            case 2:
                return f"West"
            case 3:
                return f"North"


class TileType(Enum):
    MAN = 0
    PIN = 1
    SOU = 2
    WIND = 3
    DRAGON = 4

class Tile():
    def __init__(self, type: TileType, number: int, aka: bool = False):
        # Tile standard attributes
        self.type = type
        self.number = number
        self.aka = aka

    def __str__(self, full: bool = False):
        if not full:
            tile_type = None
            match self.type:
                case TileType.SOU:
                    tile_type = "s"
                case TileType.PIN:
                    tile_type = "p"
                case TileType.MAN:
                    tile_type = "m"
                case TileType.DRAGON:
                    if self.number == 1:
                        return "P"
                    elif self.number == 2:
                        return "F"
                    elif self.number == 3:
                        return "C"
                case TileType.WIND:
                    if self.number == 1:
                        return "E"
                    elif self.number == 2:
                        return "S"
                    elif self.number == 3:
                        return "W"
                    elif self.number == 4:
                        return "N"
            return f"{self.number}{tile_type}{'r' if self.aka else ''}"

        return f"{self.type} {self.number}"

TILES = [
    *(f"{n}m" for n in range(1, 10)),
    *(f"{n}p" for n in range(1, 10)),
    *(f"{n}s" for n in range(1, 10)),
    "E", "S", "W", "N", "P", "F", "C"
]
TILE_IDX = {tile: idx for idx, tile in enumerate(TILES)}

print(Tile(TileType.WIND, 1))
print(TILE_IDX[str(Tile(TileType.WIND, 1))])