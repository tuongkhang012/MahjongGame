from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import typing
from utils.helper import build_center_rect
import pygame

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class DeckField(TilesField):
    def __init__(self, screen: Surface, tiles_list: list["Tile"]):
        super().__init__(screen, tiles_list)

    def render(self, player: "Player"):
        self.build_tiles_position(player)
        self.build_field_surface(player)
        if (
            player.player_idx == 1
            and player.get_draw_tile() == player.player_deck[-1]
            and len(player.player_deck) >= 14
        ):
            player.player_deck[-1].render(self.surface)
            for tile in player.player_deck[:-1]:
                tile.render(self.surface)

        else:
            for tile in player.player_deck:
                tile.render(self.surface)

        match player.player_idx:
            case 0 | 2:
                half_screen_surface = Surface(
                    (self.screen.get_width(), self.screen.get_height() / 3),
                    pygame.SRCALPHA,
                )

            case 1 | 3:
                half_screen_surface = Surface(
                    (self.screen.get_width() / 3, self.screen.get_height()),
                    pygame.SRCALPHA,
                )

        position = build_center_rect(half_screen_surface, self.surface)

        pygame.draw.rect(self.surface, (255, 0, 0), self.surface.get_rect(), 2)
        pygame.draw.rect(
            half_screen_surface, (255, 0, 0), half_screen_surface.get_rect(), 2
        )

        half_screen_surface.blit(self.surface, (position.x, position.y))
        match player.player_idx:
            case 0:
                self.screen.blit(
                    half_screen_surface, (0, 2 * self.screen.get_height() / 3)
                )

            case 1:
                self.screen.blit(
                    half_screen_surface,
                    (2 * self.screen.get_width() / 3, 0),
                )

            case 2 | 3:
                self.screen.blit(half_screen_surface, (0, 0))
