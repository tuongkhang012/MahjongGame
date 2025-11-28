from components.entities.buttons.button import Button
from pygame.freetype import Font
from pygame import Surface, Rect, Color
import sys
import pygame
from utils.constants import UI_BUTTON_SIZE
from utils.helper import build_center_rect


class UIButton(Button):
    def __init__(self, text: str, font: Font, text_color: Color, bg_color: Color, border_color: Color):
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
        text_surface = self._build_text_surface()
        text_pos = build_center_rect(self.surface, text_surface)
        self.surface.blit(text_surface, (text_pos.x, text_pos.y))
        surface.blit(self.surface, (self.get_position().x, self.get_position().y))

    def init_button(self):
        self.hidden = True
        self.surface = self.__create_new_surface()
        self.draw_rect(self.border_color)

    def draw_hitbox(surface: Surface, color: Color = (255, 0, 0)) -> None:
        if len(sys.argv) > 1 and "debug" in sys.argv:
            pygame.draw.rect(surface, color, surface.get_rect(), 2)

    def __create_new_surface(self) -> Surface:
        return Surface(self.button_size, pygame.SRCALPHA)

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