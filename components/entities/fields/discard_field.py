from components.entities.fields.tiles_field import TilesField
from pygame import Rect, Surface
import pygame
import typing
from shared.image_cutter import ImageCutter
from utils.constants import DISCARD_FIELD_SIZE
import math
from utils.helper import draw_hitbox

if typing.TYPE_CHECKING:
    from components.entities.player import Player
    from components.entities.buttons.tile import Tile


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
        self.__ratio_riichi = 1

        self.__ratio_normal = 1 / 6

    def render(self) -> Surface:
        self.build_field_surface()
        self.build_tiles_position()
        for tile in self.get_tiles_list():
            tile.render(self.surface)

        draw_hitbox(self.surface, (0, 255, 255))

    def build_field_surface(self) -> Surface:
        check_riichi_tiles = list(
            filter(lambda tile: tile.discard_from_richii(), self.get_tiles_list())
        )
        not_riichi_tiles = list(
            filter(lambda tile: not tile.discard_from_richii(), self.get_tiles_list())
        )
        if len(check_riichi_tiles) == 0 or len(not_riichi_tiles) == 0:
            self.surface = Surface(DISCARD_FIELD_SIZE, pygame.SRCALPHA)
        else:
            match self.player_idx:
                case 0 | 2:
                    self.surface = Surface(
                        (
                            DISCARD_FIELD_SIZE[0]
                            + abs(
                                check_riichi_tiles[0].get_surface().get_width()
                                * self.__ratio_riichi
                                - not_riichi_tiles[0].get_surface().get_height()
                                * self.__ratio_normal
                            ),
                            DISCARD_FIELD_SIZE[1],
                        ),
                        pygame.SRCALPHA,
                    )

                case 1 | 3:
                    self.surface = Surface(
                        (
                            DISCARD_FIELD_SIZE[0],
                            DISCARD_FIELD_SIZE[1]
                            + abs(
                                check_riichi_tiles[0].get_surface().get_height()
                                * self.__ratio_riichi
                                - not_riichi_tiles[0].get_surface().get_height()
                                * self.__ratio_normal
                            ),
                        ),
                        pygame.SRCALPHA,
                    )

    def build_tiles_position(self):
        riichi_tile_idx = None
        riichi_tile_line = None
        riichi_tile = None
        for idx, tile in enumerate(self.get_tiles_list()):
            line = math.floor(idx / 6)

            same_line_with_riichi = line == riichi_tile_line

            tile_height = DISCARD_FIELD_SIZE[1] / 6
            tile_width = DISCARD_FIELD_SIZE[0] / 6

            if tile.discard_from_richii():
                riichi_tile = tile
                riichi_tile_idx = idx
                match self.player_idx:
                    case 0 | 2:
                        self.__ratio_riichi = tile_height / tile.surface.get_height()
                    case 1 | 3:
                        self.__ratio_riichi = tile_width / tile.surface.get_width()

                tile.scale_surface(self.__ratio_riichi)
                tile.update_position(
                    tile.surface.get_width() * (idx % 6),
                    line * tile.surface.get_height(),
                    tile.surface.get_width(),
                    tile.surface.get_height(),
                )
                continue

            match self.player_idx:
                case 0:
                    if same_line_with_riichi:
                        tile_x = (
                            tile.surface.get_width() * (idx % 6)
                            if idx < riichi_tile_idx
                            else riichi_tile.get_position().x
                            + riichi_tile.get_surface().get_width()
                            + tile.surface.get_width()
                            * ((idx - riichi_tile_idx - 1) % 6)
                        )
                    else:
                        tile_x = tile.surface.get_width() * (idx % 6)
                    self.__ratio_normal = tile_width / tile.get_surface().get_width()
                    tile.scale_surface(self.__ratio_normal)
                    tile.update_position(
                        tile_x,
                        line * tile.surface.get_height(),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 1:
                    if same_line_with_riichi:
                        tile_y = (
                            self.surface.get_height()
                            - tile.surface.get_height() * ((idx % 6) + 1)
                            if idx < riichi_tile_idx
                            else riichi_tile.get_position().y
                            - tile.surface.get_height() * ((idx - riichi_tile_idx) % 6)
                        )
                    else:
                        tile_y = (
                            self.surface.get_height()
                            - tile.surface.get_height() * ((idx % 6) + 1)
                        )
                    self.__ratio_normal = tile_height / tile.get_surface().get_height()
                    tile.scale_surface(self.__ratio_normal)
                    tile.update_position(
                        line * tile.surface.get_width(),
                        tile_y,
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 2:
                    self.__ratio_normal = tile_width / tile.get_surface().get_width()
                    tile.scale_surface(self.__ratio_normal)
                    tile.update_position(
                        180 - tile.surface.get_width() * ((idx % 6) + 1),
                        180 - tile.surface.get_height() * (line + 1),
                        tile.surface.get_width(),
                        tile.surface.get_height(),
                    )
                case 3:
                    self.__ratio_normal = tile_height / tile.get_surface().get_height()
                    tile.scale_surface(self.__ratio_normal)
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
