from utils.enums import CallType
from components.tile import Tile


class Call:
    type: CallType
    tiles: list[Tile]

    def __init__(self, type: CallType, tiles: list[Tile]):
        tiles.sort(key=lambda tile: (tile.type.value, tile.number))
        first_tile = tiles[0]
        match type:
            case CallType.Ron:
                pass
            case CallType.Kan:
                if (
                    len(
                        list(
                            filter(
                                lambda tile: tile.number == first_tile.number
                                and tile.type == first_tile.type,
                                tiles,
                            )
                        )
                    )
                    != len(tiles)
                    != 4
                ):
                    raise ValueError(
                        f"Wrong Kan format! The tiles are {tiles} which are not the correct for Kan"
                    )
            case CallType.Pon:
                if (
                    len(
                        list(
                            filter(
                                lambda tile: tile.number == first_tile.number
                                and tile.type == first_tile.type,
                                tiles,
                            )
                        )
                    )
                    != len(tiles)
                    != 3
                ):
                    raise ValueError(
                        f"Wrong Pon format! The tiles are {tiles} which are not the correct for Pon"
                    )
            case CallType.Chi:
                if not (
                    len(tiles) == 3
                    and tiles[0].number + 1 == tiles[1].number
                    and tiles[0].number + 2 == tiles[2].number
                    and tiles[0].type == tiles[1].type == tiles[2].type
                ):
                    raise ValueError(
                        f"Wrong Chi format! The tiles are {tiles} which are not the correct for Chi"
                    )
