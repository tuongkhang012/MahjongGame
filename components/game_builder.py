from utils.enums import Direction
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK
from components.tile import Tile
from pygame import Surface
from utils.enums import TilesType
from components.player import Player


class GameBuilder:
    def __init__(self, screen: Surface, clock):
        self.screen = screen
        self.clock = clock

    def direction(self) -> list[Direction]:
        import random

        current_direction = random.randint(0, 3)
        standard = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_idx = standard.index(Direction(current_direction))
        return list(reversed(standard[current_idx:] + standard[:current_idx]))

    def create_new_deck(self) -> list[Tile]:
        from random import shuffle

        full_deck = []
        for i in range(4):
            dragon_tiles_deck = [Tile(TilesType.DRAGON, x) for x in range(1, 4)]
            wind_tiles_deck = [Tile(TilesType.WIND, x) for x in range(1, 5)]
            full_deck += dragon_tiles_deck + wind_tiles_deck
        for i in range(3):
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
            + [
                Tile(TilesType.MAN, 5, True),
                Tile(TilesType.PIN, 5, True),
                Tile(TilesType.SOU, 5, True),
            ]
        )

        shuffle(full_deck)
        return full_deck

    def roll_dices(self) -> int:
        from random import randint

        return randint(2, 12)

    def build_tiles_poistion(self, player_idx: int, player: Player) -> None:
        start_x_center, start_y_center = self.calculate_center_range(
            player_idx, player.player_deck
        )
        for idx, tile in enumerate(player.player_deck):
            tile.update_tile_surface(player_idx)
            tile_surface = (
                tile.get_hidden_surface() if tile.hidden else tile.get_surface()
            )
            tile_width, tile_height = tile_surface.get_size()
            position = None
            match player_idx:
                case 0:
                    position = (start_x_center + tile_width * idx, start_y_center)

                case 1:
                    position = (start_x_center, start_y_center + tile_height / 2 * idx)

                case 2:
                    position = (start_x_center + tile_width * idx, start_y_center)

                case 3:
                    position = (start_x_center, start_y_center + tile_height / 2 * idx)

            tile.update_position(position[0], position[1], tile_width, tile_height)

    def calculate_center_range(self, player_idx: int, deck_list: list[Tile]):
        deck_size = len(deck_list)

        middle_height = self.screen.get_height() * 1 / 2
        middle_width = self.screen.get_width() * 1 / 2
        quarter_height = self.screen.get_height() * 1 / 3
        quarter_width = self.screen.get_width() * 1 / 3

        total_width = list(
            map(lambda tile: tile.get_surface().get_bounding_rect().width, deck_list)
        )
        total_heigth = list(
            map(lambda tile: tile.get_surface().get_bounding_rect().height, deck_list)
        )
        match player_idx:
            case 0:
                return (
                    middle_width
                    - (deck_size * (sum(total_width) / len(total_width)) / 2),
                    middle_height + quarter_height,
                )
            case 1:
                return (
                    middle_width - quarter_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )
            case 2:
                return (
                    middle_width
                    - (deck_size * (sum(total_width) / len(total_width)) / 2),
                    middle_height - quarter_height,
                )
            case 3:
                return (
                    middle_width + quarter_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )
