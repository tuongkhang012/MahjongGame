from pygame import Rect, Surface
from components.fields.field import Field
import pygame
import typing
import math

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class TilesField(Field):
    tiles_list: list["Tile"]
    draw_tile_offset: int = 20

    def __init__(self, screen: Surface, tiles_list: list["Tile"]):
        super().__init__()
        self.screen = screen
        self.tiles_list = tiles_list

    def hover(self):
        pass

    def click(self):
        pass

    def build_field_surface(self, player: "Player"):
        first_tile = self.tiles_list[0]
        tile_width, tile_height = first_tile.get_surface().get_size()

        match player.player_idx:
            case 0 | 2:
                self.surface = Surface(
                    (
                        tile_width * len(player.player_deck)
                        + (self.draw_tile_offset if player.total_tiles() >= 14 else 0),
                        tile_height,
                    ),
                    pygame.SRCALPHA,
                )

            case 1 | 3:
                self.surface = Surface(
                    (
                        tile_width,
                        tile_height * (math.ceil(len(player.player_deck) / 2) + 1)
                        + tile_height
                        + (self.draw_tile_offset if player.total_tiles() >= 14 else 0),
                    ),
                    pygame.SRCALPHA,
                )

    def build_tiles_position(self, player: "Player"):
        for idx, tile in enumerate(player.player_deck):
            tile.update_tile_surface(player.player_idx)
            tile_surface = (
                tile.get_hidden_surface() if tile.hidden else tile.get_surface()
            )
            tile_width, tile_height = tile_surface.get_size()

            match player.player_idx:
                case 0:
                    if (
                        tile == player.player_deck[-1]
                        and player.total_tiles() >= 14
                        and player.get_draw_tile() == tile
                    ):
                        position_x = self.draw_tile_offset + tile_width * idx

                    else:
                        position_x = tile_width * idx

                    position_y = 0

                case 2:
                    start_x_position = 0
                    if (
                        tile == player.player_deck[-1]
                        and player.total_tiles() >= 14
                        and player.get_draw_tile() == tile
                    ):

                        position_x = 0
                        start_x_position = tile_width + self.draw_tile_offset

                    else:
                        position_x = start_x_position + tile_width * idx

                    position_y = 0

                case 3:
                    position_x = 0

                    if (
                        tile == player.player_deck[-1]
                        and player.total_tiles() >= 14
                        and tile == player.get_draw_tile()
                    ):
                        position_y = self.draw_tile_offset + tile_height / 2 * idx

                    else:
                        position_y = (tile_height / 2) * idx

                case 1:
                    position_x = 0

                    start_y_position = 0
                    if (
                        tile == player.player_deck[-1]
                        and player.total_tiles() >= 14
                        and tile == player.get_draw_tile()
                    ):
                        position_y = 0
                        start_y_position = tile_height + self.draw_tile_offset
                    else:
                        position_y = start_y_position + tile_height / 2 * idx

            tile.update_position(position_x, position_y, tile_width, tile_height)

    def calculate_center_range(self, deck_list: list["Tile"], player_idx: int):
        deck_size = len(deck_list)

        middle_height = self.screen.get_height() * 1 / 2
        middle_width = self.screen.get_width() * 1 / 2
        offset_height = self.screen.get_height() * 1 / 3
        offset_width = self.screen.get_width() * 1 / 3

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
                    middle_height + offset_height,
                )
            case 1:
                return (
                    middle_width + offset_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )
            case 2:
                return (
                    middle_width
                    + (deck_size * (sum(total_width) / len(total_width)) / 2),
                    middle_height - offset_height,
                )
            case 3:
                return (
                    middle_width - offset_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )
