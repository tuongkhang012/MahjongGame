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
)
from components.entities.player import Player
from shared.image_cutter import ImageCutter
import math
from pygame.freetype import Font


class CenterBoardField(Field):
    __directions_list: list[Direction]

    screen: Surface
    __direction_width: float
    __direction_height: float

    __discards_fields: list[DiscardField] = []

    __player_list: list[Player]
    # Timer
    start_timer: float

    def __init__(
        self,
        screen: Surface,
        directions_list: list[Direction],
        player_list: list[Player],
    ):
        super().__init__()
        self.__directions_list = directions_list

        for player in player_list:
            self.__discards_fields.append(player.discard_field)

        self.__player_list = player_list

        self.screen = screen
        self.image_cutter = ImageCutter(DIRECTION_IMAGE_LINK)
        self.__direction_width = DIRECTION_WIDTH
        self.__direction_height = DIRECTION_HEIGHT
        self.start_timer = pygame.time.get_ticks()

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
        for idx, discard_field in enumerate(self.__discards_fields):
            discard_field.render()
            relative_position = self.build_discard_surface_position(idx)
            discard_field.update_relative_position(relative_position)

            self.render_surface(surface, discard_field.surface, relative_position)

        return surface

    def build_discard_surface_position(self, idx: int) -> Rect:
        match idx:
            case 0:
                return Rect(
                    180, CENTER_BOARD_FIELD_SIZE[1] - DISCARD_FIELD_SIZE[1], 180, 180
                )
            case 1:
                return Rect(
                    CENTER_BOARD_FIELD_SIZE[0] - DISCARD_FIELD_SIZE[0], 180, 180, 180
                )
            case 2:
                return Rect(180, 0, 180, 180)
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
                turn_surface = self.draw_turn_full()
            else:
                turn_surface = self.draw_turn_empty()
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
            font_surface, font_rect = font.render(f"{player.points}", COLOR_WHITE)
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

        return center_field_surface

    def draw_turn_empty(self) -> Surface:
        turn_surface = Surface((100, 10), pygame.SRCALPHA)
        pygame.draw.rect(
            turn_surface,
            (255, 255, 255),
            turn_surface.get_rect(),
            2,
            border_radius=10,
        )
        return turn_surface

    def draw_turn_full(self) -> Surface:
        turn_surface = Surface((100, 10), pygame.SRCALPHA)
        pygame.draw.rect(
            turn_surface,
            (255, 255, 255),
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
