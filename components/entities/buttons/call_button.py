from components.entities.buttons.button import Button
from pygame.freetype import Font
from pygame import Surface, Rect, Color
import pygame
from utils.helper import build_center_rect
from utils.constants import CALL_BUTTON_SIZE, SMOKE_PARTICLE_IMAGE_LINK
from shared.image_cutter import ImageCutter


class CallButton(Button):
    _smoke_base_frames: list[Surface] | None = None # Shared smoke frames for all call buttons
    def __init__(self, text: str, font: Font, text_color: Color, bg_color: Color):
        super().__init__(text, font, text_color)

        # Text Color
        self.text_color = text_color

        # Backgroun color
        self.bg_color = bg_color
        self.smoke_frames: list[Surface] = self._build_smoke_frames()

        # Init call button size
        self.button_size = CALL_BUTTON_SIZE

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
        self.draw_rect()

    def __create_new_surface(self) -> Surface:
        return Surface(self.button_size, pygame.SRCALPHA)

    @classmethod
    def _get_smoke_base_frames(cls) -> list[Surface]:
        if cls._smoke_base_frames is None:
            cls._smoke_base_frames = ImageCutter.load_frames_from_folder(SMOKE_PARTICLE_IMAGE_LINK, 4)
        return cls._smoke_base_frames

    def _build_smoke_frames(self) -> list[Surface]:
        base_frames = self._get_smoke_base_frames()
        color = self.bg_color
        return [ImageCutter.tint_surface(frame, color) for frame in base_frames]

    def get_smoke_frames(self) -> list[Surface]:
        return self.smoke_frames
