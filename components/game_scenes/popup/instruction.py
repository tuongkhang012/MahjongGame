import pygame
from utils.constants import (
    INSTRUCTION_ASSETS,
    COLOR_WHITE,
    BETTER_VCR_FONT,
    COLOR_BLUE,
    COLOR_BLACK,
    INSTRUCTION_CARD_TITLE_COLOR,
    INSTRUCTION_CARD_BODY_COLOR,
    POPUP_BACKGROUND_COLOR,
)
from pygame import Surface, Color, Rect
from pygame.event import Event
from utils.instruction_data_dict import InstructionCard, InstructionPageData
from components.game_scenes.popup.popup import Popup
from utils.enums import InstructionSection
from pygame.freetype import Font
from components.entities.buttons.button import Button
from utils.helper import build_center_rect, draw_hitbox

import json


class Instruction(Popup):
    akadora: Surface
    ankan: Surface
    bakaze: Surface
    chankan: Surface
    chanta: Surface
    chii: Surface
    chiitoitsu: Surface
    chinitsu: Surface
    chinroutou: Surface
    chuurenpoutou: Surface
    daisangen: Surface
    daisuushi: Surface
    dora: Surface
    dragon: Surface
    hand: Surface
    honitsu: Surface
    honroutou: Surface
    houra: Surface
    iipeikou: Surface
    ittsu: Surface
    jikaze: Surface
    junchan: Surface
    junseichuurenpoutou: Surface
    kakan: Surface
    kokushimusou: Surface
    kokushimusou13menmachi: Surface
    kyotaku: Surface
    man: Surface
    menzentsumo: Surface
    minkan: Surface
    pair: Surface
    pin: Surface
    pinfu: Surface
    pon: Surface
    riichi: Surface
    riichi_yaku: Surface
    ryanpeikou: Surface
    ryuuiisou: Surface
    sanankou: Surface
    sangenpai: Surface
    sankantsu: Surface
    sanshokudoujun: Surface
    sanshokudoukou: Surface
    sequence: Surface
    shousangen: Surface
    shousuushi: Surface
    sou: Surface
    suuankou: Surface
    suukantsu: Surface
    tanyao: Surface
    tanyao_yaku: Surface
    tenpai: Surface
    terminal: Surface
    toitoi: Surface
    triplet: Surface
    tsuuiisou: Surface
    wind: Surface

    def __init__(self, screen: Surface):
        """
        Initialize Instruction Popup
        :param screen: The popup render surface
        """
        super().__init__()
        self.screen = screen
        self.akadora = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_AKADORA"])
        self.ankan = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_ANKAN"])
        self.bakaze = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_BAKAZE"])
        self.chankan = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_CHANKAN"])
        self.chanta = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_CHANTA"])
        self.chii = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_CHII"])
        self.chiitoitsu = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_CHIITOITSU"]
        )
        self.chinitsu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_CHINITSU"])
        self.chinroutou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_CHINROUTOU"]
        )
        self.chuurenpoutou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_CHUURENPOUTOU"]
        )
        self.daisangen = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_DAISANGEN"])
        self.daisuushi = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_DAISUUSHI"])
        self.dora = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_DORA"])
        self.dragon = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_DRAGON"])
        self.hand = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_HAND"])
        self.honitsu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_HONITSU"])
        self.honroutou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_HONROUTOU"])
        self.houra = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_HOURA"])
        self.iipeikou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_IIPEIKOU"])
        self.ittsu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_ITTSU"])
        self.jikaze = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_JIKAZE"])
        self.junchan = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_JUNCHAN"])
        self.junseichuurenpoutou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_JUNSEICHUURENPOUTOU"]
        )
        self.kakan = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_KAKAN"])
        self.kokushimusou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_KOKUSHIMUSOU"]
        )
        self.kokushimusou13menmachi = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_KOKUSHIMUSOU13MENMACHI"]
        )
        self.kyotaku = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_KYOTAKU"])
        self.man = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_MAN"])
        self.menzentsumo = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_MENZENTSUMO"]
        )
        self.minkan = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_MINKAN"])
        self.pair = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_PAIR"])
        self.pin = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_PIN"])
        self.pinfu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_PINFU"])
        self.pon = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_PON"])
        self.riichi = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_RIICHI"])
        self.riichi_yaku = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_RIICHI_YAKU"]
        )
        self.ryanpeikou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_RYANPEIKOU"]
        )
        self.ryuuiisou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_RYUUIISOU"])
        self.sanankou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SANANKOU"])
        self.sangenpai = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SANGENPAI"])
        self.sankantsu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SANKANTSU"])
        self.sanshokudoujun = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_SANSHOKUDOUJUN"]
        )
        self.sanshokudoukou = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_SANSHOKUDOUKOU"]
        )
        self.sequence = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SEQUENCE"])
        self.shousangen = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_SHOUSANGEN"]
        )
        self.shousuushi = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_SHOUSUUSHI"]
        )
        self.sou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SOU"])
        self.suuankou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SUUANKOU"])
        self.suukantsu = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_SUUKANTSU"])
        self.tanyao = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TANYAO"])
        self.tanyao_yaku = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_TANYAO_YAKU"]
        )
        self.tenpai = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TENPAI"])
        self.terminal = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TERMINAL"])
        self.toitoi = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TOITOI"])
        self.triplet = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TRIPLET"])
        self.tsuuiisou = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_TSUUIISOU"])
        self.wind = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_WIND"])
        self.yakuhai = pygame.image.load(INSTRUCTION_ASSETS["INSTRUCTION_YAKUHAI"])

        self.game_flow_ui = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_UI"]
        )
        self.game_flow_chii = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_CHII"]
        )
        self.game_flow_pon = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_PON"]
        )
        self.game_flow_kan = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_KAN"]
        )
        self.game_flow_tsumo = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_TSUMO"]
        )
        self.game_flow_ron = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_RON"]
        )
        self.game_flow_riichi = pygame.image.load(
            INSTRUCTION_ASSETS["INSTRUCTION_GAME_FLOW_RIICHI"]
        )

        with open("data/instruction_tutorial.json", "r") as file:
            self.instruction_tutorial_data: dict[str, InstructionPageData] = json.load(
                file
            )

        with open("data/instruction_yaku.json", "r") as file:
            self.instruction_yaku_data: dict[str, InstructionPageData] = json.load(file)

        with open("data/instruction_game_flow.json", "r") as file:
            self.instruction_game_flow_data: dict[str, InstructionPageData] = json.load(
                file
            )

        arrow = pygame.image.load("public/images/buttons/arrow_up.png")
        self.next_button = Button()
        self.next_button.set_surface(pygame.transform.rotate(arrow, -90))
        self.prev_button = Button()
        self.prev_button.set_surface(pygame.transform.rotate(arrow, 90))
        self.close_button = Button()
        self.close_button.set_surface(
            pygame.image.load("public/images/buttons/close_button.png")
        )

        self.tutorial_button = Button()

        self.section = InstructionSection.TUTORIAL
        self.page = 0
        self.yaku_page = 0
        self.game_flow_page = 0
        self.max_instruction_tutorial_page = len(self.instruction_tutorial_data.keys())
        self.max_instruction_yaku_page = len(self.instruction_yaku_data.keys())
        self.max_instruction_game_flow_page = len(
            self.instruction_game_flow_data.keys()
        )

    def change_section(self, section: InstructionSection):
        self.section = section

    def change_page(self, page: int):
        self.page = page

    def build_surface(self, section: InstructionSection, page: int):
        PADDING_X = 20
        PADDING_Y = 20
        self.set_bg_color(POPUP_BACKGROUND_COLOR)
        self.section_surface = Surface(
            (self.screen.get_size()[0], self.screen.get_size()[1] * 0.95),
            pygame.SRCALPHA,
        )
        self.draw_surface_border_radius(self.section_surface)
        # Build body surface
        match section:
            case InstructionSection.TUTORIAL:
                self.build_surface_tutorial(page)
            case InstructionSection.YAKU_OVERVIEW:
                self.build_surface_yaku_overview(page)
            case InstructionSection.GAME_FLOW:
                self.build_surface_game_flow(page)

        # Build section tab button
        self.section_tab_surface = Surface(
            (self.screen.get_size()[0], self.screen.get_size()[1] * 0.05),
            pygame.SRCALPHA,
        )

        # region Create Tutorial Section Button
        # ----- Create Tutorial Section Button -----
        self.section_tutorial_button = Button(
            text="Tutorial",
            font=Font(BETTER_VCR_FONT, 15),
            text_color=COLOR_BLACK,
            bg_color=(
                COLOR_WHITE
                if self.section == InstructionSection.TUTORIAL
                else POPUP_BACKGROUND_COLOR
            ),
        )

        self.section_tutorial_button.set_surface(
            Surface(
                (
                    self.section_tab_surface.get_width() / 7,
                    self.section_tab_surface.get_height(),
                ),
                pygame.SRCALPHA,
            )
        )
        self.draw_button_surface(self.section_tutorial_button)

        self.section_tutorial_button.update_position(
            self.section_tab_surface.get_width() / 7, 0
        )
        # endregion Create Yaku Section Button

        # region Create Yaku Section Button
        # ----- Create Yaku Section Button -----
        self.section_yaku_overview_button = Button(
            text="Yaku Overview",
            font=Font(BETTER_VCR_FONT, 15),
            text_color=COLOR_BLACK,
            bg_color=(
                COLOR_WHITE
                if self.section == InstructionSection.YAKU_OVERVIEW
                else POPUP_BACKGROUND_COLOR
            ),
        )

        self.section_yaku_overview_button.set_surface(
            Surface(
                (
                    self.section_tab_surface.get_width() / 7,
                    self.section_tab_surface.get_height(),
                ),
                pygame.SRCALPHA,
            )
        )
        self.draw_button_surface(self.section_yaku_overview_button)

        self.section_yaku_overview_button.update_position(
            3 * self.section_tab_surface.get_width() / 7, 0
        )
        # endregion Create Yaku Section Button

        # region Create Game Flow Section Button
        # ----- Create Game Flow Button ------
        self.section_game_flow_button = Button(
            text="Game Flow",
            font=Font(BETTER_VCR_FONT, 15),
            text_color=COLOR_BLACK,
            bg_color=(
                COLOR_WHITE
                if self.section == InstructionSection.GAME_FLOW
                else POPUP_BACKGROUND_COLOR
            ),
        )

        self.section_game_flow_button.set_surface(
            Surface(
                (
                    self.section_tab_surface.get_width() / 7,
                    self.section_tab_surface.get_height(),
                ),
                pygame.SRCALPHA,
            )
        )
        self.draw_button_surface(self.section_game_flow_button)

        self.section_game_flow_button.update_position(
            5 * self.section_tab_surface.get_width() / 7, 0
        )
        # endregion Create Game Flow Button
        # ----- Render All Section Button
        self.section_tutorial_button.render(self.section_tab_surface)
        self.section_yaku_overview_button.render(self.section_tab_surface)
        self.section_game_flow_button.render(self.section_tab_surface)

        # Close Button
        self.close_button.update_position(
            self.section_surface.get_width()
            - PADDING_X
            - self.close_button.get_surface().get_width(),
            PADDING_Y,
        )

        self.close_button.render(self.section_surface)

        # Changing page area
        match self.section:
            case InstructionSection.TUTORIAL:
                page_number_surface = self.build_font_surface(
                    str(self.page + 1), text_color=COLOR_WHITE
                )
            case InstructionSection.YAKU_OVERVIEW:
                page_number_surface = self.build_font_surface(
                    str(self.yaku_page + 1), text_color=COLOR_WHITE
                )
            case InstructionSection.GAME_FLOW:
                page_number_surface = self.build_font_surface(
                    str(self.game_flow_page + 1), text_color=COLOR_WHITE
                )

        max_height = max(
            page_number_surface.get_height(),
            self.prev_button.get_surface().get_height(),
            self.next_button.get_surface().get_height(),
        )

        # Changing pages buttons
        if self.max_instruction_tutorial_page > 1:
            PADDING_EACH_BUTTON_X = 30
            change_pages_buttons_surface = Surface(
                (
                    page_number_surface.get_width()
                    + self.prev_button.get_surface().get_width()
                    + self.next_button.get_surface().get_width()
                    + PADDING_X * 2
                    + PADDING_EACH_BUTTON_X * 2,
                    max_height,
                ),
                pygame.SRCALPHA,
            )

            start_width = PADDING_X
            center_pos = build_center_rect(
                change_pages_buttons_surface, self.prev_button.get_surface()
            )
            self.prev_button.update_position(start_width, center_pos.y)
            self.prev_button.render(change_pages_buttons_surface)

            start_width += (
                self.prev_button.get_surface().get_width() + PADDING_EACH_BUTTON_X
            )
            center_pos = build_center_rect(
                change_pages_buttons_surface, page_number_surface
            )
            change_pages_buttons_surface.blit(
                page_number_surface, (start_width, center_pos.y)
            )

            start_width += page_number_surface.get_width() + PADDING_EACH_BUTTON_X
            center_pos = build_center_rect(
                change_pages_buttons_surface, self.next_button.get_surface()
            )
            self.next_button.update_position(start_width, center_pos.y)
            self.next_button.render(change_pages_buttons_surface)

            center_pos = build_center_rect(
                self.section_surface, change_pages_buttons_surface
            )
            change_pages_buttons_position = (
                center_pos.x,
                self.section_surface.get_height()
                - change_pages_buttons_surface.get_height()
                - 10,
            )

            self.section_surface.blit(
                change_pages_buttons_surface, change_pages_buttons_position
            )

            self.__prev_button_rect = Rect(
                change_pages_buttons_position[0] + self.prev_button.get_position().x,
                change_pages_buttons_position[1] + self.prev_button.get_position().y,
                self.next_button.get_surface().get_width(),
                self.next_button.get_surface().get_height(),
            )

            self.__next_button_rect = Rect(
                change_pages_buttons_position[0] + self.next_button.get_position().x,
                change_pages_buttons_position[1] + self.next_button.get_position().y,
                self.next_button.get_surface().get_width(),
                self.next_button.get_surface().get_height(),
            )

        self._surface = Surface(self.screen.get_size(), pygame.SRCALPHA)
        self._surface.blit(self.section_tab_surface, (0, 0))
        self._surface.blit(
            self.section_surface, (0, self.section_tab_surface.get_height())
        )

    def build_surface_tutorial(self, page: int):
        try:
            body_surface = getattr(self, f"build_page_{page+1}_tutorial_surface")()
        except Exception as e:
            print(e.args, "Hello")
            body_surface = Surface((0, 0), pygame.SRCALPHA)

        try:
            title = self.instruction_tutorial_data[str(self.page)]["title"]
        except:
            title = "Not yet implement data!!!"
        self.build_page_information_surface(title, body_surface)

    def build_surface_yaku_overview(self, page: int):
        try:
            body_surface = getattr(self, f"build_page_{page+1}_yaku_surface")()
        except Exception as e:
            print(e.args, "Hello")
            body_surface = Surface((0, 0), pygame.SRCALPHA)

        try:
            title = self.instruction_yaku_data[str(self.yaku_page)]["title"]
        except:
            title = "Not yet implement data!!!"
        self.build_page_information_surface(title, body_surface)

    def build_surface_game_flow(self, page: int):
        try:
            body_surface = getattr(self, f"build_page_{page+1}_game_flow")()
        except Exception as e:
            print(e.args, "Hello")
            body_surface = Surface((0, 0), pygame.SRCALPHA)

        try:
            title = self.instruction_game_flow_data[str(self.game_flow_page)]["title"]
        except:
            title = "Not yet implement data!!!"
        self.build_page_information_surface(title, body_surface)

    def render(self, screen: Surface):
        match self.section:
            case InstructionSection.TUTORIAL:
                self.build_surface(self.section, self.page)
            case InstructionSection.YAKU_OVERVIEW:
                self.build_surface(self.section, self.yaku_page)
            case InstructionSection.GAME_FLOW:
                self.build_surface(self.section, self.game_flow_page)

        center_pos = build_center_rect(screen, self._surface)
        screen.blit(self._surface, (center_pos.x, center_pos.y))
        self.update_absolute_position_rect(
            Rect(
                center_pos.x,
                center_pos.y,
                self._surface.get_width(),
                self._surface.get_height(),
            )
        )

    def build_page_information_surface(self, title: str, body_surface: Surface):
        PADDING_Y = 20
        title_surface = self.build_font_surface(
            title, font_size=25, text_color=COLOR_WHITE
        )

        center_pos = build_center_rect(self.section_surface, title_surface)
        self.section_surface.blit(title_surface, (center_pos.x, PADDING_Y))

        center_pos = build_center_rect(self.section_surface, body_surface)
        self.section_surface.blit(body_surface, (center_pos.x, center_pos.y))

    def build_instruction_card_surface(self, instruction_card_data: InstructionCard):
        title = instruction_card_data["title"]

        PADDING_X = 20
        PADDING_Y = 10

        SPACE_BETWEEN_CONTENT = 20

        # ----- Build title surface -----
        font_surface = self.build_font_surface(title, text_color=(94, 92, 92))
        title_surface = Surface(
            (
                font_surface.get_width() + PADDING_X * 2,
                font_surface.get_height() + PADDING_Y * 2,
            ),
            pygame.SRCALPHA,
        )

        title_surface.fill(INSTRUCTION_CARD_TITLE_COLOR)
        title_surface.blit(font_surface, (PADDING_X, PADDING_Y))

        context_surfaces: list[Surface] = []
        image_surface_idx = []
        for idx, context in enumerate(instruction_card_data["body"]):
            if context["type"] == "text":
                description = context["content"]
                font_surface = self.build_font_surface(
                    description, font_size=15, text_color=COLOR_BLACK
                )

                context_surfaces.append(font_surface)
            if context["type"] == "image":
                image = self.__getattribute__(context["content"])
                if context.get("resize") is None or (
                    context.get("resize") is not None and not context.get("resize")
                ):
                    context_surfaces.append(pygame.transform.scale_by(image, 2.5))
                else:
                    context_surfaces.append(
                        pygame.transform.scale_by(image, float(context.get("resize")))
                    )

                image_surface_idx.append(idx)

        max_width = max(
            [title_surface.get_width()]
            + list(map(lambda surface: surface.get_width(), context_surfaces)),
        )

        total_body_height = sum(
            list(map(lambda surface: surface.get_height(), context_surfaces))
        )
        # This contain all information (description and image)
        information_surface = Surface(
            (
                max_width + PADDING_X * 2,
                total_body_height
                + PADDING_Y * 2
                + SPACE_BETWEEN_CONTENT * (len(context_surfaces) - 1),
            ),
            pygame.SRCALPHA,
        )
        information_surface.fill(INSTRUCTION_CARD_BODY_COLOR)

        start_height = PADDING_Y
        for idx, surface in enumerate(context_surfaces):
            if idx in image_surface_idx:
                center_pos = build_center_rect(information_surface, surface)
                information_surface.blit(surface, (center_pos.x, start_height))
            else:
                information_surface.blit(surface, (PADDING_X, start_height))
            start_height += surface.get_height() + SPACE_BETWEEN_CONTENT

        wrap_surface = Surface(
            (
                information_surface.get_width(),
                title_surface.get_height() + information_surface.get_height(),
            ),
            pygame.SRCALPHA,
        )
        wrap_surface.blit(title_surface, (0, 0))
        wrap_surface.blit(information_surface, (0, title_surface.get_height()))
        return wrap_surface

    def build_font_surface(
        self,
        text: str,
        font_family: str = BETTER_VCR_FONT,
        font_size: int = 20,
        text_color: Color = pygame.Color(COLOR_BLUE),
    ) -> Surface:
        font = Font(font_family, font_size)
        y_offset = 5
        lines = text.split("\n")
        text_surfaces: list[Surface] = []
        for line in lines:
            text_surface, _ = font.render(line, text_color)
            text_surfaces.append(text_surface)
        font_surface = Surface(
            (
                max(list(map(lambda surface: surface.get_width(), text_surfaces))),
                sum(list(map(lambda surface: surface.get_height(), text_surfaces)))
                + y_offset * (len(lines) - 1),
            ),
            pygame.SRCALPHA,
        )
        start_height = 0
        for surface in text_surfaces:
            font_surface.blit(surface, (0, start_height))
            start_height += surface.get_height() + y_offset
        return font_surface

    def handle_event(self, event: Event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if not self.check_collide(event.pos):
                    return "close"

                mouse_pos = self.build_local_mouse(event.pos)

                if self.section_tutorial_button.check_collidepoint(mouse_pos):
                    self.section = InstructionSection.TUTORIAL
                if self.section_yaku_overview_button.check_collidepoint(mouse_pos):
                    self.section = InstructionSection.YAKU_OVERVIEW
                if self.section_game_flow_button.check_collidepoint(mouse_pos):
                    self.section = InstructionSection.GAME_FLOW
                if Rect(
                    0,
                    self.section_tab_surface.get_height(),
                    self.section_surface.get_width(),
                    self.section_surface.get_height(),
                ).collidepoint(mouse_pos[0], mouse_pos[1]):
                    section_local_mouse = (
                        mouse_pos[0],
                        mouse_pos[1] - self.section_tab_surface.get_height(),
                    )
                    if self.__prev_button_rect.collidepoint(
                        section_local_mouse[0], section_local_mouse[1]
                    ):
                        self.__turn_prev_page()
                    if self.__next_button_rect.collidepoint(
                        section_local_mouse[0], section_local_mouse[1]
                    ):
                        self.__turn_next_page()
                    if self.close_button.check_collidepoint(section_local_mouse):
                        return "close"
            case pygame.MOUSEMOTION:
                mouse_pos = self.build_local_mouse(event.pos)

                if self.section_tutorial_button.check_collidepoint(mouse_pos):
                    return self.section_tutorial_button
                if self.section_yaku_overview_button.check_collidepoint(mouse_pos):
                    return self.section_yaku_overview_button
                if self.section_game_flow_button.check_collidepoint(mouse_pos):
                    return self.section_game_flow_button
                if Rect(
                    0,
                    self.section_tab_surface.get_height(),
                    self.section_surface.get_width(),
                    self.section_surface.get_height(),
                ).collidepoint(mouse_pos[0], mouse_pos[1]):
                    section_local_mouse = (
                        mouse_pos[0],
                        mouse_pos[1] - self.section_tab_surface.get_height(),
                    )
                    if self.__prev_button_rect.collidepoint(
                        section_local_mouse[0], section_local_mouse[1]
                    ):
                        return "prev"
                    if self.__next_button_rect.collidepoint(
                        section_local_mouse[0], section_local_mouse[1]
                    ):
                        return "next"
                    if self.close_button.check_collidepoint(section_local_mouse):
                        return "close"

            case pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__turn_prev_page()
                elif event.key == pygame.K_RIGHT:
                    self.__turn_next_page()
                elif event.key == pygame.K_UP:
                    self.section = InstructionSection(
                        (self.section.value + 1) % len(InstructionSection)
                    )
                elif event.key == pygame.K_DOWN:
                    self.section = InstructionSection(
                        (self.section.value - 1) % len(InstructionSection)
                    )
                elif event.key == pygame.K_ESCAPE:
                    return "close"

    def create_rescale_surface(self, surface: Surface, scale_by: int):
        return Surface(
            pygame.transform.scale_by(surface, scale_by).get_size(), pygame.SRCALPHA
        )

    def __turn_prev_page(self):
        if self.section == InstructionSection.TUTORIAL:
            self.page = (self.page - 1) % (self.max_instruction_tutorial_page)
        elif self.section == InstructionSection.YAKU_OVERVIEW:
            self.yaku_page = (self.yaku_page - 1) % (self.max_instruction_yaku_page)
        elif self.section == InstructionSection.GAME_FLOW:
            self.game_flow_page = (self.game_flow_page - 1) % (
                self.max_instruction_game_flow_page
            )

    def __turn_next_page(self):
        if self.section == InstructionSection.TUTORIAL:
            self.page = (self.page + 1) % (self.max_instruction_tutorial_page)
        elif self.section == InstructionSection.YAKU_OVERVIEW:
            self.yaku_page = (self.yaku_page + 1) % (self.max_instruction_yaku_page)
        elif self.section == InstructionSection.GAME_FLOW:
            self.game_flow_page = (self.game_flow_page + 1) % (
                self.max_instruction_game_flow_page
            )

    def draw_button_surface(self, button: Button):
        pygame.draw.rect(
            button.get_surface(),
            button.bg_color,
            button.get_surface().get_rect(),
            border_top_left_radius=10,
            border_top_right_radius=10,
        )
        pygame.draw.rect(
            button.get_surface(),
            COLOR_WHITE,
            button.get_surface().get_rect(),
            2,
            border_top_left_radius=10,
            border_top_right_radius=10,
        )
        pygame.draw.line(
            button.get_surface(),
            button.bg_color,
            (2, button.get_surface().get_height() - 2),
            (
                button.get_surface().get_width() - 3,
                button.get_surface().get_height() - 2,
            ),
            2,
        )

    def build_normal_page_surface(
        self, data: InstructionPageData, padding_x: int = 0, padding_y: int = 0
    ) -> Surface:
        surface_list: list[Surface] = []
        for key in data["cards"].keys():
            surface = self.build_instruction_card_surface(data["cards"][f"{key}"])
            surface_list.append(surface)

        body_surface = Surface(
            (
                max(list(map(lambda surface: surface.get_width(), surface_list))),
                sum(list(map(lambda surface: surface.get_height(), surface_list)))
                + padding_y * (len(surface_list) - 1),
            ),
            pygame.SRCALPHA,
        )

        start_height = 0
        for surface in surface_list:
            body_surface.blit(surface, (0, start_height))
            start_height += padding_y + surface.get_height()

        return body_surface

    # region Tutorial Page
    # ---------- BUILDING FOR EACH TUTORIAL PAGE ----------

    def build_page_1_tutorial_surface(self):
        PADDING_X = 200
        PADDING_Y = 25
        PAGE_DATA = self.instruction_tutorial_data["0"]

        man_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["man"])
        pin_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["pin"])
        sou_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["sou"])
        wind_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["wind"])
        dragon_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["dragon"]
        )

        list_wrap_width = [
            man_surface.get_width() + wind_surface.get_width(),
            pin_surface.get_width() + dragon_surface.get_width(),
            sou_surface.get_width(),
        ]
        max_wrap_width = max(list_wrap_width)

        body_surface = Surface(
            (
                max_wrap_width + 3 * PADDING_X,
                max(man_surface.get_height(), wind_surface.get_height())
                + max(pin_surface.get_height(), dragon_surface.get_height())
                + max(sou_surface.get_height(), 0)
                + 4 * PADDING_Y,
            ),
            pygame.SRCALPHA,
        )
        draw_hitbox(body_surface, COLOR_WHITE)

        start_height = PADDING_Y
        # Row 1
        body_surface.blit(man_surface, (PADDING_X, start_height))
        body_surface.blit(
            wind_surface, (man_surface.get_width() + 2 * PADDING_X, start_height)
        )

        # Row 2
        start_height += PADDING_Y + man_surface.get_height()
        body_surface.blit(pin_surface, (PADDING_X, start_height))
        body_surface.blit(
            dragon_surface, (pin_surface.get_width() + 2 * PADDING_X, start_height)
        )

        # Row 3
        start_height += PADDING_Y + pin_surface.get_height()
        body_surface.blit(sou_surface, (PADDING_X, start_height))
        return body_surface

    def build_page_2_tutorial_surface(self):
        PADDING_X = 30
        PADDING_Y = 5
        PAGE_DATA = self.instruction_tutorial_data["1"]

        hand_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["hand"])
        houra_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["houra"])
        triplet_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["triplet"]
        )
        sequence_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["sequence"]
        )
        pair_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["pair"])

        max_wrap_width = max(
            hand_surface.get_width(),
            houra_surface.get_width(),
            (
                triplet_surface.get_width()
                + sequence_surface.get_width()
                + pair_surface.get_width()
                + PADDING_X * 2
            ),
        )

        body_surface = Surface(
            (
                max_wrap_width + PADDING_X * 2,
                hand_surface.get_height()
                + houra_surface.get_height()
                + max(
                    triplet_surface.get_height(),
                    sequence_surface.get_height(),
                    pair_surface.get_height(),
                )
                + PADDING_Y * 4,
            ),
            pygame.SRCALPHA,
        )

        draw_hitbox(body_surface)

        # Row 1
        start_height = PADDING_Y
        body_surface.blit(hand_surface, (PADDING_X, start_height))

        # Row 2
        start_height += hand_surface.get_height() + PADDING_Y
        body_surface.blit(houra_surface, (PADDING_X, start_height))

        # Row 3
        start_height += houra_surface.get_height() + PADDING_Y
        body_surface.blit(sequence_surface, (PADDING_X, start_height))
        body_surface.blit(
            triplet_surface,
            (PADDING_X * 2 + sequence_surface.get_width(), start_height),
        )
        body_surface.blit(
            pair_surface,
            (
                PADDING_X * 3
                + sequence_surface.get_width()
                + triplet_surface.get_width(),
                start_height,
            ),
        )

        return body_surface

    def build_page_3_tutorial_surface(self):

        PAGE_DATA = self.instruction_tutorial_data["2"]

        yaku_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["yaku"])
        return yaku_surface

    def build_page_4_tutorial_surface(self):
        PAGE_DATA = self.instruction_tutorial_data["3"]

        tanyao_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["tanyao"]
        )
        return tanyao_surface

    def build_page_5_tutorial_surface(self):
        PADDING_X = 100
        PADDING_Y = 20
        PAGE_DATA = self.instruction_tutorial_data["4"]

        chii_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["chii"])
        pon_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["pon"])

        body_surface = Surface(
            (
                max(chii_surface.get_width(), pon_surface.get_width()) + PADDING_X * 2,
                chii_surface.get_height() + pon_surface.get_height() + 3 * PADDING_Y,
            ),
            pygame.SRCALPHA,
        )

        start_height = PADDING_Y
        body_surface.blit(chii_surface, (PADDING_X, start_height))

        start_height += chii_surface.get_height() + PADDING_Y
        body_surface.blit(pon_surface, (PADDING_X, start_height))

        return body_surface

    def build_page_6_tutorial_surface(self):
        PAGE_DATA = self.instruction_tutorial_data["5"]

        kan_surface = self.build_instruction_card_surface(PAGE_DATA["cards"]["kan"])

        return kan_surface

    def build_page_7_tutorial_surface(self):
        PAGE_DATA = self.instruction_tutorial_data["6"]

        tenpai_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["tenpai"]
        )
        return tenpai_surface

    def build_page_8_tutorial_surface(self):
        PAGE_DATA = self.instruction_tutorial_data["7"]

        riichi_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["riichi"]
        )

        return riichi_surface

    def build_page_9_tutorial_surface(self):
        PAGE_DATA = self.instruction_tutorial_data["8"]

        yakuhai_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["yakuhai"]
        )
        return yakuhai_surface

    def build_page_10_tutorial_surface(self):
        PADDING_Y = 20
        EACH_CONTENT_PADDING = 10
        PAGE_DATA = self.instruction_tutorial_data["9"]

        furiten_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["furiten"]
        )
        discard_furiten_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["discard_furiten"]
        )
        temporary_furiten_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["temporary_furiten"]
        )
        riichi_furiten_surface = self.build_instruction_card_surface(
            PAGE_DATA["cards"]["riichi_furiten"]
        )

        body_surface = Surface(
            (
                max(
                    sum(
                        list(
                            map(
                                lambda surface: surface.get_width(),
                                [
                                    discard_furiten_surface,
                                    temporary_furiten_surface,
                                    riichi_furiten_surface,
                                ],
                            )
                        )
                        + (
                            [
                                EACH_CONTENT_PADDING
                                * (
                                    len(
                                        [
                                            discard_furiten_surface,
                                            temporary_furiten_surface,
                                            riichi_furiten_surface,
                                        ]
                                    )
                                    - 1
                                )
                            ]
                        )
                    ),
                    furiten_surface.get_width(),
                ),
                max(
                    list(
                        map(
                            lambda surface: surface.get_height(),
                            [
                                discard_furiten_surface,
                                temporary_furiten_surface,
                                riichi_furiten_surface,
                            ],
                        )
                    )
                )
                + furiten_surface.get_height()
                + PADDING_Y,
            ),
            pygame.SRCALPHA,
        )

        start_height = 0

        # Row 1
        body_surface.blit(furiten_surface, (0, start_height))
        start_height += PADDING_Y + furiten_surface.get_height()

        # Row 2
        start_width = 0
        body_surface.blit(discard_furiten_surface, (start_width, start_height))
        start_width += EACH_CONTENT_PADDING + discard_furiten_surface.get_width()
        body_surface.blit(temporary_furiten_surface, (start_width, start_height))
        start_width += EACH_CONTENT_PADDING + temporary_furiten_surface.get_width()

        body_surface.blit(riichi_furiten_surface, (start_width, start_height))
        draw_hitbox(body_surface)
        return body_surface

    # endregion Tutorial Page

    # region Yaku Overview Page
    # ---------- BUILDING FOR EACH YAKU PAGE ----------

    def build_page_1_yaku_surface(self):
        PADDING_Y = 2
        PAGE_DATA = self.instruction_yaku_data["0"]
        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_2_yaku_surface(self):
        PADDING_Y = 10
        PAGE_DATA = self.instruction_yaku_data["1"]
        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_3_yaku_surface(self):
        PADDING_Y = 5
        PAGE_DATA = self.instruction_yaku_data["2"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_4_yaku_surface(self):
        PADDING_Y = 25
        PAGE_DATA = self.instruction_yaku_data["3"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_5_yaku_surface(self):
        PADDING_Y = 30
        PAGE_DATA = self.instruction_yaku_data["4"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_6_yaku_surface(self):
        PADDING_Y = 30
        PAGE_DATA = self.instruction_yaku_data["5"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_7_yaku_surface(self):
        PADDING_Y = 15
        PAGE_DATA = self.instruction_yaku_data["6"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_8_yaku_surface(self):
        PADDING_Y = 5
        PAGE_DATA = self.instruction_yaku_data["7"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_9_yaku_surface(self):
        PAGE_DATA = self.instruction_yaku_data["8"]

        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_10_yaku_surface(self):
        PADDING_Y = 5
        PAGE_DATA = self.instruction_yaku_data["9"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_11_yaku_surface(self):
        PAGE_DATA = self.instruction_yaku_data["10"]

        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_12_yaku_surface(self):
        PAGE_DATA = self.instruction_yaku_data["11"]

        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_13_yaku_surface(self):
        PADDING_Y = 5
        PAGE_DATA = self.instruction_yaku_data["12"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_14_yaku_surface(self):
        PADDING_Y = 10
        PAGE_DATA = self.instruction_yaku_data["13"]
        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_15_yaku_surface(self):
        PADDING_Y = 5
        PAGE_DATA = self.instruction_yaku_data["14"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_16_yaku_surface(self):
        PAGE_DATA = self.instruction_yaku_data["15"]

        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_17_yaku_surface(self):
        PADDING_Y = 20
        PAGE_DATA = self.instruction_yaku_data["16"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    def build_page_18_yaku_surface(self):
        PADDING_Y = 20
        PAGE_DATA = self.instruction_yaku_data["17"]

        return self.build_normal_page_surface(PAGE_DATA, padding_y=PADDING_Y)

    # endregion Yaku Overview Page

    # region Game Flow Page
    # ----- BUILDING FOR EACH GAME FLOW PAGE
    def build_page_1_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["0"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_2_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["1"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_3_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["2"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_4_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["3"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_5_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["4"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_6_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["5"]
        return self.build_normal_page_surface(PAGE_DATA)

    def build_page_7_game_flow(self):
        PAGE_DATA = self.instruction_game_flow_data["6"]
        return self.build_normal_page_surface(PAGE_DATA)

    # endregion Game Flow Page
