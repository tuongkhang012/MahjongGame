from utils.enums import CallType, TileSource
from components.entities.buttons.tile import Tile
import typing
from mahjong.meld import Meld
from utils.helper import map_call_type_to_meld_type


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
        """
        Initialize a Call object representing a Mahjong call (naki).
        :param type: The type of call (CallType).
        :param tiles: The list of tiles involved in the call.
        :param current_player_idx: The index of the current player making the call.
        :param from_player_idx: The index of the player from whom the tile is taken. (Absolute index)
        :param is_kakan: Indicates if the call is a kakan (added kan).
        """
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
                    # Ankan
                    self.is_opened = False

                # Minkan
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
                        f"Wrong Pon format! The tiles are {list(map(lambda tile: tile.__str__(True), tiles))} which are not the correct for Pon"
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
        self.from_who = (from_player_idx - current_player_idx) % 4
        self.who = current_player_idx
        self.another_player_tiles = self.__get_another_player_tile(tiles)
        self.meld = Meld(
            meld_type=map_call_type_to_meld_type(type),
            tiles=list(map(lambda tile: tile.hand136_idx, tiles)),
            called_tile=self.another_player_tiles if self.is_opened else None,
            opened=self.is_opened,
            who=current_player_idx,
            from_who=(from_player_idx - current_player_idx) % 4, # Relative index
        )
        self.is_kakan = is_kakan

    @staticmethod
    def __rearrange_list(tiles: list[Tile], position: int) -> list[Tile]:
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

    @staticmethod
    def __check_having_another_player_tile(tiles: list[Tile]) -> bool:
        """
        Check if there is exactly one tile taken from another player in the call.
        :param tiles: The list of tiles in the call.
        :return: True if there is exactly one tile taken from another player, False otherwise.
        """
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

    @staticmethod
    def __check_having_same_amount_of_tiles(
        tiles: list[Tile], number: int
    ) -> bool:
        """
        Check if all tiles have the same type and number, and the amount of tiles is equal to the given number.
        :param tiles: The list of tiles to check.
        :param number: The required number of tiles.
        :return: True if all tiles have the same type and number,
        and the amount of tiles is equal to the given number, False otherwise.
        """
        return len(tiles) == number and all(
            tile.type == tiles[0].type and tile.number == tiles[0].number
            for tile in tiles
        )

    @staticmethod
    def __check_consecutive_numbers(tiles: list[Tile]) -> bool:
        """
        Check if the tiles have consecutive numbers.
        :param tiles: The list of tiles to check.
        :return: True if the tiles have consecutive numbers, False otherwise.
        """
        return all(
            tiles[i].number - tiles[i - 1].number == 1 for i in range(1, len(tiles))
        )

    @staticmethod
    def __get_another_player_tile(tiles: list[Tile]) -> Tile | None:
        """
        Get the tile taken from another player in the call.
        :param tiles: The list of tiles in the call.
        :return: The tile taken from another player, or None if not found.
        :rtype: Tile | None
        """
        try:
            return list(filter(lambda tile: tile.source == TileSource.PLAYER, tiles))[0]
        except:
            return None
