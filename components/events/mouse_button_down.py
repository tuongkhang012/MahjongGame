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
        call_button_field = self.game_manager.call_button_field

        if (
            player == self.game_manager.current_player
            and player.deck_field.check_collide(event.pos)
        ):
            player.deck_field.click(event, self.game_manager)

        if (
            player == self.game_manager.calling_player
            and call_button_field.check_collide(event.pos)
        ):
            call_button_field.click(event, self.game_manager)
