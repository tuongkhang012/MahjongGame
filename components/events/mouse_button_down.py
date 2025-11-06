from pygame import Surface
import pygame
from components.tile import Tile
from pygame.event import Event


class MouseButtonDown:
    def __init__(self, screen: Surface, tiles_list: list[Tile]):
        self.screen = screen
        self.tile_list = tiles_list

    def run(self, event: Event):
        print(event.pos)
        for tile in self.tile_list:
            if tile.hidden:
                continue
            if tile.check_collidepoint(event.pos):
                print(tile.type, tile.number, tile.hidden)
