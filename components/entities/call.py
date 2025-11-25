from utils.enums import CallType, TileSource, CallName
from components.entities.buttons.tile import Tile
import typing
from mahjong.meld import Meld
from utils.helper import map_call_type_to_meld_type

if typing.TYPE_CHECKING:
    from components.entities.player import Player


class Call:
    type: CallType
    tiles: list[Tile]
    meld: Meld
    is_opened: bool = True
    is_kakan: bool = False

    def __init__(
        self,
        type: CallType,
        tiles: list[Tile],
        current_player_idx: int,
        from_player_idx: int,
        is_kakan: bool = False,
    ):
        tiles.sort(key=lambda tile: (tile.type.value, tile.number))
        self.is_opened = True
        match type:
            case CallType.RON:
                print("INIT CALL FOR RON")
                pass
            case CallType.KAN:
                print("INIT CALL FOR KAN")
                if not self.__check_having_same_amount_of_tiles(tiles, 4):
                    raise ValueError(
                        f"Wrong Kan format! The tiles are {list(map(lambda tile: tile.__str__(), tiles))} which are not the correct for Kan"
                    )
                if current_player_idx == from_player_idx and not is_kakan:
                    self.is_opened = False
                match (current_player_idx - from_player_idx) % 4:
                    case 1:
                        tiles = self.__rearrange_list(tiles, 0)
                    case 2:
                        tiles = self.__rearrange_list(tiles, 1)
                    case 3:
                        tiles = self.__rearrange_list(tiles, len(tiles))
            case CallType.PON:
                print("INIT CALL FOR PON")
                if not (
                    self.__check_having_another_player_tile(tiles)
                    and self.__check_having_same_amount_of_tiles(tiles, 3)
                ):
                    raise ValueError(
                        f"Wrong Pon format! The tiles are {list(map(lambda tile: tile.__str__(), tiles))} which are not the correct for Pon"
                    )
                match (current_player_idx - from_player_idx) % 4:
                    case 1:
                        tiles = self.__rearrange_list(tiles, 0)
                    case 2:
                        tiles = self.__rearrange_list(tiles, 1)
                    case 3:
                        tiles = self.__rearrange_list(tiles, len(tiles))
            case CallType.CHII:
                print("INIT CALL FOR CHII")
                if not (
                    self.__check_consecutive_numbers(tiles)
                    and self.__check_having_another_player_tile(tiles)
                ):

                    raise ValueError(
                        f"Wrong Chii format! The tiles are {list(map(lambda tile: tile.__str__(), tiles))} which are not the correct for Chii"
                    )
                tiles = self.__rearrange_list(tiles, 0)

        self.type = type
        self.tiles = tiles
        self.from_who = from_player_idx
        self.who = current_player_idx
        self.another_player_tiles = self.__get_another_player_tile(tiles)
        self.meld = Meld(
            meld_type=map_call_type_to_meld_type(type),
            tiles=list(map(lambda tile: tile.hand136_idx, tiles)),
            called_tile=self.another_player_tiles if self.is_opened else None,
            opened=self.is_opened,
            who=current_player_idx,
            from_who=(from_player_idx - current_player_idx + 4) % 4,
        )
        self.is_kakan = is_kakan

    def __rearrange_list(self, tiles: list[Tile], position: int) -> list[Tile]:
        """
        Rearrage list of tile to make the another tile from another player insert to corresponding position
        """
        try:
            another_player_tile = list(
                filter(lambda tile: tile.source == TileSource.PLAYER, tiles)
            )[0]
            remaining_tile = list(
                filter(lambda tile: tile.source == TileSource.DRAW, tiles)
            )
            remaining_tile.sort(key=lambda tile: (tile.type.value, tile.number))
            remaining_tile.insert(position, another_player_tile)
            return remaining_tile

        except:
            tiles_list = list(
                filter(lambda tile: tile.source == TileSource.DRAW, tiles)
            )
            tiles_list.sort(key=lambda tile: (tile.type.value, tile.number))
            return tiles_list

    def __check_having_another_player_tile(self, tiles: list[Tile]) -> bool:
        number_of_tiles_from_another_player = len(
            list(filter(lambda tile: tile.source == TileSource.PLAYER, tiles))
        )
        if number_of_tiles_from_another_player > 1:
            raise ValueError(
                "The number of tiles can take from another player when calling must be below 1!"
            )

        if number_of_tiles_from_another_player == 0:
            return False

        return True

    def __check_having_same_amount_of_tiles(
        self, tiles: list[Tile], number: int
    ) -> bool:
        return len(tiles) == number and all(
            tile.type == tiles[0].type and tile.number == tiles[0].number
            for tile in tiles
        )

    def __check_consecutive_numbers(self, tiles: list[Tile]) -> bool:
        return all(
            tiles[i].number - tiles[i - 1].number == 1 for i in range(1, len(tiles))
        )

    def __get_another_player_tile(self, tiles: list[Tile]) -> Tile | None:
        try:
            return list(filter(lambda tile: tile.source == TileSource.PLAYER, tiles))[0]
        except:
            return None
