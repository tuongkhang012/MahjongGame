from utils.enums import TilesType
import pygame
from pygame import Rect, Surface
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK


class Tile:
    def __init__(self, type: TilesType, number: int, aka: bool = False):
        # Tile standard attributes
        self.type = type
        self.number = number
        self.aka = aka
        self.hidden = True

        # Tile position
        self.__position = Rect(0, 0, 0, 0)
        self.__base_position = Rect(0, 0, 0, 0)

        # Tile surface
        self.__surface = None
        self.__hidden_surface = None
        self.__original_surface = None
        self.__highlight_surface = None

        # Flag attribute
        self.is_clicked = False
        self.is_hovered = False
        self.is_highlighted = False

        # Hovering section
        self.hover_offset_y = 12
        self.animation_speed = 0.1

        # Image Cutter for tile surface
        self.tiles_cutter = TilesCutter(TILES_IMAGE_LINK)

    def clicked(self):
        self.is_clicked = not self.hidden and True

    def unclicked(self):
        self.is_clicked = not self.hidden and False

    def hovered(self):
        self.is_hovered = not self.hidden and True

    def unhovered(self):
        self.is_hovered = not self.hidden and False

    def highlighted(self):
        self.is_highlighted = not self.hidden and True

    def unhighlighted(self):
        self.is_highlighted = not self.hidden and False

    def update(self):
        """Handles all frame-by-frame logic, like animation."""
        if self.hidden:
            return

        self.handle_hover()
        self.handle_highlight()

    def handle_hover(self):
        target_y = self.__position.y
        if self.is_hovered:
            target_y = self.__base_position.y - self.hover_offset_y

        distance_y = target_y - self.__position.y

        if abs(distance_y) > 0.1:
            self.__position.y += distance_y * self.animation_speed
        else:
            self.__position.y = self.__base_position.y

    def handle_highlight(self):
        if self.is_highlighted:
            self.__surface = self.__highlight_surface
        else:
            self.__surface = self.__original_surface

    def check_collidepoint(self, position: tuple[int, int]) -> bool:
        return (
            self.__position.collidepoint(position[0], position[1])
            if self.__position is not None
            else False
        )

    def render(self, screen: Surface):
        if self.hidden:
            screen.blit(self.__hidden_surface, (self.__position.x, self.__position.y))
        else:
            screen.blit(self.__surface, (self.__position.x, self.__position.y))

    def update_position(self, x: float, y: float, width: float, height: float):
        self.__position.x = x
        self.__position.y = y
        self.__position.width = width
        self.__position.height = height

        # Store for base value, whenever bobbing effect
        self.__base_position.x = x
        self.__base_position.y = y
        self.__base_position.width = width
        self.__base_position.height = height

    def create_highlight_surface(self, surface: Surface) -> Surface:
        """Creates a highlighted version of the input surface."""
        # Create a copy to draw on
        # .convert_alpha() ensures it has the correct pixel format for transparency
        hover_surface = surface.copy().convert_alpha()

        # Define the highlight: white, with 40/255 alpha (about 15% opacity)
        highlight_color = (255, 247, 0, 180)

        # Fill the surface with this color using an "ADD" blend mode.
        # This brightens the image without washing it out.
        hover_surface.fill(highlight_color, None, pygame.BLEND_RGBA_MULT)

        return hover_surface

    def update_tile_surface(self, player_idx: int) -> None:
        hidden_surface = self.tiles_cutter.cut_hidden_tiles(True, player_idx)
        reveal_surface = self.tiles_cutter.cut_tiles(
            self.type, self.number, self.aka, player_idx
        )

        self.__surface = reveal_surface
        self.__original_surface = reveal_surface
        self.__highlight_surface = self.create_highlight_surface(reveal_surface)

        self.__hidden_surface = hidden_surface

    def get_position(self):
        return self.__position

    def get_surface(self):
        return self.__surface

    def get_hidden_surface(self):
        return self.__hidden_surface

    def reveal(self):
        self.hidden = False

    def hide(self):
        self.hidden = True
