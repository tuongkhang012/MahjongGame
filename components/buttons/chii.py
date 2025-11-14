from components.buttons.call_button import CallButton
from pygame.freetype import Font
from utils.constants import (
    CHI_PON_KAN_FONT_SIZE,
    MADOU_FUTO_FONT,
    CALL__BUTTON_COLORS,
    CALL_TEXT_COLOR,
)
from pygame import Surface, Rect
import pygame
from utils.helper import build_center_rect


class Chii(CallButton):
    def __init__(self):
        super().__init__(
            Chii.__name__,
            Font(MADOU_FUTO_FONT, CHI_PON_KAN_FONT_SIZE),
            text_color=CALL_TEXT_COLOR,
            bg_color=CALL__BUTTON_COLORS[Chii.__name__],
        )
