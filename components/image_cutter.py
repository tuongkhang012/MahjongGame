import pygame
from pygame import Surface
from utils.enums import TilesType
from utils.constants import TILE_SCALE_BY


class TilesCutter:
    def __init__(self, deckImage: str):
        self.image = pygame.image.load(deckImage).convert_alpha()

    def cut_tiles(
        self,
        tiles_type: TilesType,
        tiles_number: int,
        player_idx: int = 1,
    ) -> Surface:
        match tiles_type:
            case TilesType.MAN:
                vertical_line_order = 0
            case TilesType.SOU:
                vertical_line_order = 1
            case TilesType.PIN:
                vertical_line_order = 2
            case TilesType.WIND | TilesType.DRAGON:
                vertical_line_order = 3
            case TilesType.AKA:
                vertical_line_order = 4

        match player_idx:
            case 1:
                image_section = 1
            case 2:
                image_section = 4
            case 3:
                image_section = 3
            case 4:
                image_section = 2
        x_left = (
            tiles_number - 1 if tiles_type != TilesType.DRAGON else tiles_number + 3
        )
        y_top = 3 + vertical_line_order + 5 * image_section

        tile_surface = self.image.subsurface(
            pygame.Rect(
                self._tile_offset_surface(x_left, y_top),
            )
        )

        return self._scale_surface(self._trimmed_surface(tile_surface), TILE_SCALE_BY)

    def cut_hidden_tiles(
        self,
        standing: bool,
        player_idx: int = 1,
    ) -> Surface:
        line = 2
        match player_idx:
            case 1:
                surface = self.image.subsurface(
                    pygame.Rect(self._tile_offset_surface(0, line))
                )
            case 2:
                if standing:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(8, line))
                    )
                else:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(6, line))
                    )
                surface = pygame.transform.flip(surface, True, False)
            case 3:
                if standing:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(2, line))
                    )
                else:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(3, line))
                    )
            case 4:
                if standing:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(8, line))
                    )
                else:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(6, line))
                    )
        return self._scale_surface(self._trimmed_surface(surface), TILE_SCALE_BY)

    def _tile_offset_surface(self, x: int, y: int) -> tuple[int, int, int, int]:
        return (x * 32, y * 32, 32, 32)

    def _trimmed_surface(self, surface: Surface) -> Surface:
        pixel_rect = surface.get_bounding_rect()

        trimmed_surface = pygame.Surface(pixel_rect.size, pygame.SRCALPHA)
        trimmed_surface.blit(surface, (0, 0), pixel_rect)
        return trimmed_surface

    def _scale_surface(self, surface: Surface, scale_by: int = 1) -> Surface:
        return pygame.transform.scale_by(surface, scale_by)
