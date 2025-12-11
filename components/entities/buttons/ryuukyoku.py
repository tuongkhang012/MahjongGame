from components.entities.buttons.call_button import CallButton
from pygame.freetype import Font
from utils.constants import (
    CHI_PON_KAN_FONT_SIZE,
    MADOU_FUTO_FONT,
    CALL_TEXT_COLOR,
    CALL_BUTTON_COLORS,
)


class Ryuukyoku(CallButton):
    def __init__(self):
        super().__init__(
            Ryuukyoku.__name__,
            Font(MADOU_FUTO_FONT, CHI_PON_KAN_FONT_SIZE),
            text_color=CALL_TEXT_COLOR,
            bg_color=CALL_BUTTON_COLORS[Ryuukyoku.__name__],
        )
