from components.entities.buttons.tile import Tile
from components.entities.call import Call
from utils.enums import CallType, TileSource, TileType, ActionType
from pygame import Surface
import typing
from utils.enums import Direction
from components.entities.fields.discard_field import DiscardField
from components.entities.fields.deck_field import DeckField
from components.entities.fields.call_field import CallField
from utils.helper import (
    map_call_to_action,
    convert_tile_to_hand34_index,
    convert_tiles_list_to_hand34,
    count_shanten_points,
)
from utils.constants import HAND_CONFIG_OPTIONS
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
from mahjong.shanten import Shanten

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


class Player:
    player_idx: int
    player_deck: list[Tile]
    discard_tiles: list[Tile]
    call_list: list[Call]
    direction: Direction
    turn: int

    # All fields
    discard_field: DiscardField
    call_field: CallField
    deck_field: DeckField

    # Callable
    can_call: list[CallType]
    callable_tiles_list: list[list[Tile]]
    melds: list[Meld]

    # Honba
    honba: int

    # Riichi
    __is_riichi: bool = False
    __riichi_turn: int = None

    # Skip yao9
    __skip_yao9: bool = False

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

        self.full_deck = full_deck
        self.screen = screen
        self.discard_field = DiscardField(
            self.screen, self.player_idx, self.discard_tiles, self.full_deck
        )
        self.call_field = CallField(
            self.screen,
            self.player_idx,
            self.call_list,
            self.call_tiles_list,
            self.full_deck,
        )
        self.deck_field = DeckField(
            self.screen, self.player_idx, self.player_deck, self.full_deck
        )

        # Call init
        self.can_call = []
        self.callable_tiles_list = []
        self.melds = []

        # Game properties
        self.__winning_tiles = []

        # Player information
        self.points = 25000
        self.turn = 0
        self.honba = 0

    def draw(
        self,
        draw_deck: list[Tile],
        round_wind: Direction = None,
        tile: Tile = None,
        check_call: bool = True,
    ):
        if tile:
            self.__draw_tile = tile
            draw_deck.remove(tile)
        else:
            self.__draw_tile = draw_deck.pop()

        self.__draw_tile.source = TileSource.DRAW
        self.player_deck.append(self.__draw_tile)
        self.__draw_tile.update_tile_surface(self.player_idx)
        if check_call:
            self.check_call(
                self.__draw_tile,
                is_current_turn=True,
                round_wind=round_wind,
            )
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

    def build_kan(self, tile: Tile) -> bool:
        self.callable_tiles_list = []
        is_kakan = False
        from_player: Player = None
        if tile.source == TileSource.PLAYER:
            callable_tiles_list = list(
                filter(
                    lambda player_tile: tile.number == player_tile.number
                    and tile.type == player_tile.type,
                    self.player_deck,
                )
            ) + [tile]
            self.callable_tiles_list.append(callable_tiles_list)
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
                        is_kakan = True
                        from_player = call.from_who
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
                    + ([tile] if tile not in self.player_deck else [])
                )
        return (is_kakan, from_player)

    def call(
        self,
        tile: Tile,
        call_list: list[Tile],
        call_type: CallType,
        player: "Player",
        is_kakan: bool = False,
    ):
        """
        Create init call
        """
        if player and not is_kakan:
            tile.source = TileSource.PLAYER

        print(
            f"Player {self.player_idx} call: {call_type} for {list(map(lambda tile: tile.__str__(True),call_list))}"
        )
        if player and not is_kakan:
            player.discard_tiles.remove(tile)
            self.player_deck.append(tile)

        for tmp_tile in call_list:
            if tmp_tile in self.player_deck:
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
                self.call_tiles_list.append(called_tile)

        self.melds.append(self.call_list[-1].meld)

        self.rearrange_deck()
        self.deck_field.build_field_surface(self)
        self.deck_field.build_tiles_position(self)

    def discard(self, tile: Tile, game_manager: "GameManager" = None):
        if game_manager.prev_action == ActionType.RIICHI:
            tile.update_tile_surface((game_manager.current_player.player_idx - 1) % 4)
            tile.discard_riichi()

        tile.reveal()
        tile.unclicked()
        self.player_deck.remove(tile)
        self.discard_tiles.append(tile)
        self.__already_discard_tiles.append(tile)
        game_manager.latest_discarded_tile = tile
        game_manager.start_discarded_animation(tile)
        self.turn += 1
        return tile

    def rearrange_deck(self):
        self.player_deck.sort(key=lambda tile: (tile.type.value, tile.number))

    def reveal_hand(self):
        for tile in self.player_deck:
            tile.hidden = False

    def make_move(self, action: ActionType = None) -> ActionType:
        from random import randint

        if self.__is_riichi:
            if self.player_idx == 0:
                return action
            if CallType.RON in self.can_call:
                return ActionType.RON
            if CallType.TSUMO in self.can_call:
                return ActionType.TSUMO
            tile = self.pick_tile()
            tile.clicked()
            return ActionType.DISCARD

        if action:
            return action

        if len(self.can_call) > 0:
            if self.player_idx == 3:
                return map_call_to_action(self.can_call[0])

            return map_call_to_action(self.can_call[randint(0, len(self.can_call) - 1)])

        tile = self.pick_tile()
        tile.clicked()
        return ActionType.DISCARD

    def pick_tile(self) -> Tile:
        import sys

        minimum_shanten = 14
        discard_tile = None
        for tile in self.player_deck:
            tmp_tiles_list = self.player_deck.copy()
            tmp_tiles_list.remove(tile)
            if minimum_shanten > count_shanten_points(tmp_tiles_list):
                discard_tile = tile
                minimum_shanten = count_shanten_points(tmp_tiles_list)

        if (
            len(sys.argv) > 1
            and len(list(filter(lambda argv: "data=kaze4.json" in argv, sys.argv))) > 0
        ):
            tile = self.find_tile(TileType.WIND, 1)

        elif self.player_idx == 1 and self.find_tile(TileType.SOU, 9):
            tile = self.find_tile(TileType.SOU, 9)
        else:
            tile = discard_tile
        return tile

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

    def check_call(
        self,
        tile: Tile,
        is_current_turn: bool,
        round_wind: Direction,
        check_chii: bool = False,
    ):
        print("----- Start cheking call -----")
        self.can_call = []

        self.__build_winning_tiles()
        if is_current_turn and self.is_tsumo_able(tile, round_wind):
            self.can_call.append(CallType.TSUMO)

        if not is_current_turn and self.is_ron_able(tile, round_wind):
            self.can_call.append(CallType.RON)

        if not self.__is_riichi:
            if self.is_riichi_able() and is_current_turn:
                self.can_call.append(CallType.RIICHI)

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

    def check_yao9(self) -> bool:
        tile_yao9_list: list[Tile] = []

        for tile in self.player_deck:
            if (
                tile.type in [TileType.MAN, TileType.SOU, TileType.PIN]
                and (tile.number == 1 or tile.number == 9)
            ) or tile.type in [TileType.DRAGON, TileType.WIND]:
                already_have_yao9_tile = False
                for yao9_tile in tile_yao9_list:
                    if yao9_tile.number == tile.number and yao9_tile.type == tile.type:
                        already_have_yao9_tile = True
                        break

                if not already_have_yao9_tile:
                    tile_yao9_list.append(tile)

        if len(tile_yao9_list) >= 8 and not self.__skip_yao9:
            return True
        else:
            return False

    def skip_yao9(self):
        self.__skip_yao9 = True

    def __build_winning_tiles(self):
        self.__winning_tiles = []
        shanten_calculator = Shanten()
        before_draw_player_deck = self.player_deck.copy()

        if self.get_draw_tile() in before_draw_player_deck:
            before_draw_player_deck.remove(self.get_draw_tile())
        hand_34 = convert_tiles_list_to_hand34(before_draw_player_deck)

        # If current hand is not Tenpai (0 shanten), Furiten concept doesn't apply yet
        if shanten_calculator.calculate_shanten(hand_34) != 0:
            return

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
            if (
                call.type == CallType.PON
                and tile == self.get_draw_tile()
                and all(
                    [
                        tile.type == call_tile.type and tile.number == call_tile.number
                        for call_tile in call.tiles
                    ]
                )
            ):
                return True
        if tile in self.player_deck:
            return convert_tiles_list_to_hand34(self.player_deck)[tile.hand34_idx] == 4
        else:
            return convert_tiles_list_to_hand34(self.player_deck)[tile.hand34_idx] == 3

    def is_ron_able(self, tile: Tile, round_wind: Direction) -> bool:
        for discard_tile in self.__already_discard_tiles:
            if convert_tile_to_hand34_index(discard_tile) in self.__winning_tiles:
                print(
                    f"Player {self.player_idx} is not winning with ron because furiten: {self.__winning_tiles} is in {self.__already_discard_tiles}"
                )
                return False

        calculator = HandCalculator()

        config = HandConfig(
            is_tsumo=False,
            is_riichi=self.__is_riichi,
            round_wind=round_wind.value + 27,
            player_wind=self.direction.value + 27,
            options=HAND_CONFIG_OPTIONS,
        )

        copy_player_deck = self.player_deck.copy()
        copy_player_deck.append(tile)
        hands = copy_player_deck + self.call_tiles_list

        result = calculator.estimate_hand_value(
            list(map(lambda tile: tile.hand136_idx, hands)),
            win_tile=tile.hand136_idx,
            melds=self.melds,
            config=config,
        )

        if not result.error:
            print(f"Player {self.player_idx} is winning: {result} with {result.yaku}")
            return True
        else:
            print(
                f"Player {self.player_idx} is not winning with ron because {result.error}"
            )
            return False

    def is_tsumo_able(self, tile: Tile, round_wind: Direction) -> bool:
        calculator = HandCalculator()

        config = HandConfig(
            is_tsumo=True,
            is_riichi=self.__is_riichi,
            round_wind=round_wind.value + 27,
            player_wind=self.direction.value + 27,
            options=HAND_CONFIG_OPTIONS,
        )
        hands = self.player_deck + self.call_tiles_list
        result = calculator.estimate_hand_value(
            list(map(lambda tile: tile.hand136_idx, hands)),
            win_tile=self.get_draw_tile().hand136_idx,
            melds=self.melds,
            config=config,
        )

        if not result.error:
            print(f"Player {self.player_idx} is winning: {result} with {result.yaku}")
            return True
        else:
            print(
                f"Player {self.player_idx} is not winning with tsumo because: {result.error}"
            )
            return False

    def is_riichi_able(self) -> bool:
        if count_shanten_points(self.player_deck) == 0 and (
            len(self.call_list) == 0
            or (
                len(self.call_list) > 0
                and len(list(filter(lambda call: call.is_opened, self.call_list))) == 0
            )
        ):
            return True
        else:
            return False

    def riichi(self):
        self.__is_riichi = True
        self.__riichi_turn = self.turn

    def is_riichi(self) -> int:
        """
        Return the turn called riichi
        """
        if self.__is_riichi:
            return self.__riichi_turn
        else:
            return -1

    def renew_deck(self):
        # Tile deck field init
        self.player_deck = []
        self.discard_tiles = []
        self.__already_discard_tiles: list[Tile] = []
        self.call_tiles_list = []
        self.call_list: list[Call] = []

        # Call init
        self.can_call = []
        self.callable_tiles_list = []
        self.melds = []

        self.discard_field = DiscardField(
            self.screen, self.player_idx, self.discard_tiles, self.full_deck
        )
        self.call_field = CallField(
            self.screen,
            self.player_idx,
            self.call_list,
            self.call_tiles_list,
            self.full_deck,
        )
        self.deck_field = DeckField(
            self.screen, self.player_idx, self.player_deck, self.full_deck
        )

        # Game properties
        self.__winning_tiles = []
        self.__is_riichi = False
        self.__riichi_turn: int = None

        self.__skip_yao9 = False

    def __eq__(self, value):
        if not isinstance(value, Player):
            return NotImplemented

        return id(value) == id(self)

    def __str__(self):
        return f"Player {self.player_idx}"
