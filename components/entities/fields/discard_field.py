from components.entities.fields.tiles_field import TilesField
from pygame import Rect, Surface
import pygame
import typing
from shared.image_cutter import ImageCutter
from utils.constants import DISCARD_FIELD_SIZE, CENTER_BOARD_FIELD_BORDER_COLOR
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
        return self.surface

    def build_field_surface(self) -> Surface:
        check_riichi_tiles = list(
            filter(lambda tile: tile.is_discard_from_riichi(), self.get_tiles_list())
        )

        tile_height = DISCARD_FIELD_SIZE[1] / 6
        tile_width = DISCARD_FIELD_SIZE[0] / 6
        if len(check_riichi_tiles) == 0:
            self.surface = Surface(DISCARD_FIELD_SIZE, pygame.SRCALPHA)
        else:
            normal_width = check_riichi_tiles[0].get_surface().get_width()
            normal_height = check_riichi_tiles[0].get_surface().get_height()
            check_riichi_tiles[0].update_tile_surface((self.player_idx - 1) % 4)

            match self.player_idx:
                case 0 | 2:
                    self.__ratio_riichi = (
                        tile_height / check_riichi_tiles[0].get_surface().get_height()
                    )
                    self.surface = Surface(
                        (
                            DISCARD_FIELD_SIZE[0]
                            + abs(
                                check_riichi_tiles[0].get_surface().get_width()
                                * self.__ratio_riichi
                                - normal_width * self.__ratio_normal
                            ),
                            DISCARD_FIELD_SIZE[1],
                        ),
                        pygame.SRCALPHA,
                    )

                case 1 | 3:
                    self.__ratio_riichi = (
                        tile_width / check_riichi_tiles[0].get_surface().get_width()
                    )
                    self.surface = Surface(
                        (
                            DISCARD_FIELD_SIZE[0],
                            DISCARD_FIELD_SIZE[1]
                            + abs(
                                check_riichi_tiles[0].get_surface().get_height()
                                * self.__ratio_riichi
                                - normal_height * self.__ratio_normal
                            ),
                        ),
                        pygame.SRCALPHA,
                    )

    def build_tiles_position(self):
        start_width = 0
        start_height = 0

        normal_tile_height = 0
        normal_tile_width = 0
        for idx, tile in enumerate(self.get_tiles_list()):
            line = math.floor(idx / 6)

            if idx % 6 == 0:
                start_width = 0
                start_height = 0

            tile_height = DISCARD_FIELD_SIZE[1] / 6
            tile_width = DISCARD_FIELD_SIZE[0] / 6

            match self.player_idx:
                case 0:
                    if tile.is_discard_from_riichi():
                        tile.scale_surface(self.__ratio_riichi)
                    else:
                        self.__ratio_normal = (
                            tile_width / tile.get_surface().get_width()
                        )
                        tile.scale_surface(self.__ratio_normal)
                        normal_tile_height = tile.get_surface().get_height()

                    tile.update_position(
                        start_width,
                        line * normal_tile_height,
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )
                    start_width += tile.get_surface().get_width()
                case 1:
                    if tile.is_discard_from_riichi():
                        tile.scale_surface(self.__ratio_riichi)
                    else:
                        self.__ratio_normal = (
                            tile_height / tile.get_surface().get_height()
                        )
                        tile.scale_surface(self.__ratio_normal)
                        normal_tile_width = tile.get_surface().get_width()

                    start_height += tile.get_surface().get_height()
                    tile.update_position(
                        line * normal_tile_width,
                        self.surface.get_height() - start_height,
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )
                case 2:
                    if tile.is_discard_from_riichi():
                        tile.scale_surface(self.__ratio_riichi)
                        start_width += tile.get_surface().get_width()
                        tile.update_position(
                            self.surface.get_width() - start_width,
                            self.surface.get_height()
                            - line * normal_tile_height
                            - tile.get_surface().get_height(),
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )

                    else:
                        self.__ratio_normal = (
                            tile_width / tile.get_surface().get_width()
                        )
                        tile.scale_surface(self.__ratio_normal)
                        normal_tile_height = tile.get_surface().get_height()

                        start_width += tile.get_surface().get_width()
                        tile.update_position(
                            self.surface.get_width() - start_width,
                            self.surface.get_height() - (line + 1) * normal_tile_height,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )
                case 3:
                    if tile.is_discard_from_riichi():
                        tile.scale_surface(self.__ratio_riichi)
                        tile.update_position(
                            self.surface.get_width()
                            - normal_tile_width * line
                            - tile.get_surface().get_width(),
                            start_height,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )
                    else:
                        self.__ratio_normal = (
                            tile_height / tile.get_surface().get_height()
                        )
                        tile.scale_surface(self.__ratio_normal)
                        normal_tile_width = tile.get_surface().get_width()

                        tile.update_position(
                            self.surface.get_width() - normal_tile_width * (line + 1),
                            start_height,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )
                    start_height += tile.get_surface().get_height()
