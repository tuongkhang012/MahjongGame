import pygame
import os
from pygame import Surface, Rect
from pygame import Color
from utils.enums import TileType
from utils.constants import TILE_SCALE_BY, TILE_WIDTH, TILE_HEIGHT


class ImageCutter:
    def __init__(self, image: str):
        self.image = pygame.image.load(image).convert_alpha()

    def cut_image(self, x: int, y: int, width: float, height: float) -> Surface:
        return self.image.subsurface(Rect(x * width, y * height, width, height))

    def cut_tiles(
        self,
        tiles_type: TileType,
        tiles_number: int,
        aka: bool,
        player_idx: int = 0,
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
                image_section = 2
            case 2:
                image_section = 3
            case 3:
                image_section = 4

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

        tile_surface = self.cut_image(
            x_left,
            y_top,
            32,
            32,
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
                surface = self.cut_image(0, line, TILE_WIDTH, TILE_HEIGHT)
            case 1:
                if standing:
                    surface = self.cut_image(8, line, TILE_WIDTH, TILE_HEIGHT)

                else:
                    surface = self.cut_image(6, line, TILE_WIDTH, TILE_HEIGHT)

            case 2:
                if standing:
                    surface = self.cut_image(2, line, TILE_WIDTH, TILE_HEIGHT)

                else:
                    surface = self.cut_image(3, line, TILE_WIDTH, TILE_HEIGHT)

            case 3:
                if standing:
                    surface = self.cut_image(8, line, TILE_WIDTH, TILE_HEIGHT)
                else:
                    surface = self.cut_image(6, line, TILE_WIDTH, TILE_HEIGHT)

                surface = pygame.transform.flip(surface, True, False)

        return self._scale_surface(self._trimmed_surface(surface), TILE_SCALE_BY)

    @staticmethod
    def load_frames_from_folder(folder_path: str, max_idx: int) -> list[Surface]:
        """
        Load a list of PNG frames like 0.png, 1.png ... from a given folder path.
        """
        frames: list[Surface] = []
        for i in range(max_idx):
            path = os.path.join(folder_path, f"{i}.png")
            image = pygame.image.load(path).convert_alpha()
            frames.append(image)
        return frames

    @staticmethod
    def tint_surface(surface: Surface, tint_color: Color) -> Surface:
        """
        Return a tinted copy of the given surface.
        """
        tinted_surface = surface.copy()
        tinted_surface.fill((*tint_color, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted_surface

    def _tile_offset_surface(self, x: int, y: int) -> Rect:
        return Rect(x * 32, y * 32, 32, 32)

    def _trimmed_surface(self, surface: Surface) -> Surface:
        pixel_rect = surface.get_bounding_rect()

        trimmed_surface = pygame.Surface(pixel_rect.size, pygame.SRCALPHA)
        trimmed_surface.blit(surface, (0, 0), pixel_rect)
        return trimmed_surface

    def _scale_surface(self, surface: Surface, scale_by: int = 1) -> Surface:
        return pygame.transform.scale_by(surface, scale_by)
