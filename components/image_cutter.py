import pygame
from pygame import Surface
from utils.enums import TileType
from utils.constants import TILE_SCALE_BY


class TilesCutter:
    def __init__(self, deckImage: str):
        self.image = pygame.image.load(deckImage).convert_alpha()

    def cut_tiles(
        self,
        tiles_type: TileType,
        tiles_number: int,
        aka: bool,
        player_idx: int = 1,
    ) -> Surface:
        if aka:
            vertical_line_order = 4
        else:
            match tiles_type:
                case TileType.MAN:
                    vertical_line_order = 0
                case TileType.SOU:
                    vertical_line_order = 1
                case TileType.PIN:
                    vertical_line_order = 2
                case TileType.WIND | TileType.DRAGON:
                    vertical_line_order = 3

        match player_idx:
            case 0:
                image_section = 1
            case 1:
                image_section = 4
            case 2:
                image_section = 3
            case 3:
                image_section = 2

        # Handle image vertical line for each tile type
        y_top = 3 + vertical_line_order + 5 * image_section

        # Handle image index for each vertical line in image
        if aka:
            match tiles_type:
                case TileType.MAN:
                    x_left = 0

                case TileType.SOU:
                    x_left = 1

                case TileType.PIN:
                    x_left = 2
        else:
            x_left = (
                tiles_number - 1 if tiles_type != TileType.DRAGON else tiles_number + 3
            )

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
            case 0:
                surface = self.image.subsurface(
                    pygame.Rect(self._tile_offset_surface(0, line))
                )
            case 1:
                if standing:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(8, line))
                    )
                else:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(6, line))
                    )
                surface = pygame.transform.flip(surface, True, False)
            case 2:
                if standing:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(2, line))
                    )
                else:
                    surface = self.image.subsurface(
                        pygame.Rect(self._tile_offset_surface(3, line))
                    )
            case 3:
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
