from pygame import Surface
import pygame
from components.buttons.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController
import typing

if typing.TYPE_CHECKING:
    # This line ONLY runs for type checkers
    from components.game_manager import GameManager


class MouseButtonDown(EventController):

    def __init__(
        self,
        screen: Surface,
        game_manager: "GameManager",
        tiles_list: list[Tile] = [],
    ):
        super().__init__(tiles_list)
        self.screen = screen
        self.game_manager = game_manager

    def run(self, event: Event):
        player = self.game_manager.player_list[0]
        if self.game_manager.current_turn != player.direction:
            print(player.direction, self.game_manager.current_turn)
            return
        else:
            print(player.direction, self.game_manager.current_turn)

        update_tiles: list[Tile] = []

        # Check for collide tiles
        collide_tiles = list(
            filter(
                lambda tile: tile.check_collidepoint(event.pos) and not tile.hidden,
                self.get_tiles_list(),
            )
        )
        for tile in collide_tiles:
            tile.clicked()
            update_tiles.append(tile)

        # Check for uncollided clicked tiles
        remaining_clicked_tiles = list(
            filter(
                lambda tile: not tile.check_collidepoint(event.pos)
                and not tile.hidden
                and tile.is_clicked,
                self.get_tiles_list(),
            )
        )
        for tile in remaining_clicked_tiles:
            tile.unclicked()
            update_tiles.append(tile)

        for tile in update_tiles:
            tile.update_clicked(self.game_manager)
