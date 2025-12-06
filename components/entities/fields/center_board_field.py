from components.entities.fields.field import Field
from components.entities.fields.discard_field import DiscardField
from utils.enums import Direction
from pygame import Surface, Rect
import pygame
from utils.helper import build_center_rect, draw_hitbox
from utils.constants import (
    DIRECTION_IMAGE_LINK,
    DIRECTION_HEIGHT,
    DIRECTION_WIDTH,
    DIRECTION_TURN_SIZE,
    CENTER_BOARD_FIELD_SIZE,
    DISCARD_FIELD_SIZE,
    MADOU_FUTO_FONT,
    COLOR_WHITE,
    COLOR_BLUE,
    TILES_IMAGE_LINK,
    COLOR_BLACK,
)
from components.entities.player import Player
from shared.image_cutter import ImageCutter
import math
from pygame.freetype import Font
from components.entities.deck import Deck


class CenterBoardField(Field):
    __directions_list: list[Direction]

    screen: Surface
    __direction_width: float
    __direction_height: float

    __discards_fields: list[DiscardField] = []

    __player_list: list[Player]
    # Timer
    start_timer: float

    # Tsumi
    __tsumi_number: int
    __tsumi_image: Surface

    # Kyoutaku
    __kyoutaku_number: int
    __kyoutaku_image: Surface

    def __init__(
        self,
        screen: Surface,
        round_wind: tuple[Direction, int],
        directions_list: list[Direction],
        deck: Deck,
        player_list: list[Player],
        tsumi_number: int,
        kyoutaku_number: int,
    ):
        super().__init__()
        self.__directions_list = directions_list

        self.__discards_fields = []
        for player in player_list:
            self.__discards_fields.append(player.discard_field)

        self.__player_list = player_list
        self.__round_wind = round_wind
        self.deck = deck
        self.screen = screen
        self.image_cutter = ImageCutter(DIRECTION_IMAGE_LINK)
        self.tile_image_cutter = ImageCutter(TILES_IMAGE_LINK)
        self.__direction_width = DIRECTION_WIDTH
        self.__direction_height = DIRECTION_HEIGHT
        self.start_timer = pygame.time.get_ticks()

        # Tsumi, kyoutaku related
        self.__kyoutaku_image = self.tile_image_cutter.cut_image(0, 1, 32, 32, True)
        self.__kyoutaku_number = kyoutaku_number

        self.__tsumi_image = self.tile_image_cutter.cut_image(1, 1, 32, 32, True)
        self.__tsumi_number = tsumi_number

    def render(self, turn: Direction):
        self.surface = self.build_center_surface(turn)

        draw_hitbox(self.surface)
        # Render center surface
        self.render_surface(
            self.screen,
            self.surface,
            build_center_rect(self.screen, self.surface),
        )

        self._absolute_position = build_center_rect(self.screen, self.surface)

        for discard_field in self.__discards_fields:
            discard_field.update_absolute_position(
                Rect(
                    self._absolute_position.x + discard_field.get_relative_position().x,
                    self._absolute_position.y + discard_field.get_relative_position().y,
                    discard_field.surface.get_rect().width,
                    discard_field.surface.get_rect().height,
                )
            )

    def build_center_surface(self, turn: Direction):
        surface = Surface(CENTER_BOARD_FIELD_SIZE, pygame.SRCALPHA)
        draw_hitbox(surface)

        # --- THIS IS FOR INIT THE CENTER FIELD INCLUDE DIRECTION AND TURN BAR ---
        direction_turn_surface = self.build_center_field_default_surface(turn)

        self.render_surface(
            surface,
            direction_turn_surface,
            build_center_rect(surface, direction_turn_surface),
        )

        # Build discard surface
        for idx, discard_field in enumerate(self.__discards_fields):
            discard_surface = discard_field.render()
            relative_position = self.build_discard_surface_position(
                discard_surface, idx
            )
            discard_field.update_relative_position(relative_position)

            self.render_surface(surface, discard_field.surface, relative_position)

        # Build dora surface
        dora_surface = self.build_dora_kyoutaku_tsumi_surface()

        surface.blit(dora_surface, (0, 0))
        return surface

    def build_dora_kyoutaku_tsumi_surface(self) -> Surface:
        TEXT_AND_TILE_MARGIN = 10
        DORA_KYOUTAKU_PADDING = 10
        # Build dora surface:
        dora_kyoutaku_tsumi_surface = Surface(
            (CENTER_BOARD_FIELD_SIZE[0] / 3, CENTER_BOARD_FIELD_SIZE[1] / 3),
            pygame.SRCALPHA,
        )
        max_width = 0
        max_height = 0

        # Build surface for each dora tile
        for dora_tile in self.deck.dora:
            dora_tile.update_tile_surface(0)
            dora_tile.scale_surface(0.8)
            dora_tile.hidden = False
            max_width += dora_tile.get_surface().get_width()
            max_height = max(max_height, dora_tile.get_surface().get_height())

        # Build dora text surface
        dora_font = Font(MADOU_FUTO_FONT, 15)
        dora_text_surface, _ = dora_font.render("DORA", (0, 0, 0))
        # Build a wrap surface for dora text and tile
        dora_tiles_surface = Surface(
            (
                max(max_width, dora_text_surface.get_width() + 20),
                max_height + dora_text_surface.get_height() + TEXT_AND_TILE_MARGIN,
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(dora_tiles_surface, dora_text_surface)

        dora_tiles_surface.blit(dora_text_surface, (center_pos.x, 0))

        start_x_width = build_center_rect(
            dora_tiles_surface, Surface((max_width, max_height), pygame.SRCALPHA)
        ).x
        for dora_tile in self.deck.dora:
            dora_tile.update_position(
                start_x_width,
                dora_text_surface.get_height() + TEXT_AND_TILE_MARGIN,
                dora_tile.get_surface().get_width(),
                dora_tile.get_surface().get_height(),
            )
            dora_tile.render(dora_tiles_surface)
            start_x_width += dora_tile.get_surface().get_width()

        # Wrap all surface
        kyoutaku_surface = self.build_kyoutaku_tsumi_bar_surface(
            dora_kyoutaku_tsumi_surface, True
        )

        tsumi_surface = self.build_kyoutaku_tsumi_bar_surface(
            dora_kyoutaku_tsumi_surface, False
        )

        wrap_all_surface = Surface(
            (
                dora_kyoutaku_tsumi_surface.get_width(),
                dora_tiles_surface.get_height()
                + kyoutaku_surface.get_height()
                + DORA_KYOUTAKU_PADDING,
            ),
            pygame.SRCALPHA,
        )

        center_pos = build_center_rect(wrap_all_surface, dora_tiles_surface)

        wrap_all_surface.blit(dora_tiles_surface, (center_pos.x, 0))

        wrap_all_surface.blit(
            kyoutaku_surface,
            (0, dora_tiles_surface.get_height() + DORA_KYOUTAKU_PADDING),
        )
        wrap_all_surface.blit(
            tsumi_surface,
            (
                dora_kyoutaku_tsumi_surface.get_width() / 2,
                dora_tiles_surface.get_height() + DORA_KYOUTAKU_PADDING,
            ),
        )

        center_pos = build_center_rect(dora_kyoutaku_tsumi_surface, wrap_all_surface)
        dora_kyoutaku_tsumi_surface.blit(wrap_all_surface, (center_pos.x, center_pos.y))
        return dora_kyoutaku_tsumi_surface

    def build_kyoutaku_tsumi_bar_surface(
        self, wrap_surface: Surface, kyoutaku: bool
    ) -> Surface:
        PADDING = 10
        if kyoutaku:
            target_surface = self.__kyoutaku_image
            number = self.__kyoutaku_number
        else:
            target_surface = self.__tsumi_image
            number = self.__tsumi_number

        # Build  bar surface
        text_font = Font(MADOU_FUTO_FONT, 14)
        text_surface, _ = text_font.render(f"X {number}", COLOR_WHITE)
        draw_hitbox(text_surface)
        surface = Surface(
            (
                wrap_surface.get_width() / 2,
                max(text_surface.get_height(), target_surface.get_height()),
            ),
            pygame.SRCALPHA,
        )
        tmp_center_pos_x = 0
        center_pos = build_center_rect(
            surface,
            Surface(
                (
                    text_surface.get_width() + target_surface.get_width() + PADDING,
                    target_surface.get_height(),
                ),
                pygame.SRCALPHA,
            ),
        )
        surface.blit(target_surface, (center_pos.x, center_pos.y))
        tmp_center_pos_x = center_pos.x

        center_pos = build_center_rect(
            surface,
            Surface(
                (
                    text_surface.get_width() + target_surface.get_width() + PADDING,
                    text_surface.get_height(),
                ),
                pygame.SRCALPHA,
            ),
        )
        surface.blit(
            text_surface,
            (tmp_center_pos_x + target_surface.get_width() + PADDING, center_pos.y),
        )
        draw_hitbox(surface, (255, 255, 255))
        return surface

    def build_discard_surface_position(self, surface: Surface, idx: int) -> Rect:
        match idx:
            case 0:
                return Rect(
                    180, CENTER_BOARD_FIELD_SIZE[1] - DISCARD_FIELD_SIZE[1], 180, 180
                )
            case 1:
                return Rect(
                    CENTER_BOARD_FIELD_SIZE[0] - DISCARD_FIELD_SIZE[0],
                    360 - surface.get_height(),
                    180,
                    180,
                )
            case 2:
                return Rect(360 - surface.get_width(), 0, 180, 180)
            case 3:
                return Rect(0, 180, 180, 180)

    def build_center_field_default_surface(self, turn: Direction) -> Surface:
        center_field_surface = Surface(DIRECTION_TURN_SIZE, pygame.SRCALPHA)
        center_field_surface.fill("gray")

        subsurfaces_list: list[Surface] = []
        for idx in range(4):
            subsurface = Surface(
                (DIRECTION_TURN_SIZE[0], self.__direction_height * 2),
                pygame.SRCALPHA,
            )
            draw_hitbox(subsurface)
            subsurfaces_list.append(subsurface)

        # Render direction
        for idx, direction in enumerate(self.get_directions_list()):
            direction_surface = self.image_cutter.cut_image(
                direction.value, 0, self.__direction_width, self.__direction_height
            )
            subsurfaces_list[idx].blit(
                direction_surface,
                (
                    0,
                    subsurfaces_list[idx].get_height() - direction_surface.get_height(),
                ),
            )

        # Render turn bar
        for idx in range(4):
            if (
                turn == self.get_directions_list()[idx]
                and math.floor((pygame.time.get_ticks() - self.start_timer) / 500) % 2
                == 0
            ):
                is_furiten = (
                    self.__player_list[idx].temporary_furiten
                    or self.__player_list[idx].riichi_furiten
                    or self.__player_list[idx].discard_furiten
                )
                turn_surface = self.draw_turn_full(
                    idx, self.__player_list[idx].is_riichi(), is_furiten
                )
            else:
                is_furiten = (
                    self.__player_list[idx].temporary_furiten
                    or self.__player_list[idx].riichi_furiten
                    or self.__player_list[idx].discard_furiten
                )
                turn_surface = self.draw_turn_empty(
                    idx, self.__player_list[idx].is_riichi(), is_furiten
                )
            subsurface_size = subsurfaces_list[idx].get_size()
            half_surface = Surface(
                (subsurface_size[0], subsurface_size[1] / 2), pygame.SRCALPHA
            )
            center_pos = build_center_rect(half_surface, turn_surface)
            subsurfaces_list[idx].blit(
                turn_surface,
                (
                    center_pos.x,
                    subsurfaces_list[idx].get_height()
                    - turn_surface.get_height()
                    - center_pos.y,
                ),
            )

        # Render player points
        for idx, player in enumerate(self.__player_list):
            subsurface_size = subsurfaces_list[idx].get_size()
            half_surface = Surface(
                (subsurface_size[0], subsurface_size[1] / 2), pygame.SRCALPHA
            )
            font = Font(MADOU_FUTO_FONT, 20)
            font_surface, font_rect = font.render(f"{player.points}", COLOR_BLACK)
            center_pos = build_center_rect(half_surface, font_surface)
            subsurfaces_list[idx].blit(
                font_surface,
                (center_pos.x, half_surface.get_height() - font_surface.get_height()),
            )

        # Render subsurface
        for idx, subsurface in enumerate(subsurfaces_list):
            match idx:
                case 0:
                    subsurface_position = (
                        0,
                        DIRECTION_TURN_SIZE[1] - subsurface.get_height(),
                    )
                case 1:
                    subsurface = pygame.transform.rotate(subsurface, 90)
                    subsurface_position = (
                        DIRECTION_TURN_SIZE[0] - subsurface.get_width(),
                        0,
                    )

                case 2:
                    subsurface = pygame.transform.rotate(subsurface, 180)
                    subsurface_position = (0, 0)

                case 3:
                    subsurface = pygame.transform.rotate(subsurface, 270)
                    subsurface_position = (0, 0)

            center_field_surface.blit(subsurface, subsurface_position)

        # Render round wind
        match self.__round_wind[0]:
            case Direction.EAST:
                round_wind_str = f"EAST {self.__round_wind[1]}"
            case Direction.WEST:
                round_wind_str = f"WEST {self.__round_wind[1]}"
            case Direction.SOUTH:
                round_wind_str = f"SOUTH {self.__round_wind[1]}"
            case Direction.NORTH:
                round_wind_str = f"NORTH {self.__round_wind[1]}"
        round_wind_font = Font(MADOU_FUTO_FONT, 14)
        round_wind_surface, _ = round_wind_font.render(round_wind_str, COLOR_BLUE)

        # Render draw tiles left
        draw_tiles_number_font = Font(MADOU_FUTO_FONT, 14)
        draw_tiles_number_surface, _ = draw_tiles_number_font.render(
            f"Draw: {len(self.deck.draw_deck)}"
        )

        # Create wrap surface for round wind and draw tiles left
        WRAP_WIDTH_OFFSET = 30
        WRAP_HEIGHT_OFFSET = 10
        wrap_draw_tiles_round_wind_surface = Surface(
            (
                round_wind_surface.get_width()
                + draw_tiles_number_surface.get_width()
                + WRAP_WIDTH_OFFSET,
                round_wind_surface.get_height()
                + draw_tiles_number_surface.get_height()
                + WRAP_HEIGHT_OFFSET,
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(
            wrap_draw_tiles_round_wind_surface, round_wind_surface
        )
        wrap_draw_tiles_round_wind_surface.blit(round_wind_surface, (center_pos.x, 0))

        center_pos = build_center_rect(
            wrap_draw_tiles_round_wind_surface, draw_tiles_number_surface
        )
        wrap_draw_tiles_round_wind_surface.blit(
            draw_tiles_number_surface,
            (center_pos.x, round_wind_surface.get_height() + WRAP_HEIGHT_OFFSET),
        )

        center_pos = build_center_rect(
            center_field_surface, wrap_draw_tiles_round_wind_surface
        )
        center_field_surface.blit(
            wrap_draw_tiles_round_wind_surface, (center_pos.x, center_pos.y)
        )
        return center_field_surface

    def draw_turn_empty(
        self, player_idx: int, is_riichi: int, furiten: bool = False
    ) -> Surface:
        import sys

        if furiten and (player_idx == 0 or (len(sys.argv) > 1 and "debug" in sys.argv)):
            turn_bar_color = (255, 221, 0)
        elif is_riichi >= 0:
            turn_bar_color = (255, 0, 0)
        else:
            turn_bar_color = (255, 255, 255)
        turn_surface = Surface((100, 10), pygame.SRCALPHA)
        pygame.draw.rect(
            turn_surface,
            turn_bar_color,
            turn_surface.get_rect(),
            2,
            border_radius=10,
        )
        return turn_surface

    def draw_turn_full(
        self, player_idx: int, is_riichi: int, furiten: bool = False
    ) -> Surface:
        import sys

        if furiten and (player_idx == 0 or (len(sys.argv) > 1 and "debug" in sys.argv)):
            turn_bar_color = (255, 221, 0)
        elif is_riichi >= 0:
            turn_bar_color = (255, 0, 0)
        else:
            turn_bar_color = (255, 255, 255)
        turn_surface = Surface((100, 10), pygame.SRCALPHA)
        pygame.draw.rect(
            turn_surface,
            turn_bar_color,
            turn_surface.get_rect(),
            border_radius=10,
        )
        return turn_surface

    def render_surface(self, target_surface: Surface, surface: Surface, position: Rect):
        target_surface.blit(surface, (position.x, position.y))

    def get_directions_list(self):
        return self.__directions_list

    def get_discard_fields(self):
        return self.__discards_fields

    def update_kyoutaku_number(self, number: int):
        self.__kyoutaku_number = number

    def update_tsumi_number(self, number: int):
        self.__tsumi_number = number
