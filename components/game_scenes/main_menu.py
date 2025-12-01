import typing
import pygame
from pygame import Surface, Color, Rect
from components.entities.buttons.ui_button import UIButton

from utils.constants import (
    MAIN_MENU_BACKGROUND,
    MINTSODA_FONT,
    UI_FONT_SIZE,
    UI_TEXT_COLOR,
    UI_BUTTON_COLOR,
    UI_BUTTON_SIZE,
    COLOR_WHITE,
)
from pygame.freetype import Font
from pygame.event import Event
from utils.helper import build_center_rect, draw_hitbox
from utils.enums import GameScene

if typing.TYPE_CHECKING:
    from components.game_scenes.scenes_controller import ScenesController


class MainMenu:
    screen: Surface
    scenes_controller: "ScenesController"

    __absolute_position: Rect = None

    def __init__(self, screen: Surface, scenes_controller: "ScenesController"):
        self.main_screen = screen
        self.screen = screen.copy()
        self.scenes_controller = scenes_controller
        self.bg_image = pygame.image.load(MAIN_MENU_BACKGROUND)
        self.start_button = UIButton(
            text="Start Game",
            font=Font(MINTSODA_FONT, UI_FONT_SIZE),
            text_color=UI_TEXT_COLOR,
            bg_color=UI_BUTTON_COLOR,
            border_color=COLOR_WHITE,
        )
        self.continue_button = UIButton(
            text="Continue",
            font=Font(MINTSODA_FONT, UI_FONT_SIZE),
            text_color=UI_TEXT_COLOR,
            bg_color=UI_BUTTON_COLOR,
            border_color=COLOR_WHITE,
        )
        self.continue_button.disabled()
        self.instruction_button = UIButton(
            text="How to play",
            font=Font(MINTSODA_FONT, UI_FONT_SIZE),
            text_color=UI_TEXT_COLOR,
            bg_color=UI_BUTTON_COLOR,
            border_color=COLOR_WHITE,
        )
        self.quit_button = UIButton(
            text="Quit",
            font=Font(MINTSODA_FONT, UI_FONT_SIZE),
            text_color=UI_TEXT_COLOR,
            bg_color=UI_BUTTON_COLOR,
            border_color=COLOR_WHITE,
        )

    def render(self) -> Surface:
        self.screen.blit(self.bg_image, (0, 0))

        # Render main menu elements here
        main_menu_buttons_surface = Surface(
            (UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1] * 4), pygame.SRCALPHA
        )
        self.draw_border(
            main_menu_buttons_surface,
            Color(0, 0, 0, int(255 * 0.8)),
            Color(255, 255, 255),
        )

        # Start Button
        self.start_button.update_position(0, 0, UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1])
        self.start_button.render(main_menu_buttons_surface)
        # Continue Button
        self.continue_button.update_position(
            0, UI_BUTTON_SIZE[1], UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1]
        )
        self.continue_button.render(main_menu_buttons_surface)

        # Instruction Button
        self.instruction_button.update_position(
            0, UI_BUTTON_SIZE[1] * 2, UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1]
        )
        self.instruction_button.render(main_menu_buttons_surface)

        # Quit Button
        self.quit_button.update_position(
            0, UI_BUTTON_SIZE[1] * 3, UI_BUTTON_SIZE[0], UI_BUTTON_SIZE[1]
        )
        self.quit_button.render(main_menu_buttons_surface)

        # self.start_button.render(self.screen)
        draw_hitbox(main_menu_buttons_surface)
        center_pos = build_center_rect(self.screen, main_menu_buttons_surface)
        self.screen.blit(main_menu_buttons_surface, (center_pos.x, 380))
        self.__absolute_position = Rect(
            center_pos.x, 380, self.screen.get_width(), self.screen.get_height()
        )
        self.main_screen.blit(self.screen, (0, 0))
        return self.main_screen

    def handle_event(self, event: Event):
        local_mouse = (
            event.pos[0] - self.__absolute_position.x,
            event.pos[1] - self.__absolute_position.y,
        )
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                # Click start button
                if (
                    self.start_button.check_collidepoint(local_mouse)
                    and self.start_button.is_disabled == False
                ):
                    self.scenes_controller.change_scene(scene=GameScene.GAME)

                # Click continue button
                if (
                    self.continue_button.check_collidepoint(local_mouse)
                    and self.start_button.is_disabled == False
                ):
                    pass

                if self.instruction_button.check_collidepoint(local_mouse):
                    pass

                # Click quit button
                if (
                    self.quit_button.check_collidepoint(local_mouse)
                    and self.start_button.is_disabled == False
                ):
                    return True

            case pygame.MOUSEMOTION:
                self.start_button.unhovered()
                self.continue_button.unhovered()
                self.instruction_button.unhovered()
                self.quit_button.unhovered()

                is_hovering = False
                if self.start_button.check_collidepoint(local_mouse):
                    self.start_button.hovered()
                    is_hovering = (
                        True if self.start_button.is_disabled == False else False
                    )
                if self.continue_button.check_collidepoint(local_mouse):
                    self.continue_button.hovered()
                    is_hovering = (
                        True if self.continue_button.is_disabled == False else False
                    )
                if self.instruction_button.check_collidepoint(local_mouse):
                    self.instruction_button.hovered()
                    is_hovering = (
                        True if self.instruction_button.is_disabled == False else False
                    )
                if self.quit_button.check_collidepoint(local_mouse):
                    self.quit_button.hovered()
                    is_hovering = (
                        True if self.quit_button.is_disabled == False else False
                    )
                if is_hovering:
                    self.scenes_controller.mouse.hover()
                else:
                    self.scenes_controller.mouse.default()

    def draw_border(self, surface: Surface, bg_color: Color, border_color: Color):
        pygame.draw.rect(
            surface,
            bg_color,
            surface.get_rect(),
            border_radius=10,
        )

        pygame.draw.rect(surface, border_color, surface.get_rect(), 2, border_radius=10)
