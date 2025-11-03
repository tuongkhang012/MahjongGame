import pygame
from pygame import Surface
class TilesCutter:
    def __init__(self, deckImage:str):
        self.image = pygame.image.load(deckImage).convert_alpha()

    def cut_tiles(self, tiles_type: str | None, tiles_number: int | None) -> Surface:
        if tiles_number is not None:
            cropped_surface =  self.image.subsurface(pygame.Rect((tiles_number - 1) * 32, 3 * 32, 32, 32))
            return cropped_surface
        else:
            pass

