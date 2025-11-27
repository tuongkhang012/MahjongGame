import typing
from pygame import Surface
from components.entities.buttons.ui_button import UIButton
from utils.constants import MADOU_FUTO_FONT, ANMOTALES_FONT, MINTSODA_FONT, PIXELARI_FONT, UI_FONT_SIZE, UI_TEXT_COLOR, \
    UI_BUTTON_COLOR, UI_BUTTON_SIZE
from pygame.freetype import Font
from utils.helper import build_center_rect
from components.events.mouse_button_down_MM import MouseButtonDown

if typing.TYPE_CHECKING:
    from components.game_scenes.scenes_controller import ScenesController


class MainMenu:
    screen: Surface
    scenes_controller: "ScenesController"

    def __init__(self, screen: Surface, scenes_controller: "ScenesController"):
        self.main_screen = screen
        self.screen = screen.copy()
        self.scenes_controller = scenes_controller

        self.start_button = UIButton(
            text="Start Game",
            font=Font(MINTSODA_FONT, UI_FONT_SIZE),
            text_color=UI_TEXT_COLOR,
            bg_color=UI_BUTTON_COLOR,
        )

        self.mouse_button_down = MouseButtonDown(
            screen=self.screen,
            main_menu=self,
        )

    def render(self) -> Surface:
        self.screen.fill((0, 0, 0))
        # Render main menu elements here
        screen_center = build_center_rect(self.screen, self.start_button.surface)
        self.start_button.update_position(
            screen_center.x,
            screen_center.y,
            UI_BUTTON_SIZE[0],
            UI_BUTTON_SIZE[1],
        )
        self.start_button.render(self.screen)
        self.main_screen.blit(self.screen, (0, 0))

        return self.main_screen

    def update(self):
        pass
