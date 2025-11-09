from pygame import Surface
from components.buttons.tile import Tile
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

        # Check for collide tiles
        collide_tile = list(
            filter(
                lambda tile: tile.check_collidepoint(event.pos) and not tile.hidden,
                self.get_tiles_list(),
            )
        )
        for tile in collide_tile:
            # Hover tile
            tile.hovered()
            update_tile_list.append(tile)

            # Change mouse display
            self.mouse.hover()

            # Highlight all tiles
            for tmp_tile in self.get_tiles_list():
                tmp_tile.number == tile.number and tmp_tile.type == tile.type and tmp_tile.highlighted()
                update_tile_list.append(tmp_tile)

        # Check for remaining hovered tiles
        remaining_hovered_tiles = list(
            filter(
                lambda tile: not tile.check_collidepoint(event.pos)
                and not tile.hidden
                and tile.is_hovered,
                self.get_tiles_list(),
            )
        )
        for tile in remaining_hovered_tiles:
            tile.unhovered()
            update_tile_list.append(tile)
            self.mouse.default()

            # Unhighlight all tiles
            for tmp_tile in self.get_tiles_list():
                tmp_tile.is_highlighted and tmp_tile.unhighlighted()
                update_tile_list.append(tmp_tile)

        for tile in update_tile_list:
            tile.update()
