import pygame
from pygame import Surface
from components.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController
from components.mouse import Mouse


class MouseMotion(EventController):
    def __init__(self, screen: Surface, tiles_list: list[Tile] = []):
        super().__init__(tiles_list)
        self.screen = screen
        self.mouse = Mouse()

    def run(self, event: Event):
        update_tile_list: list[Tile] = []
        for tile in self.get_tiles_list():
            if tile.hidden:
                continue
            if tile.check_collidepoint(event.pos):
                # Hover tile
                tile.hovered()
                update_tile_list.append(tile)

                # Change mouse display
                self.mouse.hover()

                # Highlight all tiles
                for tmp_tile in self.get_tiles_list():
                    tmp_tile.number == tile.number and tmp_tile.type == tile.type and tmp_tile.highlighted()
                    update_tile_list.append(tmp_tile)

            elif tile.is_hovered:
                tile.unhovered()
                update_tile_list.append(tile)
                self.mouse.default()

                # Unhighlight all tiles
                for tmp_tile in self.get_tiles_list():
                    tmp_tile.is_highlighted and tmp_tile.unhighlighted()
                    update_tile_list.append(tmp_tile)

        for tile in update_tile_list:
            tile.update()
