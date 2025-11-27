from utils.enums import GameScene, GamePopup, TileSource
from utils.constants import GAME_TITLE, WINDOW_SIZE, FPS_LIMIT
from utils.game_data_dict import AfterMatchData
import pygame
from pygame import Surface
import typing
from typing import Any
from utils.helper import build_center_rect
from components.game_scenes.popup.after_match import AfterMatchPopup

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager
    from components.entities.buttons.tile import Tile


class ScenesController:
    __scene: GameScene
    __screen: Surface
    __popup_screen: Surface = None

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

    def popup(self, game_popup: GamePopup, data: AfterMatchData):
        match game_popup:
            case GamePopup.AFTER_MATCH:
                self.__popup_screen = self.__create_after_match_popup(data)

    def close_popup(self):
        self.__popup_screen = None

    def create_popup_surface(self, size_ratio: float):
        screen_size = self.__screen.get_size()
        return Surface(
            (screen_size[0] * size_ratio, screen_size[1] * size_ratio), pygame.SRCALPHA
        )

    def render_popup(self):
        if self.__popup_screen:
            overlay = self.__screen.copy().convert_alpha()
            overlay.fill(
                pygame.Color(0, 0, 0, int(255 / 2)), None, pygame.BLEND_RGBA_MULT
            )
            center_pos = build_center_rect(overlay, self.__popup_screen)
            overlay.blit(self.__popup_screen, (center_pos.x, center_pos.y))
            self.__screen.blit(overlay, (0, 0))

    def update_render_surface(self, surface: Surface):
        self.__screen = surface

    def render(self):
        match self.__scene:
            case GameScene.START | GameScene.GAME:
                self.__screen = self.game_manager.render()

        self.render_popup()
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

    def __create_after_match_popup(self, data: AfterMatchData) -> Surface:
        surface = self.create_popup_surface(0.8)
        surface.fill(pygame.Color(0, 0, 0, int(255 * 0.8)))
        popup = AfterMatchPopup(self.create_popup_surface(0.8))
        player_deck = data["player_deck"]
        win_tile = data["win_tile"]
        call_tiles_list = data["call_tiles_list"]
        deltas = data["deltas"]
        player_list = data["player_list"]
        match_result = data["result"]

        tsumi_number = data["tsumi_number"]
        kyoutaku_number = data["kyoutaku_number"]

        # Build render hands surface
        hands_surface_position = (0, 0)
        hands_surface = popup.create_hands_surface(
            player_deck, win_tile, call_tiles_list, height_ratio=2 / 8
        )
        surface.blit(hands_surface, hands_surface_position)

        # Build Yaku, Fu, Han and total points
        result_surface_position = (0, surface.get_height() / 4)
        result_surface = popup.create_result_surface(
            match_result, width_ratio=1 / 2, height_ratio=5 / 8
        )
        surface.blit(result_surface, result_surface_position)

        # Build player current position
        players_surface_position = (surface.get_width() / 2, surface.get_height() / 4)
        players_surface = popup.create_players_surface(
            players=player_list,
            deltas=deltas,
            tsumi_number=tsumi_number,
            kyoutaku_number=kyoutaku_number,
            width_ratio=1 / 2,
            height_ratio=5 / 8,
        )

        surface.blit(players_surface, players_surface_position)

        # Build change scene button (New Game, Main Menu, Quit)
        option_buttons_surface_position = (0, 7 * surface.get_height() / 8)
        option_buttons_surface = popup.create_option_buttons_surface(height_ratio=1 / 8)
        surface.blit(players_surface, option_buttons_surface_position)

        return surface
