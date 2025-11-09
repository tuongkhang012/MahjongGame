from components.buttons.tile import Tile
from components.call import Call
from utils.enums import CallType, TileSource
from pygame import Surface


class Player:
    player_idx: int
    player_deck: list[Tile]
    play_tiles: list[Tile]
    call_tiles: list[Call]

    def __init__(
        self,
        player_idx: int,
        player_deck: list[Tile] = None,
        play_tiles: list[Tile] = None,
        call_tiles: list[Tile] = None,
    ):
        self.player_idx = player_idx
        self.player_deck = player_deck if player_deck is not None else []
        self.play_tiles = play_tiles if play_tiles is not None else []
        self.call_tiles = call_tiles if call_tiles is not None else []

    def draw(self, draw_deck: list[Tile]):
        self.__draw_tile = draw_deck.pop()
        self.__draw_tile.source = TileSource.DRAW
        self.player_deck.append(self.__draw_tile)
        self.__draw_tile.update_tile_surface(self.player_idx)

    def discard(self, tile: Tile):
        tile.reveal()
        tile.unclicked()
        self.player_deck.remove(tile)
        self.play_tiles.append(tile)
        print(f"Player {self.player_idx} discard tile: {tile.type} {tile.number}")

    def call(self, type: CallType, tiles: list[Tile]):
        for tile in tiles:
            tile.reveal()

        self.call_tiles.append(Call(type, tiles))

    def rearrange_deck(self):
        self.player_deck.sort(key=lambda tile: (tile.type.value, tile.number))

    def reveal_hand(self):
        for tile in self.player_deck:
            tile.hidden = False

    def make_move(self):
        from random import randint

        tile_idx = randint(0, len(self.player_deck) - 1)
        self.discard(self.player_deck[tile_idx])

    def render_player_deck(self, screen: Surface):
        for tile in self.player_deck:
            tile.render(screen)
