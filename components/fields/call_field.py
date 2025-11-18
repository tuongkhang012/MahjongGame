from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import pygame
import typing
from components.call import Call
from utils.enums import CallType, TileSource
from utils.helper import draw_hitbox

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class CallField(TilesField):
    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__(screen, player_idx, tiles_list, full_tiles_list)
        self.__call_list: list[Call] = []
        self.__call_surface: list[Surface] = []
        self.max_height = 0
        self.max_width = 0
        self.field_offset = (30, 30)

    def render(self, screen: Surface):
        self.build_call_surface()
        self.build_call_field()

        match self.player_idx:
            case 0:
                screen.blit(
                    self.surface,
                    (
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                    ),
                ),

            case 1:
                screen.blit(
                    self.surface,
                    (
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        self.field_offset[1],
                    ),
                )
            case 2:
                screen.blit(
                    self.surface,
                    (
                        self.field_offset[0],
                        self.field_offset[1],
                    ),
                )
            case 3:
                screen.blit(
                    self.surface,
                    (
                        self.field_offset[0],
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                    ),
                )

    def build_call_field(self):
        # Build wrap surface
        call_field_width = 0
        call_field_height = 0

        match self.player_idx:
            case 0 | 2:
                call_field_height = self.max_height
                for call_surface in self.__call_surface:
                    call_field_width += call_surface.get_width()

            case 1 | 3:
                call_field_width = self.max_width
                for call_surface in self.__call_surface:
                    call_field_height += call_surface.get_height()

        self.surface = Surface((call_field_width, call_field_height), pygame.SRCALPHA)
        draw_hitbox(self.surface, (228, 208, 10))

        # Render each call_surface on surface
        start_width = 0
        start_height = 0
        for call_surface in self.__call_surface:
            match self.player_idx:
                case 0:
                    start_width += call_surface.get_width()
                    self.surface.blit(
                        call_surface, (self.surface.get_width() - start_width, 0)
                    )

                case 1:
                    self.surface.blit(call_surface, (0, start_height))
                    start_height += call_surface.get_height()

                case 2:
                    self.surface.blit(call_surface, (start_width, 0))
                    start_width += call_surface.get_width()

                case 3:
                    start_height += call_surface.get_height()
                    self.surface.blit(
                        call_surface, (0, self.surface.get_height() - start_height)
                    )

    def __build_tiles_position(self, call: Call, surface: Surface):
        start_width = 0
        start_height = 0
        match self.player_idx:
            case 0:
                for tile in call.tiles:
                    tile.update_position(
                        start_width,
                        surface.get_height() - tile.get_surface().get_height(),
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )
                    start_width += tile.get_surface().get_width()

            case 1:
                for tile in call.tiles:
                    start_height += tile.get_surface().get_height()
                    tile.update_position(
                        surface.get_width() - tile.get_surface().get_width(),
                        surface.get_height() - start_height,
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )

            case 2:
                for tile in call.tiles:
                    start_width += tile.get_surface().get_width()

                    tile.update_position(
                        surface.get_width() - start_width,
                        0,
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )

            case 3:
                for tile in call.tiles:
                    tile.update_position(
                        0,
                        start_height,
                        tile.get_surface().get_width(),
                        tile.get_surface().get_height(),
                    )
                    start_height += tile.get_surface().get_height()

    def build_call_surface(self):
        self.__call_surface = []
        for call in self.__call_list:
            # If not ANKAN, update sideway surface for tile
            if not (
                call.type == CallType.KAN and call.another_player_tiles is not None
            ):
                reveal_surface = call.another_player_tiles.tiles_cutter.cut_tiles(
                    call.another_player_tiles.type,
                    call.another_player_tiles.number,
                    call.another_player_tiles.aka,
                    (self.player_idx - 1) % 4,
                )
                call.another_player_tiles.update_tile_surface(
                    reveal_surface=reveal_surface
                )

            surface_size = self.__build_surface_size_based_on_player_idx(call)
            call_surface = Surface(surface_size, pygame.SRCALPHA)

            self.__build_tiles_position(call, call_surface)
            for tile in call.tiles:
                tile.render(call_surface)

            draw_hitbox(call_surface)
            self.__call_surface.append(call_surface)

    def add_call(self, call: Call):
        self.__call_list.append(call)
        for tile in call.tiles:
            self.get_tiles_list().append(tile)

    def __build_surface_size_based_on_player_idx(self, call: Call):
        surface_width = 0
        surface_height = 0

        match self.player_idx:
            case 0 | 2:
                for tile in call.tiles:
                    surface_width += tile.get_surface().get_width()
                try:
                    target_tile_height = list(
                        filter(
                            lambda tile: tile.source == TileSource.PLAYER, call.tiles
                        )
                    )[0]
                    surface_height = target_tile_height.get_surface().get_height() * 2
                except:
                    surface_height = call.tiles[0].get_surface().get_height()
                self.max_height = max(self.max_height, surface_height)
            case 1 | 3:
                for tile in call.tiles:
                    surface_height += tile.get_surface().get_height()
                try:
                    target_tile_height = list(
                        filter(
                            lambda tile: tile.source == TileSource.PLAYER, call.tiles
                        )
                    )[0]
                    surface_width = target_tile_height.get_surface().get_width() * 2
                except:
                    surface_width = call.tiles[0].get_surface().get_width()
                self.max_width = max(surface_width, self.max_width)

        return (surface_width, surface_height)

    def get_call_list(self) -> list[Call]:
        return self.__call_list
