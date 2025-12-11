from utils.enums import TileType, TileSource
import pygame
from pygame import Surface
from shared.image_cutter import ImageCutter
from utils.constants import TILES_IMAGE_LINK, TILE_ANIMATION_DURATION
from utils.helper import draw_hitbox, convert_tile_to_hand34_index
from components.entities.buttons.button import Button
import sys


class Tile(Button):
    source: TileSource
    from_death_wall: bool = False

    # Tile properties
    type: TileType
    number: int
    aka: bool
    hand136_idx: int
    hand34_idx: int
    name: str  # This is the name for naming in mahjong, use __str__ for AI

    # Hovering animation
    hover_offset_y: float = 12
    animation_speed: float = 0.5
    animation_duration: float = TILE_ANIMATION_DURATION

    # Riichi relative
    __is_riichi_discard: bool  # Is a riichi discard

    def __init__(
        self, idx: int, type: TileType, number: int, name: str, aka: bool = False
    ):
        super().__init__()
        # Tile standard attributes
        self.type = type
        self.number = number
        self.aka = aka
        if len(sys.argv) > 1 and "debug" in sys.argv:
            self.hidden = False
        else:
            self.hidden = True

        # Hovering section
        self.hover_offset_y = 12
        self.animation_speed = 0.5
        self.animation_duration = TILE_ANIMATION_DURATION

        # Hand index
        self.hand34_idx = convert_tile_to_hand34_index(self)
        self.hand136_idx = idx
        self.name = name
        # Image Cutter for tile surface
        self.tiles_cutter = ImageCutter(TILES_IMAGE_LINK)

        # Riichi discard Tile
        self.__is_riichi_discard: bool = False
        self.source = TileSource.DRAW

    def update_hover(self):
        """Handles all frame-by-frame logic, like animation."""
        if self.hidden:
            return

        self.__handle_hover()

    def __handle_hover(self):
        if self._position.y == self._base_position.y - self.hover_offset_y:
            return
        target_y = self._position.y
        if self.is_hovered:
            target_y = self._base_position.y - self.hover_offset_y

        distance_y = target_y - self._position.y

        if abs(distance_y) > 0.1:
            self._position.y += distance_y * self.animation_speed
        else:
            self._position.y = self._base_position.y

    def render(self, screen: Surface):
        if self.hidden:
            self.set_surface(self._hidden_surface)
        elif self.is_disabled:
            self.set_surface(self._disable_surface)
        elif self.is_highlighted:
            self.set_surface(self._highlight_surface)
        else:
            self.set_surface(self._original_surface)

        draw_hitbox(self.surface)
        screen.blit(self.surface, (self._position.x, self._position.y))

    def update_tile_surface(
        self,
        player_idx: int = None,
        reveal_surface: Surface = None,
        hidden_surface: Surface = None,
    ) -> None:
        if hidden_surface is None and player_idx is not None:
            hidden_surface = self.tiles_cutter.cut_hidden_tiles(True, player_idx)

        if reveal_surface is None and player_idx is not None:
            reveal_surface = self.tiles_cutter.cut_tiles(
                self.type, self.number, self.aka, player_idx
            )
        if reveal_surface:
            self.surface = reveal_surface
            self._original_surface = reveal_surface
            self._highlight_surface = self._create_highlight_surface(
                reveal_surface, pygame.Color(255, 247, 0, 160)
            )
            self._disable_surface = self._create_highlight_surface(
                reveal_surface, pygame.Color(0, 0, 0, 128)
            )

        if hidden_surface:
            self._hidden_surface = hidden_surface

    def scale_surface(self, scale_by: float):
        self.surface = pygame.transform.scale_by(self.surface, scale_by)
        self._original_surface = pygame.transform.scale_by(
            self._original_surface, scale_by
        )
        self._highlight_surface = pygame.transform.scale_by(
            self._highlight_surface, scale_by
        )

        self._hidden_surface = pygame.transform.scale_by(self._hidden_surface, scale_by)

    def reveal(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def discard_riichi(self):
        self.__is_riichi_discard = True

    def undiscard_riichi(self):
        self.__is_riichi_discard = False

    def is_discard_from_riichi(self):
        return self.__is_riichi_discard

    def reset(self):
        self.__is_riichi_discard = False
        self.is_clicked = False
        self.is_highlighted = False
        self.is_hovered = False
        self.is_disabled = False
        self.hidden = True
        self.source = None
        self.from_death_wall = False

    def __eq__(self, other):
        if not isinstance(other, Tile):  # Optional: ensure comparison with same type
            return NotImplemented
        return id(self) == id(other)

    def __str__(self, full: bool = False):
        if not full:
            tile_type = None
            match self.type:
                case TileType.SOU:
                    tile_type = "s"
                case TileType.PIN:
                    tile_type = "p"
                case TileType.MAN:
                    tile_type = "m"
                case TileType.DRAGON:
                    if self.number == 1:
                        return "P"
                    elif self.number == 2:
                        return "F"
                    elif self.number == 3:
                        return "C"
                case TileType.WIND:
                    if self.number == 1:
                        return "E"
                    elif self.number == 2:
                        return "S"
                    elif self.number == 3:
                        return "W"
                    elif self.number == 4:
                        return "N"
            return f"{self.number}{tile_type}{'r' if self.aka else ''}"

        return f"{self.type} {self.number} FROM {self.source}"

    def __repr__(self, full: bool = False):
        if not full:
            tile_type = None
            match self.type:
                case TileType.SOU:
                    tile_type = "s"
                case TileType.PIN:
                    tile_type = "p"
                case TileType.MAN:
                    tile_type = "m"
                case TileType.DRAGON:
                    if self.number == 1:
                        return "P"
                    elif self.number == 2:
                        return "F"
                    elif self.number == 3:
                        return "C"
                case TileType.WIND:
                    if self.number == 1:
                        return "E"
                    elif self.number == 2:
                        return "S"
                    elif self.number == 3:
                        return "W"
                    elif self.number == 4:
                        return "N"
            return f"{self.number}{tile_type}{'r' if self.aka else ''}"

        return f"{self.type} {self.number} FROM {self.source}"
