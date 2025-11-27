from pygame import Surface
import pygame
from components.entities.buttons.tile import Tile
from pygame.event import Event
from components.events.event_controller import EventController
from utils.enums import GameScene
import typing

if typing.TYPE_CHECKING:
    from components.game_scenes.main_menu import MainMenu


class MouseButtonDown:
    def __init__(
        self,
        screen: Surface,
        main_menu: "MainMenu",
    ):
        self.screen = screen
        self.main_menu = main_menu

    def run(self, event: Event):
        if self.main_menu.start_button.check_collidepoint(event.pos):
            self.main_menu.scenes_controller.change_scene(
                scene=GameScene.GAME
            )
