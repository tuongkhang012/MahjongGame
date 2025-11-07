from pygame import Surface
import pygame
from components.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController


class MouseButtonDown(EventController):

    def __init__(self, screen: Surface, tiles_list: list[Tile] = []):
        super().__init__(tiles_list)
        self.screen = screen

    def run(self, event: Event):
        update_tiles: list[Tile] = []
        for tile in self.get_tiles_list():
            if tile.hidden:
                continue
            if tile.check_collidepoint(event.pos):
                tile.clicked()
                update_tiles.append(tile)
                break
            else:
                for tmp_tile in filter(
                    lambda tile: tile.is_clicked == True, self.get_tiles_list()
                ):
                    tmp_tile.unclicked()
                    update_tiles.append(tile)

        for tile in update_tiles:
            tile.update()
