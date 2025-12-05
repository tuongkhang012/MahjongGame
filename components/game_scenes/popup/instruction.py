import pygame
from utils.constants import (
    INSTRUCTION_ASSETS,
    COLOR_WHITE,
    BETTER_VCR_FONT,
    COLOR_BLUE,
    COLOR_BLACK,
    ANCIENT_MODERN_FONT,
    INSTRUCTION_TITLE_COLOR,
)
from pygame import Surface, Color, Rect
from pygame.event import Event
from utils.instruction_data_dict import InstructionCard, InstructionTutorialPage
from components.game_scenes.popup.popup import Popup
from utils.enums import InstructionSection
from pygame.freetype import Font
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

        with open("data/instruction_tutorial.json", "r") as file:
            self.instruction_tutorial_data: dict[str, InstructionTutorialPage] = (
                json.load(file)
            )

        arrow = pygame.image.load("public/images/buttons/arrow_up.png")
        self.next_button = pygame.transform.rotate(arrow, -90)
        self.prev_button = pygame.transform.rotate(arrow, 90)
        self.close_button = pygame.image.load("public/images/buttons/close_button.png")

        self.section = InstructionSection.TUTORIAL
        self.page = 0
        self.max_page = len(self.instruction_tutorial_data.keys())

    def change_section(self, section: InstructionSection):
        self.section = section

    def change_page(self, page: int):
        self.page = page

    def build_surface(self, section: InstructionSection, page: int):
        if section == InstructionSection.TUTORIAL:
            self.build_surface_tutorial(page)
        elif section == InstructionSection.YAKU_OVERVIEW:
            self.build_surface_yaku_overview(page)

    def build_surface_tutorial(self, page: int):
        self.set_bg_color(pygame.Color(203, 64, 40))
        self._surface = Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.draw_border_radius()
        try:
            body_surface = getattr(self, f"build_page_{page+1}_tutorial_surface")()
        except Exception as e:
            print(e)
            body_surface = Surface((0, 0), pygame.SRCALPHA)

        try:
            title = self.instruction_tutorial_data[str(self.page)]["title"]
        except:
            title = "Not yet implement data!!!"
        self.build_page_tutorial_surface(title, body_surface)

    def build_surface_yaku_overview(self, page: int):
        pass

    def render(self, screen: Surface):
        self.build_surface(self.section, self.page)
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

    def build_page_tutorial_surface(self, title: str, body_surface: Surface):
        PADDING_X = 20
        PADDING_Y = 20
        title_surface = self.build_font_surface(
            title, font_size=25, text_color=COLOR_WHITE
        )

        center_pos = build_center_rect(self._surface, title_surface)
        self._surface.blit(title_surface, (center_pos.x, PADDING_Y))

        self._surface.blit(
            self.close_button,
            (
                self._surface.get_width() - PADDING_X - self.close_button.get_width(),
                PADDING_Y,
            ),
        )
        self.__close_button_rect = Rect(
            self._surface.get_width() - PADDING_X - self.close_button.get_width(),
            PADDING_Y,
            self.close_button.get_width(),
            self.close_button.get_height(),
        )
        center_pos = build_center_rect(self._surface, body_surface)
        self._surface.blit(body_surface, (center_pos.x, center_pos.y))

        page_number_surface = self.build_font_surface(
            str(self.page + 1), text_color=COLOR_WHITE
        )
        max_height = max(
            page_number_surface.get_height(),
            self.prev_button.get_height(),
            self.next_button.get_height(),
        )

        PADDING_EACH_BUTTON_X = 30
        change_pages_buttons_surface = Surface(
            (
                page_number_surface.get_width()
                + self.prev_button.get_width()
                + self.next_button.get_width()
                + PADDING_X * 2
                + PADDING_EACH_BUTTON_X * 2,
                max_height,
            ),
            pygame.SRCALPHA,
        )

        start_width = PADDING_X
        center_pos = build_center_rect(change_pages_buttons_surface, self.prev_button)
        change_pages_buttons_surface.blit(self.prev_button, (start_width, center_pos.y))
        prev_button_local_position = (start_width, center_pos.y)

        start_width += self.prev_button.get_width() + PADDING_EACH_BUTTON_X
        center_pos = build_center_rect(
            change_pages_buttons_surface, page_number_surface
        )
        change_pages_buttons_surface.blit(
            page_number_surface, (start_width, center_pos.y)
        )

        start_width += page_number_surface.get_width() + PADDING_EACH_BUTTON_X
        center_pos = build_center_rect(change_pages_buttons_surface, self.next_button)
        change_pages_buttons_surface.blit(self.next_button, (start_width, center_pos.y))
        next_button_local_position = (start_width, center_pos.y)

        center_pos = build_center_rect(self._surface, change_pages_buttons_surface)
        change_pages_buttons_position = (
            center_pos.x,
            self._surface.get_height()
            - change_pages_buttons_surface.get_height()
            - PADDING_Y,
        )

        self._surface.blit(change_pages_buttons_surface, change_pages_buttons_position)

        self.__prev_button_rect = Rect(
            change_pages_buttons_position[0] + prev_button_local_position[0],
            change_pages_buttons_position[1] + prev_button_local_position[1],
            self.next_button.get_width(),
            self.next_button.get_height(),
        )
        self.__next_button_rect = Rect(
            change_pages_buttons_position[0] + next_button_local_position[0],
            change_pages_buttons_position[1] + next_button_local_position[1],
            self.next_button.get_width(),
            self.next_button.get_height(),
        )

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

        title_surface.fill((188, 179, 178))
        title_surface.blit(font_surface, (PADDING_X, PADDING_Y))
        # pygame.draw.rect(title_surface, title_end_color, title_surface.get_rect(), 1)

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
                    context.get("resize") is not None and context.get("resize")
                ):
                    context_surfaces.append(pygame.transform.scale_by(image, 2.5))
                else:
                    context_surfaces.append(image)
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
        information_surface.fill((244, 198, 173))

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
        mouse_pos = self.build_local_mouse(event.pos)
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.__prev_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.page = (self.page - 1) % (self.max_page)
                if self.__next_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.page = (self.page + 1) % (self.max_page)
                if self.__close_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    return "close"
            case pygame.MOUSEMOTION:
                if self.__prev_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    return "prev"
                if self.__next_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    return "next"
                if self.__close_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    return "close"

    def create_rescale_surface(self, surface: Surface, scale_by: int):
        return Surface(
            pygame.transform.scale_by(surface, scale_by).get_size(), pygame.SRCALPHA
        )

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
        PADDING_X = 50
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
        PADDING_X = 30
        PADDING_Y = 20
        EACH_CONTENT_PADDING = 30
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

        surface_list = [
            furiten_surface,
            discard_furiten_surface,
            temporary_furiten_surface,
            riichi_furiten_surface,
        ]
        # body_surface = Surface(
        #     (
        #         max(list(map(lambda surface: surface.get_width(), surface_list)))
        #         + PADDING_X * 2,
        #         sum(list(map(lambda surface: surface.get_height(), surface_list)))
        #         + PADDING_Y * (len(surface_list) - 1),
        #     ),
        #     pygame.SRCALPHA,
        # )
        # start_height = PADDING_Y
        # for surface in surface_list:
        #     body_surface.blit(surface, (PADDING_X, start_height))
        #     start_height += PADDING_Y + surface.get_height()
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
                )
                + PADDING_X * 2,
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
                + PADDING_Y * 3,
            ),
            pygame.SRCALPHA,
        )

        start_height = PADDING_Y

        # Row 1
        body_surface.blit(furiten_surface, (PADDING_X, start_height))
        start_height += PADDING_Y + furiten_surface.get_height()

        # Row 2
        start_width = PADDING_X
        body_surface.blit(discard_furiten_surface, (start_width, start_height))
        start_width += EACH_CONTENT_PADDING + discard_furiten_surface.get_width()
        body_surface.blit(temporary_furiten_surface, (start_width, start_height))
        start_width += EACH_CONTENT_PADDING + temporary_furiten_surface.get_width()

        body_surface.blit(riichi_furiten_surface, (start_width, start_height))
        draw_hitbox(body_surface)
        return body_surface
