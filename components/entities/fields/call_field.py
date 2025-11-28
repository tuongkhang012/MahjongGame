from components.entities.fields.tiles_field import TilesField
from pygame import Rect, Surface
from pygame.event import Event
import pygame
import typing
from components.entities.call import Call
from utils.enums import CallType, TileSource
from utils.helper import draw_hitbox

if typing.TYPE_CHECKING:
    from components.entities.player import Player
    from components.entities.buttons.tile import Tile


class CallField(TilesField):
    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        call_list: list[Call],
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__(screen, player_idx, tiles_list, full_tiles_list)
        self.__call_list = call_list
        self.__call_surface: list[Surface] = []
        self.__call_surface_position: list[tuple[int, int]] = []
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
                self.update_relative_position(
                    Rect(
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
                self.update_absolute_position(
                    Rect(
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
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
                self.update_relative_position(
                    Rect(
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        self.field_offset[1],
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
                self.update_absolute_position(
                    Rect(
                        screen.get_width()
                        - self.field_offset[0]
                        - self.surface.get_width(),
                        self.field_offset[1],
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
            case 2:
                screen.blit(
                    self.surface,
                    (
                        self.field_offset[0],
                        self.field_offset[1],
                    ),
                )
                self.update_relative_position(
                    Rect(
                        self.field_offset[0],
                        self.field_offset[1],
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
                self.update_absolute_position(
                    Rect(
                        self.field_offset[0],
                        self.field_offset[1],
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
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
                self.update_relative_position(
                    Rect(
                        self.field_offset[0],
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )
                self.update_absolute_position(
                    Rect(
                        self.field_offset[0],
                        screen.get_height()
                        - self.field_offset[1]
                        - self.surface.get_height(),
                        self.surface.get_width(),
                        self.surface.get_height(),
                    )
                )

    def hover(self, mouse_pos: tuple[int, int]) -> "Tile":
        hovered_call_surface_idx: int = None
        for idx, call_surface in enumerate(self.__call_surface):
            surface_position = self.__call_surface_position[idx]
            local_mouse_pos = self.build_local_mouse(mouse_pos)
            surface_rect = call_surface.get_rect()
            if Rect(
                surface_position[0],
                surface_position[1],
                surface_rect.width,
                surface_rect.height,
            ).collidepoint(
                local_mouse_pos[0],
                local_mouse_pos[1],
            ):
                hovered_call_surface_idx = idx
                break

        if hovered_call_surface_idx is not None:
            call = self.__call_list[hovered_call_surface_idx]
            for tile in call.tiles:
                local_mouse = self.build_local_mouse(mouse_pos)
                if tile.get_position().collidepoint(
                    local_mouse[0] - surface_position[0],
                    local_mouse[1] - surface_position[1],
                ):
                    return [tile]

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
        self.__call_surface_position = []
        for call_surface in self.__call_surface:
            match self.player_idx:
                case 0:
                    start_width += call_surface.get_width()
                    surface_position = (self.surface.get_width() - start_width, 0)
                    self.surface.blit(call_surface, surface_position)

                case 1:
                    surface_position = (0, start_height)
                    self.surface.blit(call_surface, surface_position)
                    start_height += call_surface.get_height()

                case 2:
                    surface_position = (start_width, 0)
                    self.surface.blit(call_surface, surface_position)
                    start_width += call_surface.get_width()

                case 3:
                    start_height += call_surface.get_height()
                    surface_position = (0, self.surface.get_height() - start_height)
                    self.surface.blit(call_surface, surface_position)
            self.__call_surface_position.append(surface_position)

    def __build_tiles_position(self, call: Call, surface: Surface):
        start_width = 0
        start_height = 0

        # Handle for not kakan
        if not call.is_kakan:
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

        # Handle for kakan
        else:
            one_drawn_tile = list(
                filter(lambda tile: tile.source == TileSource.DRAW, call.tiles)
            )[-1]

            tmp_tile_list = call.tiles.copy()
            tmp_tile_list.remove(one_drawn_tile)

            match self.player_idx:
                case 0:
                    for tile in tmp_tile_list:
                        tile.update_position(
                            start_width,
                            surface.get_height() - tile.get_surface().get_height(),
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )
                        start_width += tile.get_surface().get_width()

                    one_drawn_tile.update_tile_surface((self.player_idx - 1) % 4)
                    one_drawn_tile.update_position(
                        call.another_player_tiles.get_position().x,
                        0,
                        one_drawn_tile.get_surface().get_width(),
                        one_drawn_tile.get_surface().get_height(),
                    )
                case 1:
                    for tile in tmp_tile_list:
                        start_height += tile.get_surface().get_height()
                        tile.update_position(
                            surface.get_width() - tile.get_surface().get_width(),
                            surface.get_height() - start_height,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )

                    one_drawn_tile.update_tile_surface((self.player_idx - 1) % 4)
                    one_drawn_tile.update_position(
                        0,
                        call.another_player_tiles.get_position().y,
                        one_drawn_tile.get_surface().get_width(),
                        one_drawn_tile.get_surface().get_height(),
                    )
                case 2:
                    for tile in tmp_tile_list:
                        start_width += tile.get_surface().get_width()

                        tile.update_position(
                            surface.get_width() - start_width,
                            0,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )

                    one_drawn_tile.update_tile_surface((self.player_idx - 1) % 4)
                    one_drawn_tile.update_position(
                        call.another_player_tiles.get_position().x,
                        call.another_player_tiles.get_surface().get_height(),
                        one_drawn_tile.get_surface().get_width(),
                        one_drawn_tile.get_surface().get_height(),
                    )
                case 3:
                    for tile in tmp_tile_list:
                        tile.update_position(
                            0,
                            start_height,
                            tile.get_surface().get_width(),
                            tile.get_surface().get_height(),
                        )
                        start_height += tile.get_surface().get_height()

                    one_drawn_tile.update_tile_surface((self.player_idx - 1) % 4)
                    one_drawn_tile.update_position(
                        call.another_player_tiles.get_surface().get_width(),
                        call.another_player_tiles.get_position().y,
                        one_drawn_tile.get_surface().get_width(),
                        one_drawn_tile.get_surface().get_height(),
                    )

    def build_call_surface(self):
        self.__call_surface = []
        for call in self.__call_list:
            # If not ANKAN, update sideway surface for tile
            if not (call.type == CallType.KAN and call.another_player_tiles is None):
                for tile in call.tiles:
                    reveal_surface = tile.tiles_cutter.cut_tiles(
                        tile.type, tile.number, tile.aka, self.player_idx
                    )
                    tile.update_tile_surface(reveal_surface=reveal_surface)
                    tile.hidden = False
                call.another_player_tiles.update_tile_surface((self.player_idx - 1) % 4)
            else:
                tiles_list = call.tiles
                tiles_list[0].hidden = True
                tiles_list[-1].hidden = True
                tiles_list[1].hidden = False
                tiles_list[2].hidden = False
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
                if not call.is_kakan:
                    for tile in call.tiles:
                        surface_width += tile.get_surface().get_width()
                else:
                    surface_width += call.another_player_tiles.get_surface().get_width()
                    for tile in [
                        tmp_tile
                        for tmp_tile in call.tiles
                        if tmp_tile != call.another_player_tiles
                        and tmp_tile.get_surface().get_size()
                        != call.another_player_tiles.get_surface().get_size()
                    ][0:2]:

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
                if not call.is_kakan:
                    for tile in call.tiles:
                        surface_height += tile.get_surface().get_height()
                else:
                    surface_height += (
                        call.another_player_tiles.get_surface().get_height()
                    )
                    for tile in [
                        tmp_tile
                        for tmp_tile in call.tiles
                        if tmp_tile != call.another_player_tiles
                        and tmp_tile.get_surface().get_size()
                        != call.another_player_tiles.get_surface().get_size()
                    ][0:2]:
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
