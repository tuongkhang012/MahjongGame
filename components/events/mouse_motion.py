from pygame import Surface
from components.entities.buttons.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController
from components.entities.mouse import Mouse
import typing

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


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
        call_button_field = self.game_manager.call_button_field
        center_board_field = self.game_manager.center_board_field
        deck_field = player.deck_field

        deck_field_hover = False
        center_board_field_hover = False
        call_button_field_hover = False
        if deck_field.check_collide(event.pos):
            deck_field_hover = deck_field.hover(event, True, True)
        elif center_board_field.check_collide(event.pos):
            deck_field.unhover()
            center_board_field_hover = self.__discard_field_check_collide(event)
        else:
            deck_field.unhover()
            self.__discard_field_unhover_all()

        if call_button_field.check_collide(event.pos):
            call_button_field_hover = call_button_field.hover(event)
        else:
            call_button_field.unhover()

        if deck_field_hover or center_board_field_hover or call_button_field_hover:
            self.mouse.hover()
        else:
            self.mouse.default()

    def __discard_field_check_collide(self, event: Event) -> bool:
        center_board_field = self.game_manager.center_board_field

        for discard_field in center_board_field.get_discard_fields():
            if not discard_field.check_collide(event.pos):
                discard_field.unhover()

        for idx, discard_field in enumerate(center_board_field.get_discard_fields()):
            if discard_field.check_collide(event.pos):
                return discard_field.hover(event)

    def __discard_field_unhover_all(self):
        center_board_field = self.game_manager.center_board_field

        for discard_field in center_board_field.get_discard_fields():
            discard_field.unhover()
