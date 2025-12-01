from components.entities.buttons.button import Button
from pygame.freetype import Font
from pygame import Surface, Rect, Color
import sys
import pygame
from utils.constants import UI_BUTTON_SIZE
from utils.helper import build_center_rect


class UIButton(Button):
    def __init__(
        self,
        text: str,
        font: Font,
        text_color: Color,
        bg_color: Color,
        border_color: Color,
    ):
        super().__init__(text, font, text_color)

        # Text Color
        self.text_color = text_color

        # Background color
        self.bg_color = bg_color
        self.border_color = border_color

        self.button_size = UI_BUTTON_SIZE

        # Init button
        self.init_button()

    def render(self, surface: Surface):
        if self.is_disabled:
            self.surface = self._disable_surface
        elif self.is_hovered:
            self.surface = self._highlight_surface
        else:
            self.surface = self._original_surface

        surface.blit(self.surface, (self.get_position().x, self.get_position().y))

    def init_button(self):
        self.hidden = True
        self.surface = self.__create_new_surface()

    def draw_hitbox(surface: Surface, color: Color = (255, 0, 0)) -> None:
        if len(sys.argv) > 1 and "debug" in sys.argv:
            pygame.draw.rect(surface, color, surface.get_rect(), 2)

    def __create_new_surface(self) -> Surface:
        reveal_surface = Surface(self.button_size, pygame.SRCALPHA)

        text_surface = self._build_text_surface()
        text_pos = build_center_rect(reveal_surface, text_surface)
        reveal_surface.blit(text_surface, (text_pos.x, text_pos.y))

        self._original_surface = reveal_surface
        self._highlight_surface = self._create_highlight_surface(
            reveal_surface, pygame.Color(255, 247, 0, 160)
        )
        self._disable_surface = self._create_highlight_surface(
            reveal_surface, pygame.Color(0, 0, 0, 128)
        )

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
