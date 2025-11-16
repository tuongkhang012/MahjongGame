from components.fields.field import Field
from pygame import Surface, Rect
from pygame.event import Event
import pygame
from utils.constants import CALL_BUTTON_SIZE
from utils.enums import CallType, ActionType
from utils.helper import build_center_rect, draw_hitbox

# All call buttons
from components.buttons.chii import Chii
from components.buttons.kan import Kan
from components.buttons.pon import Pon
from components.buttons.ron import Ron
from components.buttons.skip import Skip
from components.call import Call

import typing

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class CallButtonField(Field):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen = screen
        self.chii_button = Chii()
        self.kan_button = Kan()
        self.pon_button = Pon()
        self.ron_button = Ron()
        self.skip_button = Skip()

        self.space_between_each_button = 20
        self.render_button_list: list[Chii | Kan | Pon | Ron | Skip] = []

    def render(self, call_list: list[CallType]):
        self.build_surface(call_list)
        render_surface = Surface(
            (self.screen.get_width(), CALL_BUTTON_SIZE[1]), pygame.SRCALPHA
        )
        center_pos = build_center_rect(render_surface, self.surface)
        self._relative_position = center_pos
        render_surface.blit(self.surface, (center_pos.x, center_pos.y))
        draw_hitbox(render_surface)

        screen_pos = (0, 4 * self.screen.get_height() / 5 - CALL_BUTTON_SIZE[1])
        self.screen.blit(render_surface, screen_pos)
        self._absolute_position = Rect(
            screen_pos[0] + center_pos.x,
            screen_pos[1] + center_pos.y,
            render_surface.get_width(),
            render_surface.get_height(),
        )

    def build_surface(self, call_list: list[CallType]) -> Surface:
        self.render_button_list = []
        self.surface = Surface(
            (
                CALL_BUTTON_SIZE[0] * len(call_list)
                + self.space_between_each_button * (len(call_list) - 1),
                CALL_BUTTON_SIZE[1],
            ),
            pygame.SRCALPHA,
        )
        self.build_button_position(call_list)

        for button in self.render_button_list:
            button.render(self.surface)

        self.surface.blit(
            button.get_surface(), (button.get_position().x, button.get_position().y)
        )

    def build_button_position(self, call_list: list[CallType]):
        for idx, call_type in enumerate(call_list):
            match call_type:
                case CallType.SKIP:
                    self.skip_button.update_position(
                        idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button),
                        0,
                        CALL_BUTTON_SIZE[0],
                        CALL_BUTTON_SIZE[1],
                    )
                    self.render_button_list.append(self.skip_button)
                case CallType.CHII:
                    self.chii_button.update_position(
                        idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button),
                        0,
                        CALL_BUTTON_SIZE[0],
                        CALL_BUTTON_SIZE[1],
                    )
                    self.render_button_list.append(self.chii_button)
                case CallType.PON:
                    self.pon_button.update_position(
                        idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button),
                        0,
                        CALL_BUTTON_SIZE[0],
                        CALL_BUTTON_SIZE[1],
                    )
                    self.render_button_list.append(self.pon_button)
                case CallType.KAN:
                    self.kan_button.update_position(
                        idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button),
                        0,
                        CALL_BUTTON_SIZE[0],
                        CALL_BUTTON_SIZE[1],
                    )
                    self.render_button_list.append(self.kan_button)
                case CallType.RON:
                    self.ron_button.update_position(
                        idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button),
                        0,
                        CALL_BUTTON_SIZE[0],
                        CALL_BUTTON_SIZE[1],
                    )
                    self.render_button_list.append(self.ron_button)

    def hover(self, event: Event) -> bool:
        local_mouse = self.build_local_mouse(event.pos)
        is_hovering_button = False
        for button in self.render_button_list:
            if button.check_collidepoint(local_mouse):
                is_hovering_button = True
                button.hovered()
                break

        for button in self.render_button_list:
            if not button.check_collidepoint(local_mouse):
                button.unhovered()

        return is_hovering_button

    def unhover(self):
        for button in self.render_button_list:
            button.unhovered()

    def click(self, event: Event, game_manager: "GameManager"):
        local_mouse = self.build_local_mouse(event.pos)

        for button in self.render_button_list:
            if button.check_collidepoint(local_mouse):
                print(f"CLICKING BUTTON {button.text.upper()}")
                if isinstance(button, Chii):
                    game_manager.action = ActionType.CHII
                elif isinstance(button, Skip):
                    game_manager.action = ActionType.SKIP
                elif isinstance(button, Pon):
                    game_manager.action = ActionType.PON
                elif isinstance(button, Kan):
                    game_manager.action = ActionType.KAN
                elif isinstance(button, Ron):
                    game_manager.action = ActionType.RON
