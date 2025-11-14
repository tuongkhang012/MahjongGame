from utils.enums import CallType
from components.buttons.tile import Tile
import typing

if typing.TYPE_CHECKING:
    from components.player import Player


class Call:
    type: CallType
    tiles: list[Tile]
    player: "Player"

    def __init__(self, type: CallType, tiles: list[Tile]):
        tiles.sort(key=lambda tile: (tile.type.value, tile.number))
        first_tile = tiles[0]
        match type:
            case CallType.RON:
                pass
            case CallType.KAN:
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
            case CallType.PON:
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
            case CallType.CHII:
                if not (
                    len(tiles) == 3
                    and tiles[0].number + 1 == tiles[1].number
                    and tiles[0].number + 2 == tiles[2].number
                    and tiles[0].type == tiles[1].type == tiles[2].type
                ):
                    raise ValueError(
                        f"Wrong Chii format! The tiles are {tiles} which are not the correct for Chii"
                    )
