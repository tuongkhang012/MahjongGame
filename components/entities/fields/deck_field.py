from components.entities.fields.tiles_field import TilesField
from mahjong.shanten import Shanten
from pygame import Rect, Surface
import typing
from utils.helper import build_center_rect, draw_hitbox, convert_tiles_list_to_hand34
import pygame

if typing.TYPE_CHECKING:
    from components.entities.player import Player
    from components.entities.buttons.tile import Tile


class DeckField(TilesField):
    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__(screen, player_idx, tiles_list, full_tiles_list)

    def render(self, player: "Player"):
        self.build_field_surface(player)
        self.build_tiles_position(player)
        if (
            player.player_idx == 1
            and player.get_draw_tile() == self.get_tiles_list()[-1]
            and len(self.get_tiles_list()) >= 14
        ):
            self.get_tiles_list()[-1].render(self.surface)
            for tile in self.get_tiles_list()[:-1]:
                tile.render(self.surface)

        else:
            for tile in self.get_tiles_list():
                tile.render(self.surface)

        match player.player_idx:
            case 0 | 2:
                half_screen_surface = Surface(
                    (self.screen.get_width(), self.screen.get_height() / 6),
                    pygame.SRCALPHA,
                )

            case 1 | 3:
                half_screen_surface = Surface(
                    (self.screen.get_width() / 3, self.screen.get_height()),
                    pygame.SRCALPHA,
                )

        self.update_relative_position(
            build_center_rect(half_screen_surface, self.surface)
        )

        draw_hitbox(self.surface)
        draw_hitbox(half_screen_surface)

        half_screen_surface.blit(
            self.surface,
            (self.get_relative_position().x, self.get_relative_position().y),
        )
        match player.player_idx:
            case 0:
                half_screen_surface_position = (0, 5 * self.screen.get_height() / 6)

            case 1:
                half_screen_surface_position = (2 * self.screen.get_width() / 3, 0)

            case 2 | 3:
                half_screen_surface_position = (0, 0)

        self._absolute_position = Rect(
            half_screen_surface_position[0] + self.get_relative_position().x,
            half_screen_surface_position[1] + self.get_relative_position().y,
            self.get_relative_position().width,
            self.get_relative_position().height,
        )

        self.screen.blit(half_screen_surface, half_screen_surface_position)

    def build_field_surface(self, player: "Player"):
        first_tile = self.get_tiles_list()[0]
        tile_width, tile_height = first_tile.get_surface().get_size()
        hover_offset_y = first_tile.hover_offset_y
        match player.player_idx:
            case 0:
                self.surface = Surface(
                    (
                        tile_width * len(self.get_tiles_list())
                        + (
                            self.draw_tile_offset
                            if player.get_draw_tile() == self.get_tiles_list()[-1]
                            and player.total_tiles() >= 14
                            else 0
                        ),
                        tile_height + hover_offset_y,
                    ),
                    pygame.SRCALPHA,
                )

            case 2:
                self.surface = Surface(
                    (
                        tile_width * len(self.get_tiles_list())
                        + (
                            self.draw_tile_offset
                            if player.get_draw_tile() == self.get_tiles_list()[-1]
                            and player.total_tiles() >= 14
                            else 0
                        ),
                        tile_height,
                    ),
                    pygame.SRCALPHA,
                )
            case 1 | 3:
                self.surface = Surface(
                    (
                        tile_width,
                        (tile_height / 2) * (len(self.get_tiles_list()) - 1)
                        + tile_height
                        + (
                            self.draw_tile_offset
                            if player.get_draw_tile() == self.get_tiles_list()[-1]
                            and player.total_tiles() >= 14
                            else 0
                        ),
                    ),
                    pygame.SRCALPHA,
                )

    def build_tiles_position(self, player: "Player"):

        for idx, tile in enumerate(self.get_tiles_list()):
            if tile.is_hovered == True:
                continue

            tile.update_tile_surface(player.player_idx)
            tile_surface = (
                tile.get_hidden_surface() if tile.hidden else tile.get_surface()
            )
            tile_width, tile_height = tile_surface.get_size()

            match player.player_idx:
                case 0:
                    if (
                        tile == self.get_tiles_list()[-1]
                        and player.total_tiles() >= 14
                        and player.get_draw_tile() == tile
                    ):
                        position_x = self.draw_tile_offset + tile_width * idx

                    else:
                        position_x = tile_width * idx

                    position_y = tile.hover_offset_y

                case 1:
                    position_x = 0
                    if (
                        tile == self.get_tiles_list()[-1]
                        and tile == player.get_draw_tile()
                        and player.total_tiles() >= 14
                    ):
                        position_y = 0

                    elif (
                        player.total_tiles() >= 14
                        and self.get_tiles_list()[-1] == player.get_draw_tile()
                    ):
                        position_y = self.draw_tile_offset + tile_height / 2 * (idx + 1)
                    else:
                        position_y = tile_height / 2 * idx

                case 2:
                    if (
                        tile == self.get_tiles_list()[-1]
                        and player.total_tiles() >= 14
                        and player.get_draw_tile() == tile
                    ):
                        position_x = 0
                    elif (
                        player.total_tiles() >= 14
                        and self.get_tiles_list()[-1] == player.get_draw_tile()
                    ):
                        position_x = self.draw_tile_offset + tile_width * (idx + 1)
                    else:
                        position_x = tile_width * idx
                    position_y = 0

                case 3:
                    position_x = 0

                    if (
                        tile == self.get_tiles_list()[-1]
                        and player.total_tiles() >= 14
                        and tile == player.get_draw_tile()
                    ):
                        position_y = self.draw_tile_offset + tile_height / 2 * idx

                    else:
                        position_y = (tile_height / 2) * idx

            tile.update_position(position_x, position_y, tile_width, tile_height)
