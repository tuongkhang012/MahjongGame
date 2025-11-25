from components.entities.buttons.call_button import CallButton
from pygame.freetype import Font
from utils.constants import (
    CHI_PON_KAN_FONT_SIZE,
    MADOU_FUTO_FONT,
    CALL_TEXT_COLOR,
    CALL_BUTTON_COLORS,
)
from pygame import Surface, Rect
import pygame
from utils.helper import build_center_rect


class Tsumo(CallButton):
    def __init__(self):
        super().__init__(
            Tsumo.__name__,
            Font(MADOU_FUTO_FONT, CHI_PON_KAN_FONT_SIZE),
            text_color=CALL_TEXT_COLOR,
            bg_color=CALL_BUTTON_COLORS[Tsumo.__name__],
        )
