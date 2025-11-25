from components.entities.buttons.button import Button
from pygame.freetype import Font
from pygame import Surface, Rect, Color
import pygame
from utils.helper import build_center_rect
from utils.constants import CALL_BUTTON_SIZE


class CallButton(Button):
    def __init__(self, text: str, font: Font, text_color: Color, bg_color: Color):
        super().__init__(text, font, text_color)

        # Text Color
        self.text_color = text_color

        # Backgroun color
        self.bg_color = bg_color

        # Init call button size
        self.button_size = CALL_BUTTON_SIZE

        # Init button
        self.init_button()

    def render(self, surface: Surface):
        text_surface, text_rect = self.build_text_surface()
        text_pos = build_center_rect(self.surface, text_surface)
        self.surface.blit(text_surface, (text_pos.x, text_pos.y))
        surface.blit(self.surface, (self.get_position().x, self.get_position().y))

    def init_button(self):
        self.hidden = True
        self.surface = self.__create_new_surface()
        self.draw_rect()

    def __create_new_surface(self) -> Surface:
        return Surface(self.button_size, pygame.SRCALPHA)

    def draw_rect(self):
        pygame.draw.rect(
            self.surface,
            self.bg_color,
            self.surface.get_rect(),
            border_radius=10,
        )

        pygame.draw.rect(
            self.surface, (255, 255, 255), self.surface.get_rect(), 2, border_radius=10
        )
