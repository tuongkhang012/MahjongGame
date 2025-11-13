from components.buttons.tile import Tile
from components.call import Call
from utils.enums import CallType, TileSource
from pygame import Surface
import typing
from utils.enums import Direction
from components.fields.discard_field import DiscardField
from components.fields.deck_field import DeckField
from components.fields.call_field import CallField

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

    def draw(self, draw_deck: list[Tile]):
        self.__draw_tile = draw_deck.pop()
        self.__draw_tile.source = TileSource.DRAW
        self.player_deck.append(self.__draw_tile)
        self.__draw_tile.update_tile_surface(self.player_idx)

    def discard(self, tile: Tile):
        tile.reveal()
        tile.unclicked()
        self.player_deck.remove(tile)
        self.discard_tiles.append(tile)
        print(
            f"Player {self.player_idx} discard tile: {tile.type} {tile.number}, discard_fields: {self.discard_tiles}"
        )

    def call(self, type: CallType, tiles: list[Tile]):
        for tile in tiles:
            tile.reveal()

        self.call_tiles.append(Call(type, tiles))

    def rearrange_deck(self):
        self.player_deck.sort(key=lambda tile: (tile.type.value, tile.number))

    def reveal_hand(self):
        for tile in self.player_deck:
            tile.hidden = False

    def make_move(self, game_manager: "GameManager"):
        from random import randint

        tile_idx = randint(0, len(self.player_deck) - 1)
        discarded_tile = self.player_deck[tile_idx]
        self.discard(discarded_tile)
        game_manager.start_discarded_animation(discarded_tile)

    def get_draw_tile(self) -> Tile:
        return self.__draw_tile

    def total_tiles(self) -> int:
        return len(self.deck_field.get_tiles_list()) + len(
            self.call_field.get_tiles_list()
        )
