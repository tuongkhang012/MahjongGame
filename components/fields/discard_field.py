from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import pygame
import typing
from components.image_cutter import ImageCutter
from utils.constants import DISCARD_FIELD_SIZE
import math
from utils.helper import draw_hitbox

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class DiscardField(TilesField):
    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__(screen, player_idx, tiles_list, full_tiles_list)
        self.tiles_per_line = 6

    def render(self, player_idx: int) -> Surface:
        self.build_field_surface()
        self.build_tiles_position(player_idx)
        for tile in self.get_tiles_list():
            tile.render(self.surface)

        draw_hitbox(self.surface, (0, 255, 255))

    def build_field_surface(self) -> Surface:
        self.surface = Surface(DISCARD_FIELD_SIZE, pygame.SRCALPHA)

    def build_tiles_position(self, player_idx: int):
        for idx, tile in enumerate(self.get_tiles_list()):

            line = math.floor(idx / 6)
            tile_width = DISCARD_FIELD_SIZE[0] / 6
            tile_height = DISCARD_FIELD_SIZE[1] / 6
            match player_idx:
                case 0:
                    tile.scale_surface(tile_width / tile.surface.get_width())
                    tile.update_position(
                        tile.surface.get_width() * (idx % 6),
                        line * tile.surface.get_height(),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 1:
                    tile.scale_surface(tile_height / tile.surface.get_height())
                    tile.update_position(
                        line * tile.surface.get_width(),
                        180 - tile.surface.get_height() * ((idx % 6) + 1),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 2:
                    tile.scale_surface(tile_width / tile.surface.get_width())
                    tile.update_position(
                        180 - tile.surface.get_width() * ((idx % 6) + 1),
                        180 - tile.surface.get_height() * (line + 1),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 3:
                    tile.scale_surface(tile_height / tile.surface.get_height())
                    tile.update_position(
                        180 - tile.surface.get_width() * (line + 1),
                        tile.surface.get_height() * (idx % 6),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )

    def update_absolute_position(self, absolute_position: Rect):
        self._absolute_position = absolute_position

    def update_relative_position(self, relative_position: Rect):
        self._relative_position = relative_position
