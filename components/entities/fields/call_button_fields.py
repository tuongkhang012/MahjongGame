from components.entities.fields.field import Field
from pygame import Surface, Rect
import pygame
import random
from utils.constants import CALL_BUTTON_SIZE, COLOR_BLACK
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
from components.entities.buttons.ryuukyoku import Ryuukyoku
from components.entities.buttons.call_button import CallButton

# Particle
from components.entities.particles.smoke_particle import SmokeParticle

import typing

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


class CallButtonField(Field):
    """
    Field that holds call buttons for the player to interact with.
    :ivar screen: Surface: The main game screen surface.
    :ivar __chii_button: Chii: The Chii call button.
    :ivar __kan_button: Kan: The Kan call button.
    :ivar __pon_button: Pon: The Pon call button.
    :ivar __ron_button: Ron: The Ron call button.
    :ivar __skip_button: Skip: The Skip call button.
    :ivar __tsumo_button: Tsumo: The Tsumo call button.
    :ivar __riichi_button: Riichi: The Riichi call button.
    :ivar __ryuukyoku_button: Ryuukyoku: The Ryuukyoku call button.
    :ivar __all_button: list[CallButton]: List of all call buttons.
    :ivar space_between_each_button: int: Space between each button.
    :ivar render_button_list: list[CallButton]: List of buttons to render.
    :ivar _hovered_button: CallButton | None: The currently hovered button.
    :ivar _smoke_spawn_timer: float: Timer for spawning smoke particles.
    :ivar _smoke_spawn_interval: float: Interval between smoke particle spawns.
    :ivar _particles: list[SmokeParticle]: List of active smoke particles.
    """
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
        self.__ryuukyoku_button = Ryuukyoku()

        self.__all_button: list[CallButton] = [
            self.__chii_button,
            self.__kan_button,
            self.__pon_button,
            self.__ron_button,
            self.__skip_button,
            self.__tsumo_button,
            self.__riichi_button,
            self.__ryuukyoku_button,
        ]
        self.space_between_each_button = 20
        self.render_button_list: list[CallButton] = []

        self._hovered_button: CallButton | None = None

        # Smoke spawning while hovering
        self._smoke_spawn_timer: float = 0.0
        self._smoke_spawn_interval: float = 0.05  # seconds between smoke puffs

        self._particles: list[SmokeParticle] = []

        self.hidden = True

    def render(self, call_list: list[CallType]):
        self.build_surface(call_list)
        render_surface = Surface(
            (self.screen.get_width(), CALL_BUTTON_SIZE[1]), pygame.SRCALPHA
        ) # Transparent surface to render buttons onto
        center_pos = build_center_rect(render_surface, self.surface) # Center position to render buttons
        self.update_relative_position(center_pos)
        render_surface.blit(self.surface, (center_pos.x, center_pos.y))
        draw_hitbox(render_surface)

        screen_pos = (0, 4 * self.screen.get_height() / 5 - CALL_BUTTON_SIZE[1])
        self.screen.blit(render_surface, screen_pos)
        self._absolute_position = Rect(
            screen_pos[0] + center_pos.x,
            screen_pos[1] + center_pos.y,
            self.surface.get_width(),
            self.surface.get_height(),
        )

    def update_particles(self, dt: float):
        alive: list[SmokeParticle] = []
        for p in self._particles:
            p.update(dt)
            if not p.dead:
                alive.append(p)
        self._particles = alive

        hovered_buttons = list(
            filter(lambda button: button.is_hovered, self.__all_button)
        )
        if len(hovered_buttons) > 0:
            for button in hovered_buttons:
                self._smoke_spawn_timer += dt
                while self._smoke_spawn_timer >= self._smoke_spawn_interval:
                    self._smoke_spawn_timer -= self._smoke_spawn_interval
                    self._spawn_smoke_for_button(button)
        else:
            self._smoke_spawn_timer = 0.0

    def render_particles(self, screen: Surface):
        for p in self._particles:
            p.draw(screen)

    def _spawn_smoke_for_button(self, button):
        frames = button.get_smoke_frames()
        if not frames:
            return

        # Button rect is in field-local coordinates
        button_rect = button.get_position()

        # _absolute_position is set in render()
        field_rect = self._absolute_position

        # Top-center of the button in *screen* coordinates
        x = random.uniform(
            field_rect.x + button_rect.x,
            field_rect.x + button_rect.x + button_rect.width,
        )
        y = field_rect.y + button_rect.y

        self._particles.append(
            SmokeParticle(
                frames=frames,
                pos=(x, y),
            )
        )
        self._particles.append(
            SmokeParticle(
                frames=frames,
                pos=(x, y),
            )
        )
        self._particles.append(
            SmokeParticle(
                frames=frames,
                pos=(x, y),
            )
        )

    def build_surface(self, call_list: list[CallType]) -> None:
        """
        Build the surface with the given call buttons. Then render them onto the surface.
        :param call_list: list[CallType]: List of call types to render buttons for.
        :return: None
        """
        self.render_button_list = []
        self.surface = Surface(
            size=( # x = total button width + space between each
                CALL_BUTTON_SIZE[0] * len(call_list)
                + self.space_between_each_button * (len(call_list) - 1),
                CALL_BUTTON_SIZE[1],
            ),
            flags=pygame.SRCALPHA,
        )
        draw_hitbox(self.surface, COLOR_BLACK)
        self.build_button_position(call_list)

        for button in self.render_button_list:
            button.render(self.surface)
            button.hidden = False
            self.hidden = False

    def build_button_position(self, call_list: list[CallType]) -> None:
        """
        Assign the position of each button based on the call list.
        :param call_list: list[CallType]: List of call types to render buttons for.
        :return: None
        """
        for idx, call_type in enumerate(call_list):
            button_x = idx * (CALL_BUTTON_SIZE[0] + self.space_between_each_button)
            button_y = 0
            button_width, button_height = CALL_BUTTON_SIZE
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

                case CallType.RYUUKYOKU:
                    self.__ryuukyoku_button.update_position(
                        button_x,
                        button_y,
                        button_width,
                        button_height,
                    )
                    self.render_button_list.append(self.__ryuukyoku_button)

    def hover(self, mouse_pos: tuple[int, int]) -> CallButton | None:
        if self.hidden:
            return None

        local_mouse = self.build_local_mouse(mouse_pos)

        for button in self.__all_button:
            button.unhovered()

        for button in self.render_button_list:
            if button.check_collidepoint(local_mouse) and not button.hidden:
                button.hovered()
                return button

        return None

    def unhover(self):
        for button in self.__all_button:
            button.unhovered()

    def click(self, mouse_pos: tuple[int, int], game_manager: "GameManager"):
        local_mouse = self.build_local_mouse(mouse_pos)
        player = game_manager.player_list[0]
        self.hidden = True

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
                elif isinstance(button, Ryuukyoku):
                    game_manager.action = player.make_move(ActionType.RYUUKYOKU)
                button.unhovered()
                return button

        return None