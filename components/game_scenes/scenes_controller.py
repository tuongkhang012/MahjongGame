from utils.enums import GameScene
from utils.constants import GAME_TITLE, WINDOW_SIZE, FPS_LIMIT
import pygame
from pygame import Surface
import typing
from typing import Any

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


class ScenesController:
    __scene: GameScene
    __screen: Surface

    def __init__(self):
        pygame.init()
        # pygame.mixer.init()
        # pygame.freetype.init()

        pygame.display.set_caption(GAME_TITLE)

        # Display setting
        self.__default_screen = pygame.display.set_mode(WINDOW_SIZE)
        self.__screen = pygame.Surface(
            (self.__default_screen.get_width(), self.__default_screen.get_height()),
            pygame.SRCALPHA,
        )

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60

        self.__scene = GameScene.GAME

    def change_scene(self, scene: GameScene):
        self.__scene = scene

    def handle_scene(self, scene: GameScene, handler: Any):
        match scene:
            case GameScene.GAME:
                self.game_manager: "GameManager" = handler

    def get_render_surface(self):
        return self.__screen

    def update_render_surface(self, surface: Surface):
        self.__screen = surface

    def render(self):
        match self.__scene:
            case GameScene.START | GameScene.GAME:
                self.__screen = self.game_manager.render()
        self.__default_screen.blit(self.__screen, (0, 0))

        # Listen user event
        event = self.listenEvent()
        if event["exit"] == True:
            return False
        else:
            return True

    def listenEvent(self) -> dict[str, bool]:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    match self.__scene:
                        case GameScene.GAME:
                            if self.game_manager.animation_tile is None:
                                self.game_manager.mouse_button_down.run(event)

                case pygame.MOUSEMOTION:
                    match self.__scene:
                        case GameScene.GAME:
                            self.game_manager.mouse_motion.run(event)

        return {"exit": False}
