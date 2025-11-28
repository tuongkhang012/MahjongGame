import typing
import pygame
from pygame import Surface
from components.entities.buttons.ui_button import UIButton
from utils.constants import (
    MADOU_FUTO_FONT,
    ANMOTALES_FONT,
    MINTSODA_FONT,
    PIXELARI_FONT,
    UI_FONT_SIZE,
    UI_TEXT_COLOR,
    UI_BUTTON_COLOR,
    UI_BUTTON_SIZE,
    COLOR_BLACK,
)
from pygame.freetype import Font
from pygame.event import Event
from utils.helper import build_center_rect
from utils.enums import GameScene

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
            border_color=COLOR_BLACK,
        )

    def render(self) -> Surface:
        self.screen.fill((252, 3, 136))
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

    def handle_event(self, event: Event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.start_button.check_collidepoint(event.pos):
                    self.scenes_controller.change_scene(
                        scene=GameScene.GAME
                    )
            case pygame.MOUSEMOTION:
                pass
