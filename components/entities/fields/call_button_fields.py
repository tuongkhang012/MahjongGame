from components.entities.fields.field import Field
from pygame import Surface, Rect
from pygame.event import Event
import pygame
from utils.constants import CALL_BUTTON_SIZE
from utils.enums import CallType, ActionType
from utils.helper import build_center_rect, draw_hitbox

# All call buttons
from components.entities.buttons.chii import Chii
from components.entities.buttons.kan import Kan
from components.entities.buttons.pon import Pon
from components.entities.buttons.ron import Ron
from components.entities.buttons.skip import Skip
from components.entities.buttons.tsumo import Tsumo
from components.entities.buttons.richii import Riichi
from components.entities.call import Call

import typing

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager
    from components.events.mouse_button_down import MouseButtonDown
    from components.events.mouse_motion import MouseMotion


class CallButtonField(Field):
    def __init__(
        self,
        screen: Surface,
    ):
        super().__init__()
        self.screen = screen
        self.__chii_button = Chii()
        self.__kan_button = Kan()
        self.__pon_button = Pon()
        self.__ron_button = Ron()
        self.__skip_button = Skip()
        self.__tsumo_button = Tsumo()
        self.__riichi_button = Riichi()

        self.__all_button: list[Chii | Kan | Pon | Ron | Skip | Tsumo | Riichi] = [
            self.__chii_button,
            self.__kan_button,
            self.__pon_button,
            self.__ron_button,
            self.__skip_button,
            self.__tsumo_button,
            self.__riichi_button,
        ]
        self.space_between_each_button = 20
        self.render_button_list: list[
            Chii | Kan | Pon | Ron | Skip | Tsumo | Riichi
        ] = []

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
            button.hidden = False

    def build_button_position(self, call_list: list[CallType]):
        for idx, call_type in enumerate(call_list):
            button_x = idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button)
            button_y = 0
            button_width = CALL_BUTTON_SIZE[0]
            button_height = CALL_BUTTON_SIZE[1]
            match call_type:
                case CallType.SKIP:
                    self.__skip_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__skip_button)
                case CallType.CHII:
                    self.__chii_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__chii_button)
                case CallType.PON:
                    self.__pon_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__pon_button)
                case CallType.KAN:
                    self.__kan_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__kan_button)

                case CallType.RIICHI:
                    self.__riichi_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__riichi_button)

                case CallType.RON:
                    self.__ron_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__ron_button)
                case CallType.TSUMO:
                    self.__tsumo_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__tsumo_button)

    def hover(self, event: Event) -> bool:
        local_mouse = self.build_local_mouse(event.pos)
        is_hovering_button = False
        for button in self.render_button_list:
            if button.check_collidepoint(local_mouse) and not button.hidden:
                is_hovering_button = True
                button.hovered()
                break

        for button in self.__all_button:
            if not button.check_collidepoint(local_mouse):
                button.hidden = True
                button.unhovered()

        return is_hovering_button

    def unhover(self):
        for button in self.render_button_list:
            button.unhovered()

    def click(self, event: Event, game_manager: "GameManager"):
        local_mouse = self.build_local_mouse(event.pos)
        player = game_manager.player_list[0]
        for button in self.render_button_list:
            if button.check_collidepoint(local_mouse):
                print(f"CLICKING BUTTON {button.text.upper()}")
                if isinstance(button, Chii):
                    game_manager.action = player.make_move(ActionType.CHII)
                elif isinstance(button, Skip):
                    game_manager.action = player.make_move(ActionType.SKIP)
                elif isinstance(button, Pon):
                    game_manager.action = player.make_move(ActionType.PON)
                elif isinstance(button, Kan):
                    game_manager.action = player.make_move(ActionType.KAN)
                elif isinstance(button, Ron):
                    game_manager.action = player.make_move(ActionType.RON)
                elif isinstance(button, Tsumo):
                    game_manager.action = player.make_move(ActionType.TSUMO)
                elif isinstance(button, Riichi):
                    game_manager.action = player.make_move(ActionType.RIICHI)
