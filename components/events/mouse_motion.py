from pygame import Surface
from components.buttons.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController
from components.mouse import Mouse
import typing

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class MouseMotion(EventController):
    def __init__(
        self, screen: Surface, game_manager: "GameManager", tiles_list: list[Tile] = []
    ):
        super().__init__(tiles_list)
        self.screen = screen
        self.game_manager = game_manager
        self.mouse = Mouse()

    def run(self, event: Event):
        player = self.game_manager.player_list[0]

        deck_field = player.deck_field

        if deck_field.check_collide(event.pos):
            deck_field.hover(event, True, True)
        elif self.game_manager.center_board_field.check_collide(event.pos):
            deck_field.unhover()
            self.discard_field_check_collide(event)
        else:
            deck_field.unhover()
            self.discard_field_unhover_all()

    def discard_field_check_collide(self, event: Event):
        for discard_field in self.game_manager.center_board_field.get_discard_fields():
            if not discard_field.check_collide(event.pos):
                discard_field.unhover()

        for idx, discard_field in enumerate(
            self.game_manager.center_board_field.get_discard_fields()
        ):
            if discard_field.check_collide(event.pos):
                discard_field.hover(event)

    def discard_field_unhover_all(self):
        for discard_field in self.game_manager.center_board_field.get_discard_fields():
            discard_field.unhover()
