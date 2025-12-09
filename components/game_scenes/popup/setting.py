from components.game_scenes.popup.popup import Popup
from pygame import Surface, Color, Rect
import pygame
from utils.constants import (
    ROUND_BUTTON_SIZE,
    ROUND_BUTTON_COLOR,
    COLOR_BLACK,
    BAR_SIZE,
    BETTER_VCR_FONT,
    COLOR_WHITE,
    POPUP_BACKGROUND_COLOR,
    SETTING_CONFIG_PATH,
)
from components.entities.buttons.button import Button
from utils.setting_config import SettingConfig
from utils.helper import build_center_rect, draw_hitbox
from pygame.freetype import Font
import typing

if typing.TYPE_CHECKING:

    from components.mixer.mixer import Mixer


class Setting(Popup):
    config: SettingConfig

    def __init__(self, screen: Surface, config: SettingConfig, mixer: "Mixer"):

        super().__init__()
        self.screen = screen
        self.config = config
        self.is_holding_sfx_button = False
        self.is_holding_bgm_button = False
        self.mixer = mixer

    def render(self, screen: Surface):
        self.update()
        self.build_surface()
        center_pos = build_center_rect(screen, self._surface)
        self.update_absolute_position_rect(
            Rect(
                center_pos.x,
                center_pos.y,
                self._surface.get_width(),
                self._surface.get_height(),
            )
        )
        screen.blit(self._surface, (center_pos.x, center_pos.y))

    def update(self):
        local_mouse = self.build_local_mouse(pygame.mouse.get_pos())

        if self.is_holding_bgm_button:
            bar_local_mouse = (
                local_mouse[0]
                - self.bgm_surface_position[0]
                - self.bar_and_button_relative_position[0],
                local_mouse[1]
                - self.bgm_surface_position[1]
                - self.bar_and_button_relative_position[1],
            )
            self.config["bgm"] = self.handle_min_max_value(
                (bar_local_mouse[0] - self.bgm_bar.get_position().x)
                / (self.bgm_bar.get_surface().get_width() / 100)
            )
            self.mixer.update_bgm_value(self.config["bgm"])
        if self.is_holding_sfx_button:
            bar_local_mouse = (
                local_mouse[0]
                - self.sfx_surface_position[0]
                - self.bar_and_button_relative_position[0],
                local_mouse[1]
                - self.sfx_surface_position[1]
                - self.bar_and_button_relative_position[1],
            )
            self.config["sfx"] = self.handle_min_max_value(
                (bar_local_mouse[0] - self.sfx_bar.get_position().x)
                / (self.sfx_bar.get_surface().get_width() / 100)
            )
            self.mixer.update_sfx_value(self.config["sfx"])

    def handle_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if not self.check_collide(event.pos):
                    self.export()
                    return "close"
                local_mouse = self.build_local_mouse(event.pos)
                if self.sfx_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.sfx_surface_position[0]
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.sfx_surface_position[1]
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.sfx_button.check_collidepoint(bar_local_mouse):
                        self.is_holding_sfx_button = True
                    elif self.sfx_bar.check_collidepoint(bar_local_mouse):
                        sfx = (bar_local_mouse[0] - self.sfx_bar.get_position().x) / (
                            self.sfx_bar.get_surface().get_width() / 100
                        )

                        self.config["sfx"] = self.handle_min_max_value(sfx)

                if self.bgm_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.bgm_surface_position[0]
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.bgm_surface_position[1]
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.bgm_button.check_collidepoint(bar_local_mouse):
                        self.is_holding_bgm_button = True
                    elif self.bgm_bar.check_collidepoint(bar_local_mouse):
                        bgm = (bar_local_mouse[0] - self.bgm_bar.get_position().x) / (
                            self.bgm_bar.get_surface().get_width() / 100
                        )
                        self.config["bgm"] = self.handle_min_max_value(bgm)

            case pygame.MOUSEMOTION:
                local_mouse = self.build_local_mouse(event.pos)
                if self.sfx_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.sfx_surface_position[0]
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.sfx_surface_position[1]
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.sfx_button.check_collidepoint(bar_local_mouse):
                        return self.sfx_button
                    elif self.sfx_bar.check_collidepoint(bar_local_mouse):
                        return self.sfx_bar

                if self.bgm_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.bgm_surface_position[0]
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.bgm_surface_position[1]
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.bgm_button.check_collidepoint(bar_local_mouse):
                        return self.bgm_button
                    elif self.bgm_bar.check_collidepoint(bar_local_mouse):
                        return self.bgm_bar

            case pygame.MOUSEBUTTONUP:
                self.is_holding_bgm_button = False
                self.is_holding_sfx_button = False

    def handle_min_max_value(self, value: int):
        if value > 100:
            return 100
        elif value < 0:
            return 0
        else:
            return value

    def build_surface(self):
        self._surface = Surface(
            (self.screen.get_width(), self.screen.get_height()),
            pygame.SRCALPHA,
        )
        self.set_bg_color(POPUP_BACKGROUND_COLOR)
        self.draw_border_radius(COLOR_WHITE)
        bgm_surface, buttons_list = self.build_text_and_bar_surface(
            "Background Music", self.config["bgm"]
        )
        self.bgm_bar = buttons_list[0]
        self.bgm_button = buttons_list[1]

        sfx_surface, buttons_list = self.build_text_and_bar_surface(
            "Sound Effects", self.config["sfx"]
        )
        self.sfx_bar = buttons_list[0]
        self.sfx_button = buttons_list[1]
        PADDING_X = 20
        PADDING_Y = 20
        PADDING_EACH_ELEMENTS = 40
        start_height = PADDING_Y
        title_font_surface = self.build_font_surface("Settings", font_size=30)
        center_pos = build_center_rect(self._surface, title_font_surface)
        self._surface.blit(title_font_surface, (center_pos.x, start_height))

        start_height += PADDING_EACH_ELEMENTS + title_font_surface.get_height()
        center_pos = build_center_rect(self._surface, bgm_surface)
        self.bgm_surface_position = Rect(
            center_pos.x,
            start_height,
            bgm_surface.get_width(),
            bgm_surface.get_height(),
        )
        self._surface.blit(bgm_surface, (center_pos.x, start_height))

        start_height += PADDING_EACH_ELEMENTS + bgm_surface.get_height()
        center_pos = build_center_rect(self._surface, sfx_surface)
        self.sfx_surface_position = Rect(
            center_pos.x,
            start_height,
            sfx_surface.get_width(),
            sfx_surface.get_height(),
        )
        self._surface.blit(sfx_surface, (center_pos.x, start_height))

    def build_text_and_bar_surface(
        self, text: str, button_value: int
    ) -> tuple[Surface, list[Button]]:
        bar_and_button_surface, buttons_list = self.build_bar_with_button(button_value)
        draw_hitbox(bar_and_button_surface)
        text_surface = self.build_font_surface(text)
        surface = Surface(
            (
                self._surface.get_width() * 0.8,
                max(
                    bar_and_button_surface.get_height(),
                    bar_and_button_surface.get_height(),
                ),
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(surface, text_surface)
        surface.blit(text_surface, (0, center_pos.y))

        center_pos = build_center_rect(surface, bar_and_button_surface)
        self.bar_and_button_relative_position = (
            surface.get_width() - bar_and_button_surface.get_width(),
            center_pos.y,
        )
        surface.blit(
            bar_and_button_surface,
            (
                surface.get_width() - bar_and_button_surface.get_width(),
                center_pos.y,
            ),
        )
        return (surface, buttons_list)

    def build_bar_with_button(self, button_value: int) -> tuple[Surface, list[Button]]:
        round_button = Button()
        round_button.set_surface(self.__create_round_button_surface())

        bar_button = Button()
        bar_button.set_surface(self.__create_bar_surface())

        bar_with_button_surface = Surface(
            (
                bar_button.get_surface().get_width()
                + round_button.get_surface().get_width(),
                round_button.get_surface().get_height(),
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(
            bar_with_button_surface, bar_button.get_surface()
        )
        bar_button.update_position(center_pos.x, center_pos.y)
        bar_button.render(bar_with_button_surface)

        button_pos = (
            center_pos.x
            + button_value * (bar_button.get_surface().get_width() / 100)
            - round_button.get_surface().get_width() / 2
        )
        round_button.update_position(button_pos, 0)
        round_button.render(bar_with_button_surface)
        draw_hitbox(bar_with_button_surface)
        return (bar_with_button_surface, [bar_button, round_button])

    def build_font_surface(
        self,
        text: str,
        font_family: str = BETTER_VCR_FONT,
        font_size: int = 20,
        text_color: Color = pygame.Color(COLOR_BLACK),
    ) -> Surface:
        font = Font(font_family, font_size)
        font_surface, _ = font.render(text, text_color)
        return font_surface

    def __create_bar_surface(self):
        bar_surface = Surface(BAR_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(
            bar_surface, COLOR_BLACK, bar_surface.get_rect(), border_radius=10
        )
        return bar_surface

    def __create_round_button_surface(self):
        button_surface = Surface(ROUND_BUTTON_SIZE, pygame.SRCALPHA)
        pygame.draw.circle(
            button_surface,
            ROUND_BUTTON_COLOR,
            button_surface.get_rect().center,
            button_surface.get_width() / 2,
        )
        pygame.draw.circle(
            button_surface,
            COLOR_BLACK,
            button_surface.get_rect().center,
            button_surface.get_width() / 2,
            2,
        )
        return button_surface

    def export(self):
        import json

        with open(SETTING_CONFIG_PATH, "w") as file:
            json.dump(self.config, file)
