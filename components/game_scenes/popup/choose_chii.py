from components.game_scenes.popup.popup import Popup
from components.entities.buttons.tile import Tile
from components.entities.call import Call
from pygame.freetype import Font
from utils.constants import ANCIENT_MODERN_FONT, COLOR_BLACK, CALL_BUTTON_SIZE
from pygame import Surface, Rect
from pygame.event import Event
import pygame
from utils.helper import draw_hitbox, build_center_rect


class ChiiPicker(Popup):
    callable_list: list[list[Tile]]
    call_tile: Tile

    # List of callable surface
    callable_list_surfaces: list[Surface] = []
    callable_list_positions: list[Rect] = []

    def __init__(self, callable_list: list[list[Tile]], call_tile: Tile):
        super().__init__()

        self.callable_list = callable_list
        self.call_tile = call_tile
        self.bg_color = "grey"
        self.padding_each_callable = 20
        self.popup_padding = 6

    def render(self, screen: Surface):
        self.build_call_picker_surface()
        draw_hitbox(self._surface, (255, 255, 0))
        center_pos = build_center_rect(screen, self._surface)
        screen.blit(
            self._surface,
            (
                center_pos.x,
                (4 * screen.get_height() / 5)
                - self._surface.get_height()
                - CALL_BUTTON_SIZE[1]
                - self.popup_padding,
            ),
        )
        self.update_absolute_position_rect(
            Rect(
                center_pos.x,
                (4 * screen.get_height() / 5)
                - self._surface.get_height()
                - CALL_BUTTON_SIZE[1]
                - self.popup_padding,
                self._surface.get_width(),
                self._surface.get_height(),
            ),
        )

    def build_call_picker_surface(self):
        # Build text
        choose_text_font = Font(ANCIENT_MODERN_FONT, 20)
        choose_text_surface, _ = choose_text_font.render("Choose", COLOR_BLACK)

        # Build surface for call tiles
        self.callable_list_surfaces: list[Surface] = []
        all_tiles_surface: list[list[Surface]] = []
        for call_tiles in self.callable_list:
            tile_surfaces_list: list[Surface] = []
            for tile in call_tiles:
                if tile == self.call_tile:
                    continue
                tile_surface = tile.get_surface().copy()
                tile_surface = pygame.transform.scale_by(tile_surface, 0.8)
                tile_surfaces_list.append(tile_surface)
            all_tiles_surface.append(tile_surfaces_list)
            self.callable_list_surfaces.append(
                Surface(
                    (
                        sum([surface.get_width() for surface in tile_surfaces_list]),
                        tile_surface.get_height(),
                    ),
                    pygame.SRCALPHA,
                ),
            )

        max_callable_surface_width = sum(
            [surface.get_width() for surface in self.callable_list_surfaces]
        ) + (len(self.callable_list_surfaces) - 1) * (self.padding_each_callable)

        max_callable_surface_height = max(
            list(map(lambda surface: surface.get_height(), self.callable_list_surfaces))
        )

        # Wrap popup surface
        self._surface = Surface(
            (
                max(choose_text_surface.get_width(), max_callable_surface_width)
                + self.popup_padding * 2,
                max_callable_surface_height
                + choose_text_surface.get_height()
                + self.popup_padding * 3,
            ),
            pygame.SRCALPHA,
        )
        self.draw_border_radius()

        # Draw on that popup surface
        center_pos = build_center_rect(self._surface, choose_text_surface)
        self._surface.blit(choose_text_surface, (center_pos.x, self.popup_padding))

        # Tile surfaces
        picker_surface = Surface(
            (max_callable_surface_width, max_callable_surface_height), pygame.SRCALPHA
        )
        start_width = 0
        for idx, surface in enumerate(self.callable_list_surfaces):
            for tile_idx, tile_surface in enumerate(all_tiles_surface[idx]):
                surface.blit(tile_surface, (tile_idx * tile_surface.get_width(), 0))
            picker_surface.blit(surface, (start_width, 0))
            self.callable_list_positions.append(
                Rect(
                    (
                        start_width,
                        choose_text_surface.get_height() + self.popup_padding * 2,
                        surface.get_width(),
                        surface.get_height(),
                    )
                )
            )
            start_width += surface.get_width() + self.padding_each_callable

        center_pos = build_center_rect(self._surface, picker_surface)
        self._surface.blit(
            picker_surface,
            (center_pos.x, choose_text_surface.get_height() + self.popup_padding * 2),
        )

    def handle_event(self, mouse_pos: tuple[int, int]) -> list[Tile] | None:
        local_mouse = self.build_local_mouse(mouse_pos)

        for idx, rect in enumerate(self.callable_list_positions):
            if rect.collidepoint(local_mouse[0], local_mouse[1]):
                return self.callable_list[idx]

        return None
