from components.buttons.tile import Tile
from components.call import Call
from utils.enums import CallType, TileSource, TileType, ActionType
from pygame import Surface
import typing
from utils.enums import Direction
from components.fields.discard_field import DiscardField
from components.fields.deck_field import DeckField
from components.fields.call_field import CallField
from utils.helper import map_call_to_action

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class Player:
    player_idx: int
    player_deck: list[Tile]
    discard_tiles: list[Tile]
    call_tiles: list[Call]
    direction: Direction

    # All fields
    discard_field: DiscardField
    call_field: CallField
    deck_field: DeckField

    # Callable
    can_call: list[CallType]
    callable_tiles_list: list[list[Tile]]

    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        direction: Direction,
        full_deck: list[Tile],
        player_deck: list[Tile] = None,
        discard_tiles: list[Tile] = None,
        call_tiles: list[Tile] = None,
    ):
        self.player_idx = player_idx
        self.direction = direction
        self.player_deck = player_deck if player_deck is not None else []
        self.discard_tiles = discard_tiles if discard_tiles is not None else []
        self.call_tiles = call_tiles if call_tiles is not None else []

        self.discard_field = DiscardField(
            screen, self.player_idx, self.discard_tiles, full_deck
        )
        self.call_field = CallField(screen, self.player_idx, self.call_tiles, full_deck)
        self.deck_field = DeckField(
            screen, self.player_idx, self.player_deck, full_deck
        )

        self.can_call = []
        self.callable_tiles_list = []

    def draw(self, draw_deck: list[Tile]):
        self.__draw_tile = draw_deck.pop()
        self.__draw_tile.source = TileSource.DRAW
        self.player_deck.append(self.__draw_tile)
        self.__draw_tile.update_tile_surface(self.player_idx)

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

    def call(
        self, tile: Tile, call_list: list[Tile], call_type: CallType, player: "Player"
    ):

        player.discard_tiles.remove(tile)
        tile.source = TileSource.PLAYER
        self.player_deck.append(tile)

        for tile in call_list:
            self.player_deck.remove(tile)

        self.call_field.add_call(Call(call_type, call_list))
        print(
            f"Player {self.player_idx} call: {call_type} for {list(map(lambda tile: f"{tile.type}, {tile.number}",call_list))}"
        )

    def discard(self, tile: Tile = None, game_manager: "GameManager" = None):
        import random

        if tile is None:
            tile_idx = random.randint(0, len(self.player_deck) - 1)
            tile = self.player_deck[tile_idx]

        tile.reveal()
        tile.unclicked()
        self.player_deck.remove(tile)
        self.discard_tiles.append(tile)

        print(
            f"Player {self.player_idx} discard tile: {tile.type} {tile.number}, discard_fields: {list(map(lambda tile: (tile.type, tile.number), self.discard_tiles))}"
        )
        game_manager.start_discarded_animation(tile)
        game_manager.latest_discarded_tile = tile
        return tile

    def rearrange_deck(self):
        self.player_deck.sort(key=lambda tile: (tile.type.value, tile.number))

    def reveal_hand(self):
        for tile in self.player_deck:
            tile.hidden = False

    def make_move(self) -> ActionType:
        from random import randint

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

    def count_same_tile(self, type: TileType, number: int) -> int:
        count = 0
        for tile in self.player_deck:
            if type == tile.type and number == tile.number:
                count += 1

        return count

    def check_call(self, tile, check_chii: bool = False):
        self.can_call = []
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

    def reset_call(self):
        self.can_call = []

    def is_chii_able(self, tile: Tile) -> bool:
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
        if self.count_same_tile(tile.type, tile.number) == 2:
            return True

    def is_kan_able(self, tile: Tile) -> bool:
        if self.count_same_tile(tile.type, tile.number) == 3:
            return True

    def is_ron_able(self, tile: Tile) -> bool:
        pass

    def __eq__(self, value):
        if not isinstance(value, Player):
            return NotImplemented

        return id(value) == id(self)

    def __str__(self):
        return f"Player {self.player_idx}"
