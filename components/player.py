from components.buttons.tile import Tile
from components.call import Call
from utils.enums import CallType, TileSource, TileType, ActionType
from pygame import Surface
import typing
from utils.enums import Direction
from components.fields.discard_field import DiscardField
from components.fields.deck_field import DeckField
from components.fields.call_field import CallField
from utils.helper import (
    map_call_to_action,
    convert_tile_to_hand34_index,
    convert_tiles_list_to_hand34,
    convert_tiles_list_to_hand136,
    map_call_type_to_meld_type,
)

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
from mahjong.shanten import Shanten

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class Player:
    player_idx: int
    player_deck: list[Tile]
    discard_tiles: list[Tile]
    call_list: list[Call]
    direction: Direction

    # All fields
    discard_field: DiscardField
    call_field: CallField
    deck_field: DeckField

    # Callable
    can_call: list[CallType]
    callable_tiles_list: list[list[Tile]]
    melds: list[Meld]

    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        direction: Direction,
        full_deck: list[Tile],
        player_deck: list[Tile] = None,
        discard_tiles: list[Tile] = None,
        call_tiles_list: list[Tile] = None,
    ):
        self.player_idx = player_idx
        self.direction = direction

        # Tile deck field init
        self.player_deck = player_deck if player_deck is not None else []
        self.discard_tiles = discard_tiles if discard_tiles is not None else []
        self.__already_discard_tiles: list[Tile] = []
        self.call_tiles_list = call_tiles_list if call_tiles_list is not None else []
        self.call_list: list[Call] = []
        self.discard_field = DiscardField(
            screen, self.player_idx, self.discard_tiles, full_deck
        )
        self.call_field = CallField(
            screen, self.player_idx, self.call_list, self.call_tiles_list, full_deck
        )
        self.deck_field = DeckField(
            screen, self.player_idx, self.player_deck, full_deck
        )

        # Call init
        self.can_call = []
        self.callable_tiles_list = []
        self.melds = []

        # Game properties
        self.__is_riichi = True
        self.__winning_tiles = []
        # Player scores
        self.scores = 25000

    def draw(self, draw_deck: list[Tile], tile: Tile = None):
        if tile:
            self.__draw_tile = tile
            draw_deck.remove(tile)
        else:
            self.__draw_tile = draw_deck.pop()

        self.__draw_tile.source = TileSource.DRAW
        self.player_deck.append(self.__draw_tile)
        self.__draw_tile.update_tile_surface(self.player_idx)
        self.check_call(self.__draw_tile)
        return self.__draw_tile

    def build_chii(self, tile: Tile):
        self.callable_tiles_list = []

        first_tile = self.find_tile(tile.type, tile.number - 2)
        second_tile = self.find_tile(tile.type, tile.number - 1)
        third_tile = self.find_tile(tile.type, tile.number + 1)
        forth_tile = self.find_tile(tile.type, tile.number + 2)
        if first_tile and second_tile:
            self.callable_tiles_list.append([first_tile, second_tile, tile])
        if second_tile and third_tile:
            self.callable_tiles_list.append([second_tile, tile, third_tile])
        if third_tile and forth_tile:
            self.callable_tiles_list.append([tile, third_tile, forth_tile])

    def build_pon(self, tile: Tile):
        self.callable_tiles_list = []

        self.callable_tiles_list.append(
            list(
                filter(
                    lambda player_tile: tile.number == player_tile.number
                    and tile.type == player_tile.type,
                    self.player_deck,
                )
            )[0:2]
            + [tile]
        )

    def build_kan(self, tile: Tile):
        self.callable_tiles_list = []

        if tile.source == TileSource.PLAYER:
            self.callable_tiles_list.append(
                list(
                    filter(
                        lambda player_tile: tile.number == player_tile.number
                        and tile.type == player_tile.type,
                        self.player_deck,
                    )
                )
                + [tile]
            )
        else:
            already_pon_list = list(
                filter(
                    lambda call: call.type == CallType.PON
                    and tile.number == call.tiles[0].number
                    and tile.type == call.tiles[0].type,
                    self.call_list,
                )
            )
            if len(already_pon_list) >= 1:
                for call in self.call_list:
                    if call.type == CallType.PON and all(
                        [
                            called_tile.type == tile.type
                            and called_tile.number == tile.number
                            for called_tile in call.tiles
                        ]
                    ):
                        callable_tiles_list = call.tiles + [tile]
                        self.callable_tiles_list.append(callable_tiles_list)
                        self.call_list.remove(call)
                        del call
                        break

            else:
                self.callable_tiles_list.append(
                    list(
                        filter(
                            lambda player_tile: tile.number == player_tile.number
                            and tile.type == player_tile.type,
                            self.player_deck,
                        )
                    )
                )

    def call(
        self,
        tile: Tile,
        call_list: list[Tile],
        call_type: CallType,
        player: "Player",
    ):
        if player:
            tile.source = TileSource.PLAYER

        print(
            f"Player {self.player_idx} call: {call_type} for {list(map(lambda tile: tile.__str__(),call_list))}"
        )
        if player:
            player.discard_tiles.remove(tile)
            self.player_deck.append(tile)

        # Handle Kakan case
        is_kakan = False

        for tmp_tile in call_list:
            if tmp_tile not in self.player_deck:
                is_kakan = True
            else:
                self.player_deck.remove(tmp_tile)

        self.call_list.append(
            Call(
                call_type,
                call_list,
                self.player_idx,
                player.player_idx if player else self.player_idx,
                is_kakan,
            )
        )
        for called_tile in call_list:
            if called_tile not in self.call_tiles_list:
                self.call_tiles_list.append(tile)

        self.melds.append(self.call_list[-1].meld)

        self.rearrange_deck()
        self.deck_field.build_field_surface(self)
        self.deck_field.build_tiles_position(self)

    def discard(self, tile: Tile = None, game_manager: "GameManager" = None):
        import random

        if tile is None:
            minimum_shanten = 14
            discard_tile = None
            for tile in self.player_deck:
                tmp_tiles_list = self.player_deck.copy()
                tmp_tiles_list.remove(tile)
                if minimum_shanten > self.count_shanten_points(tmp_tiles_list):
                    discard_tile = tile
                    minimum_shanten = self.count_shanten_points(tmp_tiles_list)

            print(
                f"Player {self.player_idx} have {self.count_shanten_points(self.player_deck)} SHANTEN"
            )
            tile = discard_tile

        tile.reveal()
        tile.unclicked()
        self.player_deck.remove(tile)
        self.discard_tiles.append(tile)
        self.__already_discard_tiles.append(tile)
        game_manager.latest_discarded_tile = tile
        game_manager.start_discarded_animation(tile)
        return tile

    def rearrange_deck(self):
        self.player_deck.sort(key=lambda tile: (tile.type.value, tile.number))

    def reveal_hand(self):
        for tile in self.player_deck:
            tile.hidden = False

    def make_move(self, action: ActionType = None) -> ActionType:
        from random import randint

        if action:
            return action

        if len(self.can_call) > 0:
            # return map_call_to_action(self.can_call[randint(0, len(self.can_call) - 1)])
            return map_call_to_action(self.can_call[-1])
        return ActionType.DISCARD

    def get_draw_tile(self) -> Tile:
        return self.__draw_tile

    def total_tiles(self) -> int:
        return len(self.deck_field.get_tiles_list()) + len(
            self.call_field.get_tiles_list()
        )

    def find_tile(self, type: TileType, number: int) -> Tile | None:
        try:
            return list(
                filter(
                    lambda tile: tile.type == type and tile.number == number,
                    self.player_deck,
                )
            )[0]
        except:
            return None

    def check_call(self, tile: Tile, check_chii: bool = False):
        print("----- Start cheking call -----")
        self.can_call = []

        self.__build_winning_tiles()
        if self.is_tsumo_able():
            self.can_call.append(CallType.TSUMO)

        if self.is_ron_able(tile):
            self.can_call.append(CallType.RON)

        if self.is_kan_able(tile):
            self.can_call.append(CallType.KAN)

        if self.is_pon_able(tile):
            self.can_call.append(CallType.PON)

        if self.is_chii_able(tile) and check_chii:
            self.can_call.append(CallType.CHII)

        if len(self.can_call) > 0:
            self.can_call.append(CallType.SKIP)

        print(f"Player {self.player_idx} calling: {self.can_call}")
        print("----- Done checking call -----")

    def __build_winning_tiles(self):
        self.__winning_tiles = []
        shanten_calculator = Shanten()
        hand_34 = convert_tiles_list_to_hand34(self.player_deck)

        # If current hand is not Tenpai (0 shanten), Furiten concept doesn't apply yet
        if shanten_calculator.calculate_shanten(hand_34) != 0:
            return False, []

        # Check every possible tile to see if it makes the hand complete (-1 shanten)
        for i in range(34):
            # Add tile 'i' temporarily
            hand_34[i] += 1
            if shanten_calculator.calculate_shanten(hand_34) == -1:
                self.__winning_tiles.append(i)
            hand_34[i] -= 1  # Remove it

    def reset_call(self):
        self.can_call = []

    def is_chii_able(self, tile: Tile) -> bool:
        if tile.type == TileType.DRAGON or tile.type == TileType.WIND:
            return False

        # Case 1: n - 1, n, n + 1
        if self.find_tile(tile.type, tile.number - 1) and self.find_tile(
            tile.type, tile.number + 1
        ):
            return True

        # Case 2: n - 2, n - 1, n
        if self.find_tile(tile.type, tile.number - 2) and self.find_tile(
            tile.type, tile.number - 1
        ):
            return True

        # Case 3: n, n + 1, n + 2
        if self.find_tile(tile.type, tile.number + 1) and self.find_tile(
            tile.type, tile.number + 2
        ):
            return True

    def is_pon_able(self, tile: Tile) -> bool:
        return (
            convert_tiles_list_to_hand34(self.player_deck)[tile.hand34_idx] >= 2
            and tile != self.get_draw_tile()
        )

    def is_kan_able(self, tile: Tile) -> bool:
        for call in self.call_list:
            if call.type == CallType.PON and all(
                [
                    tile.type == call_tile.type and tile.number == call_tile.number
                    for call_tile in call.tiles
                ]
            ):
                return True

        return convert_tiles_list_to_hand34(self.player_deck)[tile.hand34_idx] >= 3

    def is_ron_able(self, tile: Tile) -> bool:
        for discard_tile in self.__already_discard_tiles:
            if convert_tile_to_hand34_index(discard_tile) in self.__winning_tiles:
                return False

        calculator = HandCalculator()

        if len(self.call_list) > 0 and any(
            filter(lambda call: call.is_opened == True, self.call_list)
        ):
            config = HandConfig(is_tsumo=False, is_riichi=False)

        else:
            config = HandConfig(is_tsumo=False, is_riichi=True)

        result = calculator.estimate_hand_value(
            convert_tiles_list_to_hand136(self.player_deck),
            win_tile=convert_tiles_list_to_hand136([tile])[0],
            melds=self.melds,
            config=config,
        )

        if not result.error:
            print(f"Player {self.player_idx} is winning: {result}")
            return True
        else:
            print(f"Player {self.player_idx} is not winning because {result.error}")
            return False

    def is_tsumo_able(self) -> bool:
        calculator = HandCalculator()

        if len(self.call_list) > 0 and any(
            filter(lambda call: call.is_opened == True, self.call_list)
        ):
            config = HandConfig(is_tsumo=True, is_riichi=False)

        else:
            config = HandConfig(is_tsumo=True, is_riichi=True)

        result = calculator.estimate_hand_value(
            convert_tiles_list_to_hand136(self.player_deck),
            win_tile=convert_tiles_list_to_hand136([self.get_draw_tile()])[0],
            melds=self.melds,
            config=config,
        )

        if not result.error:
            print(f"Player {self.player_idx} is winning: {result}")
            return True
        else:
            print(
                f"Player {self.player_idx} is not winning with tsumo because: {result.error}"
            )
            return False

    def count_shanten_points(
        self,
        tiles: list[Tile],
    ) -> int:
        from mahjong.shanten import Shanten

        shanten_calculator = Shanten()
        points = shanten_calculator.calculate_shanten(
            convert_tiles_list_to_hand34(tiles),
        )
        return points

    def __eq__(self, value):
        if not isinstance(value, Player):
            return NotImplemented

        return id(value) == id(self)

    def __str__(self):
        return f"Player {self.player_idx}"
