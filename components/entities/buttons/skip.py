from components.entities.buttons.call_button import CallButton
from pygame.freetype import Font
from utils.constants import (
    CHI_PON_KAN_FONT_SIZE,
    MADOU_FUTO_FONT,
    CALL_BUTTON_COLORS,
    CALL_TEXT_COLOR,
)


class Skip(CallButton):
    def __init__(self):
        super().__init__(
            Skip.__name__,
            Font(MADOU_FUTO_FONT, CHI_PON_KAN_FONT_SIZE),
            text_color=CALL_TEXT_COLOR,
            bg_color=CALL_BUTTON_COLORS[Skip.__name__],
        )
