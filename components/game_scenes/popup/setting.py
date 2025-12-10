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
from typing import TypedDict, Literal, Type

if typing.TYPE_CHECKING:

    from components.mixer.mixer import Mixer


# Type data
class PickerDataType(TypedDict):
    button: Button
    model_surface_position: tuple[int, int]


BotModelType = Literal["shanten", "aggressive", "passive"]


class Setting(Popup):
    config: SettingConfig

    sfx_surface_position: Rect
    bgm_surface_position: Rect
    bar_and_button_relative_position: tuple[int, int]

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
                - self.bgm_surface_position.x
                - self.bar_and_button_relative_position[0],
                local_mouse[1]
                - self.bgm_surface_position.y
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
                - self.sfx_surface_position.x
                - self.bar_and_button_relative_position[0],
                local_mouse[1]
                - self.sfx_surface_position.y
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
                        - self.sfx_surface_position.x
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.sfx_surface_position.y
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.sfx_button.check_collidepoint(bar_local_mouse):
                        self.is_holding_sfx_button = True
                    elif self.sfx_bar.check_collidepoint(bar_local_mouse):
                        sfx = (bar_local_mouse[0] - self.sfx_bar.get_position().x) / (
                            self.sfx_bar.get_surface().get_width() / 100
                        )

                        self.config["sfx"] = self.handle_min_max_value(sfx)
                        self.mixer.update_sfx_value(self.config["sfx"])

                if self.bgm_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.bgm_surface_position.x
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.bgm_surface_position.y
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.bgm_button.check_collidepoint(bar_local_mouse):
                        self.is_holding_bgm_button = True
                    elif self.bgm_bar.check_collidepoint(bar_local_mouse):
                        bgm = (bar_local_mouse[0] - self.bgm_bar.get_position().x) / (
                            self.bgm_bar.get_surface().get_width() / 100
                        )
                        self.config["bgm"] = self.handle_min_max_value(bgm)
                        self.mixer.update_bgm_value(self.config["bgm"])

                model_pick = None
                bot_idx = None
                for i in range(1, 4):
                    if getattr(self, f"bot_{i}_surface_position").collidepoint(
                        local_mouse[0], local_mouse[1]
                    ):

                        if getattr(self, f"bot_{i}_button")["shanten"][
                            "button"
                        ].check_collidepoint(
                            self.__build_shanten_local_mouse(i, local_mouse)
                        ):
                            model_pick = "shanten"
                            bot_idx = i
                            break
                        if getattr(self, f"bot_{i}_button")["aggressive"][
                            "button"
                        ].check_collidepoint(
                            self.__build_aggressive_local_mouse(i, local_mouse)
                        ):
                            model_pick = "aggressive"
                            bot_idx = i
                            break
                        if getattr(self, f"bot_{i}_button")["passive"][
                            "button"
                        ].check_collidepoint(
                            self.__build_passive_local_mouse(i, local_mouse)
                        ):
                            model_pick = "passive"
                            bot_idx = i
                            break

                if bot_idx is not None and model_pick is not None:
                    self.config[f"player_{bot_idx}"] = model_pick

            case pygame.MOUSEMOTION:
                local_mouse = self.build_local_mouse(event.pos)
                if self.sfx_surface_position.collidepoint(
                    local_mouse[0], local_mouse[1]
                ):
                    bar_local_mouse = (
                        local_mouse[0]
                        - self.sfx_surface_position.x
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.sfx_surface_position.y
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
                        - self.bgm_surface_position.x
                        - self.bar_and_button_relative_position[0],
                        local_mouse[1]
                        - self.bgm_surface_position.y
                        - self.bar_and_button_relative_position[1],
                    )
                    if self.bgm_button.check_collidepoint(bar_local_mouse):
                        return self.bgm_button
                    elif self.bgm_bar.check_collidepoint(bar_local_mouse):
                        return self.bgm_bar

                for i in range(1, 4):
                    if getattr(self, f"bot_{i}_surface_position").collidepoint(
                        local_mouse[0], local_mouse[1]
                    ):

                        if getattr(self, f"bot_{i}_button")["shanten"][
                            "button"
                        ].check_collidepoint(
                            self.__build_shanten_local_mouse(i, local_mouse)
                        ):
                            return getattr(self, f"bot_{i}_button")["shanten"]["button"]
                        if getattr(self, f"bot_{i}_button")["aggressive"][
                            "button"
                        ].check_collidepoint(
                            self.__build_aggressive_local_mouse(i, local_mouse)
                        ):
                            return getattr(self, f"bot_{i}_button")["aggressive"][
                                "button"
                            ]
                        if getattr(self, f"bot_{i}_button")["passive"][
                            "button"
                        ].check_collidepoint(
                            self.__build_passive_local_mouse(i, local_mouse)
                        ):
                            return getattr(self, f"bot_{i}_button")["passive"]["button"]

            case pygame.MOUSEBUTTONUP:
                self.is_holding_bgm_button = False
                self.is_holding_sfx_button = False

    def check_collide_bot_model_picker(self):
        pass

    def __build_shanten_local_mouse(
        self, bot_idx: int, local_mouse: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            local_mouse[0]
            - getattr(self, f"bot_{bot_idx}_surface_position")[0]
            - getattr(self, f"bot_{bot_idx}_button")["shanten"][
                "model_surface_position"
            ][0],
            local_mouse[1]
            - getattr(self, f"bot_{bot_idx}_surface_position")[1]
            - getattr(self, f"bot_{bot_idx}_button")["shanten"][
                "model_surface_position"
            ][1],
        )

    def __build_aggressive_local_mouse(
        self, bot_idx: int, local_mouse: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            local_mouse[0]
            - getattr(self, f"bot_{bot_idx}_surface_position")[0]
            - getattr(self, f"bot_{bot_idx}_button")["aggressive"][
                "model_surface_position"
            ][0],
            local_mouse[1]
            - getattr(self, f"bot_{bot_idx}_surface_position")[1]
            - getattr(self, f"bot_{bot_idx}_button")["aggressive"][
                "model_surface_position"
            ][1],
        )

    def __build_passive_local_mouse(
        self, bot_idx: int, local_mouse: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            local_mouse[0]
            - getattr(self, f"bot_{bot_idx}_surface_position")[0]
            - getattr(self, f"bot_{bot_idx}_button")["passive"][
                "model_surface_position"
            ][0],
            local_mouse[1]
            - getattr(self, f"bot_{bot_idx}_surface_position")[1]
            - getattr(self, f"bot_{bot_idx}_button")["passive"][
                "model_surface_position"
            ][1],
        )

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

        # ----- Build bot model picker surface -----
        bot_1_picker_surface, bot_1_surface_data = self.build_bot_model_picker_surface(
            "Righty", self.config["player_1"]
        )
        self.bot_1_button = bot_1_surface_data
        bot_2_picker_surface, bot_2_surface_data = self.build_bot_model_picker_surface(
            "Mid   ", self.config["player_2"]
        )
        self.bot_2_button = bot_2_surface_data

        bot_3_picker_surface, bot_3_surface_data = self.build_bot_model_picker_surface(
            "Lefty ", self.config["player_3"]
        )
        self.bot_3_button = bot_3_surface_data

        # ---------- SURFACE BLIT ----------
        PADDING_X = 20
        PADDING_Y = 20
        PADDING_EACH_ELEMENTS = 35
        start_height = PADDING_Y
        # ----- Blit Title -----
        title_font_surface = self.build_font_surface("Settings", font_size=30)
        center_pos = build_center_rect(self._surface, title_font_surface)
        self._surface.blit(title_font_surface, (center_pos.x, start_height))

        # ----- Blit Background Music surface -----
        start_height += PADDING_EACH_ELEMENTS + title_font_surface.get_height()
        center_pos = build_center_rect(self._surface, bgm_surface)
        self.bgm_surface_position = Rect(
            center_pos.x,
            start_height,
            bgm_surface.get_width(),
            bgm_surface.get_height(),
        )
        self._surface.blit(bgm_surface, (center_pos.x, start_height))

        # ----- Blit Sound Effect surface -----
        start_height += PADDING_EACH_ELEMENTS + bgm_surface.get_height()
        center_pos = build_center_rect(self._surface, sfx_surface)
        self.sfx_surface_position = Rect(
            center_pos.x,
            start_height,
            sfx_surface.get_width(),
            sfx_surface.get_height(),
        )
        self._surface.blit(sfx_surface, (center_pos.x, start_height))

        start_height += PADDING_EACH_ELEMENTS + sfx_surface.get_height()
        title_font_surface = self.build_font_surface("Bot Diificulty", font_size=30)
        center_pos = build_center_rect(self._surface, title_font_surface)
        self._surface.blit(title_font_surface, (center_pos.x, start_height))

        # ----- Blit Player 1 picker -----
        start_height += PADDING_EACH_ELEMENTS + title_font_surface.get_height()
        center_pos = build_center_rect(self._surface, bot_1_picker_surface)
        self.bot_1_surface_position = Rect(
            center_pos.x,
            start_height,
            bot_1_picker_surface.get_width(),
            bot_1_picker_surface.get_height(),
        )
        self._surface.blit(bot_1_picker_surface, (center_pos.x, start_height))

        # ----- Blit Player 2 picker -----
        start_height += PADDING_EACH_ELEMENTS + bot_1_picker_surface.get_height()
        center_pos = build_center_rect(self._surface, bot_2_picker_surface)
        self.bot_2_surface_position = Rect(
            center_pos.x,
            start_height,
            bot_2_picker_surface.get_width(),
            bot_2_picker_surface.get_height(),
        )
        self._surface.blit(bot_2_picker_surface, (center_pos.x, start_height))

        # ----- Blit Player 2 picker -----
        start_height += PADDING_EACH_ELEMENTS + bot_2_picker_surface.get_height()
        center_pos = build_center_rect(self._surface, bot_3_picker_surface)
        self.bot_3_surface_position = Rect(
            center_pos.x,
            start_height,
            bot_3_picker_surface.get_width(),
            bot_3_picker_surface.get_height(),
        )
        self._surface.blit(bot_3_picker_surface, (center_pos.x, start_height))

    def build_bot_model_picker_surface(
        self, player_text: str, picked: BotModelType
    ) -> tuple[Surface, dict[BotModelType, PickerDataType]]:

        # Bot name surface
        text_surface = self.build_font_surface(player_text, text_color=COLOR_WHITE)
        # Bot model surface

        shanten_surface, shanten_button = self.build_model_picker_surface(
            "Easy", True if picked == "shanten" else False
        )
        draw_hitbox(shanten_surface, COLOR_WHITE)
        aggressive_surface, aggressive_button = self.build_model_picker_surface(
            "Medium", True if picked == "aggressive" else False
        )
        draw_hitbox(aggressive_surface, COLOR_WHITE)

        passive_surface, passive_button = self.build_model_picker_surface(
            "Hard", True if picked == "passive" else False
        )
        draw_hitbox(passive_surface, COLOR_WHITE)

        elements_list = [
            text_surface,
            shanten_surface,
            aggressive_surface,
            passive_surface,
        ]
        full_width = sum(list(map(lambda surface: surface.get_width(), elements_list)))
        wrap_surface = Surface(
            (
                self._surface.get_width() * 0.8,
                max(
                    text_surface.get_height(),
                    shanten_surface.get_height(),
                    aggressive_surface.get_height(),
                    passive_surface.get_height(),
                ),
            ),
            pygame.SRCALPHA,
        )
        padding_for_each_elements = (wrap_surface.get_width() - full_width) / (
            len(elements_list) - 1
        )

        # Blit bot name
        start_width = 0
        center_pos = build_center_rect(wrap_surface, text_surface)
        wrap_surface.blit(text_surface, (start_width, center_pos.y))

        # Blit shanten picker
        start_width += padding_for_each_elements + text_surface.get_width()
        center_pos = build_center_rect(wrap_surface, shanten_surface)
        shanten_surface_position: tuple[int, int] = (start_width, center_pos.y)
        wrap_surface.blit(shanten_surface, shanten_surface_position)

        # Blit aggressive picker
        start_width += padding_for_each_elements + shanten_surface.get_width()
        center_pos = build_center_rect(wrap_surface, aggressive_surface)
        aggressive_surface_position: tuple[int, int] = (start_width, center_pos.y)
        wrap_surface.blit(aggressive_surface, aggressive_surface_position)

        # Blit passive picker
        start_width += padding_for_each_elements + aggressive_surface.get_width()
        center_pos = build_center_rect(wrap_surface, passive_surface)
        passive_surface_position: tuple[int, int] = (start_width, center_pos.y)
        wrap_surface.blit(passive_surface, passive_surface_position)

        return_picker_surface: dict[BotModelType, PickerDataType] = {
            "shanten": {
                "model_surface_position": shanten_surface_position,
                "button": shanten_button,
            },
            "aggressive": {
                "model_surface_position": aggressive_surface_position,
                "button": aggressive_button,
            },
            "passive": {
                "model_surface_position": passive_surface_position,
                "button": passive_button,
            },
        }

        return (wrap_surface, return_picker_surface)

    def build_model_picker_surface(
        self, model_name: str, picked: bool = False
    ) -> tuple[Surface, Button]:
        model_name_surface = self.build_font_surface(model_name)
        button = Button()
        button_surface = self.__create_round_button_surface(picked)
        button.set_surface(button_surface)
        PADDING_EACH_ELEMENTS = 20
        surface = Surface(
            (
                model_name_surface.get_width()
                + button.get_surface().get_width()
                + PADDING_EACH_ELEMENTS,
                max(button.get_surface().get_height(), model_name_surface.get_height()),
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(surface, button.get_surface())
        button.update_position(0, center_pos.y)
        button.render(surface)

        center_pos = build_center_rect(surface, model_name_surface)
        surface.blit(
            model_name_surface,
            (button.get_surface().get_width() + PADDING_EACH_ELEMENTS, center_pos.y),
        )
        return (surface, button)

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

    def __create_round_button_surface(self, fill: bool = True):
        button_surface = Surface(ROUND_BUTTON_SIZE, pygame.SRCALPHA)
        if fill:
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
