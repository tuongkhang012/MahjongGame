from utils.enums import TileType, TileSource
import pygame
from pygame import Surface
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK, TILE_ANIMATION_DURATION
from components.buttons.button import Button
import typing

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class Tile(Button):
    source: TileSource

    def __init__(self, type: TileType, number: int, aka: bool = False):
        super().__init__()
        # Tile standard attributes
        self.type = type
        self.number = number
        self.aka = aka
        self.hidden = True

        # Hovering section
        self.hover_offset_y = 12
        self.animation_speed = 0.5
        self.animation_duration = TILE_ANIMATION_DURATION

        # Image Cutter for tile surface
        self.tiles_cutter = TilesCutter(TILES_IMAGE_LINK)

    def update_hover(self):
        """Handles all frame-by-frame logic, like animation."""
        if self.hidden:
            return

        self.handle_hover()
        self.handle_highlight()

    def update_clicked(self, game_manager: "GameManager"):
        self.handle_clicked(game_manager)

    def handle_hover(self):
        target_y = self._position.y
        if self.is_hovered:
            target_y = self._base_position.y - self.hover_offset_y

        distance_y = target_y - self._position.y

        if abs(distance_y) > 0.1:
            self._position.y += distance_y * self.animation_speed
        else:
            self._position.y = self._base_position.y

    def handle_highlight(self):
        if self.is_highlighted:
            self._surface = self._highlight_surface
        else:
            self._surface = self._original_surface

    def handle_clicked(self, game_manager: "GameManager"):
        if self.is_clicked:
            game_manager.start_discarded_animation(self)

    def render(self, screen: Surface):
        if self.hidden:
            self._surface = self._hidden_surface
        else:
            self._surface = self._original_surface

        screen.blit(self._surface, (self._position.x, self._position.y))

    def update_tile_surface(self, player_idx: int) -> None:
        hidden_surface = self.tiles_cutter.cut_hidden_tiles(True, player_idx)
        reveal_surface = self.tiles_cutter.cut_tiles(
            self.type, self.number, self.aka, player_idx
        )

        self._surface = reveal_surface
        self._original_surface = reveal_surface
        self._highlight_surface = self._create_highlight_surface(
            reveal_surface, pygame.Color(255, 247, 0, 180)
        )

        self._hidden_surface = hidden_surface

    def reveal(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def __eq__(self, other):
        if not isinstance(other, Tile):  # Optional: ensure comparison with same type
            return NotImplemented
        return id(self) == id(other)
