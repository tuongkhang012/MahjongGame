from utils.enums import Direction
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK
from components.tile import Tile
from pygame import Surface
from utils.enums import TilesType


class GameBuilder:
    def __init__(self, screen: Surface, clock):
        self.screen = screen
        self.clock = clock
        self.tiles_cutter = TilesCutter(TILES_IMAGE_LINK)

    def direction(self) -> list[Direction]:
        import random

        current_direction = random.randint(1, 4)
        standard = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx]

    def create_new_deck(self) -> list[Tile]:
        from random import shuffle

        full_deck = []
        for i in range(1, 5):
            dragon_tiles_deck = [Tile(TilesType.DRAGON, x) for x in range(1, 4)]
            wind_tiles_deck = [Tile(TilesType.WIND, x) for x in range(1, 5)]
            full_deck += dragon_tiles_deck + wind_tiles_deck
        for i in range(1, 4):
            pin_tiles_deck = [Tile(TilesType.PIN, x) for x in range(1, 10)]
            sou_tiles_deck = [Tile(TilesType.SOU, x) for x in range(1, 10)]
            man_tiles_deck = [Tile(TilesType.MAN, x) for x in range(1, 10)]

            full_deck += pin_tiles_deck + sou_tiles_deck + man_tiles_deck

        # Handle special case for AKA
        pin_tiles_deck = [Tile(TilesType.PIN, x) for x in range(1, 10) if x != 5]
        sou_tiles_deck = [Tile(TilesType.SOU, x) for x in range(1, 10) if x != 5]
        man_tiles_deck = [Tile(TilesType.MAN, x) for x in range(1, 10) if x != 5]
        full_deck += (
            pin_tiles_deck
            + sou_tiles_deck
            + man_tiles_deck
            + [Tile(TilesType.AKA, x) for x in range(1, 4)]
        )

        shuffle(full_deck)
        return full_deck

    def roll_dices(self) -> int:
        from random import randint

        return randint(2, 12)

    def visualize_player(self, player_idx: int, player_decks: list[Tile]) -> None:
        from utils.helper import calculate_center_range

        start_x_center, start_y_center = calculate_center_range(
            self.screen, player_idx, len(player_decks)
        )

        for idx, tile in enumerate(player_decks):
            print(f"Player {player_idx}: ", tile.number, tile.type, tile.hidden)
            if tile.hidden:
                surface = self.tiles_cutter.cut_hidden_tiles(True, player_idx)

            else:
                surface = self.tiles_cutter.cut_tiles(
                    tile.type, tile.number, player_idx
                )
            match player_idx:
                case 1:
                    self.screen.blit(
                        surface, (start_x_center + 16 * idx, start_y_center)
                    )
                case 2:
                    self.screen.blit(
                        surface, (start_x_center, start_y_center + 16 * idx)
                    )
                case 3:
                    self.screen.blit(
                        surface, (start_x_center + 16 * idx, start_y_center)
                    )
                case 4:
                    self.screen.blit(
                        surface, (start_x_center, start_y_center + 16 * idx)
                    )

    def visualize_tile(
        self,
        player_idx: int,
        tile_type: TilesType,
        tile_number: int,
    ) -> None:
        tile = self.tiles_cutter.cut_tiles(tile_type, tile_number, player_idx)
        self.screen.blit(tile, (0, 0))
