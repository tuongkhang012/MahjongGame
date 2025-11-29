from pygame import Rect, Color, Surface
from pygame.freetype import Font
import pygame
from utils.helper import build_center_rect


class Button:
    # Button surface
    surface: Surface = None
    _original_surface: Surface = None
    _highlight_surface: Surface = None
    _hidden_surface: Surface = None
    _disable_surface: Surface = None

    # Position of button
    _position: Rect
    _base_position: Rect

    # Button properties
    text: str
    color: Color
    hidden: bool
    hover_color: Color

    # Button state
    is_hovered: bool
    is_clicked: bool
    is_highlighted: bool
    is_disabled: bool

    # Timer
    animation_timer: float
    animation_duration: float

    def __init__(
        self,
        text: str = None,
        font: Font = None,
        text_color: Color = None,
        bg_color: Color = None,
        hover_color: Color = None,
    ):
        # Screen relative
        self._position = Rect(0, 0, 0, 0)
        self._base_position = Rect(0, 0, 0, 0)

        # Button information
        self.text = text
        self.font = font
        self.text_color = text_color

        # Button color
        self.bg_color = bg_color
        self.hover_color = hover_color

        # Button state
        self.is_hovered = False
        self.is_clicked = False
        self.is_highlighted = False
        self.is_disabled = False

        # Timer
        self.animation_timer = 0.0
        self.animation_duration = 1.0

    def set_surface(self, surface: Surface, bgColor: Color = None):
        if bgColor:
            surface.fill(bgColor)
        self.surface = surface

    def render(self, screen: Surface):
        if self.surface:
            text_surface = self._build_text_surface()
            text_pos = build_center_rect(self.surface, text_surface)
            self.surface.blit(text_surface, (text_pos.x, text_pos.y))

            screen.blit(self.surface, (self.get_position().x, self.get_position().y))

    def _build_text_surface(self) -> Surface:
        text_surface, _ = self.font.render(self.text, self.text_color)

        return text_surface

    def update_position(
        self,
        x: float,
        y: float,
        width: float = None,
        height: float = None,
    ):
        self._position.x = x
        self._position.y = y
        if width is not None:
            self._position.width = width
        if height is not None:
            self._position.height = height

        # Store for base value, whenever bobbing effect
        self._base_position.x = x
        self._base_position.y = y
        if width is not None:
            self._base_position.width = width
        if height is not None:
            self._base_position.height = height

    def clicked(self):
        self.is_clicked = True

    def unclicked(self):
        self.is_clicked = False

    def hovered(self):
        self.is_hovered = True

    def unhovered(self):
        self.is_hovered = False

    def highlighted(self):
        self.is_highlighted = True

    def unhighlighted(self):
        self.is_highlighted = False

    def disabled(self):
        self.is_disabled = True

    def undisabled(self):
        self.is_disabled = False

    def check_collidepoint(self, position: tuple[int, int]) -> bool:
        return (
            self.get_position().collidepoint(position[0], position[1])
            if self.get_position() is not None
            else False
        )

    def _create_highlight_surface(
        self, surface: Surface, highlight_color: Color
    ) -> Surface:
        """Creates a highlighted version of the input surface."""
        # Create a copy to draw on
        # .convert_alpha() ensures it has the correct pixel format for transparency
        original_surface = surface.copy()
        mask = pygame.mask.from_surface(original_surface)
        # Fill the surface with this color using an "ADD" blend mode.
        # This brightens the image without washing it out.
        highlight_surface = mask.to_surface(
            setcolor=highlight_color, unsetcolor=(0, 0, 0, 0)
        )

        original_surface.blit(highlight_surface, (0, 0))

        return original_surface

    def get_position(self) -> Rect:
        return self._position

    def get_surface(self) -> Surface:
        return self.surface

    def get_hidden_surface(self):
        return self._hidden_surface

    def draw_rect(self, border_color: Color = (255, 255, 255)):
        pygame.draw.rect(
            self.surface,
            self.bg_color,
            self.surface.get_rect(),
            border_radius=10,
        )

        pygame.draw.rect(
            self.surface, border_color, self.surface.get_rect(), 2, border_radius=10
        )
