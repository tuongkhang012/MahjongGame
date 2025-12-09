from utils.enums import GameScene, GamePopup, TileSource
from utils.constants import GAME_TITLE, WINDOW_SIZE, FPS_LIMIT, HISTORY_PATH
from utils.game_data_dict import AfterMatchData
from utils.instruction_data_dict import InstructionData
import pygame
from pygame import Surface
import typing
from typing import Any
from utils.helper import build_center_rect, get_data_from_file
from components.game_scenes.popup.after_match import AfterMatchPopup
from components.entities.mouse import Mouse
from components.game_history import GameHistory
from components.entities.deck import Deck
from components.game_scenes.game_manager import GameManager
import os
import json
from components.game_scenes.popup.instruction import Instruction
from components.entities.buttons.button import Button
from components.mixer.mixer import Mixer

if typing.TYPE_CHECKING:
    from components.game_scenes.main_menu import MainMenu
    from components.entities.buttons.tile import Tile
    from components.entities.buttons.button import Button

    from components.game_scenes.popup.popup import Popup


class ScenesController:
    __scene: GameScene
    __screen: Surface
    __popup_screen: "Popup" = None

    game_manager: "GameManager" = None

    def __init__(self, history: GameHistory):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        # pygame.freetype.init()

        pygame.display.set_caption(GAME_TITLE)
        pygame.display.set_icon(pygame.image.load("public/images/sob.ico"))
        # Display setting
        self.__default_screen = pygame.display.set_mode(WINDOW_SIZE)
        self.__screen = pygame.Surface(
            (self.__default_screen.get_width(), self.__default_screen.get_height()),
            pygame.SRCALPHA,
        )

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60

        self.mouse: Mouse = Mouse
        self.__scene = GameScene.START

        self.hoverable_buttons: list["Button"] = []
        self.clickable_buttons: list["Button"] = []

        self.history = history

        self.deck = Deck(self.history.data["seed"] if self.history.data else None)

        self.instruction_manager = Instruction(self.create_popup_surface(0.9))

        self.hints_button = Button()
        hints_button_surface = pygame.transform.scale_by(
            pygame.image.load("public/images/book.png"), 1.4
        )

        hints_button_background = Surface(
            (
                hints_button_surface.get_width() + 5,
                hints_button_surface.get_height() + 5,
            ),
            pygame.SRCALPHA,
        )
        pygame.draw.rect(
            hints_button_background,
            pygame.Color(6, 118, 209),
            hints_button_background.get_rect(),
            border_radius=10,
        )
        hints_button_background.blit(hints_button_surface, (2.5, 2.5))
        self.hints_button.set_surface(hints_button_background)

        self.mixer = Mixer()

    def change_scene(self, scene: GameScene):
        self.__scene = scene

    def get_current_scene(self):
        return self.__scene

    def handle_scene(self, scene: GameScene, handler: Any):
        match scene:
            case GameScene.GAME:
                self.game_manager: "GameManager" = handler
            case GameScene.START:
                self.start_menu: "MainMenu" = handler

    def get_render_surface(self):
        return self.__screen

    def popup(self, game_popup: GamePopup, data: AfterMatchData):
        match game_popup:
            case GamePopup.AFTER_MATCH:
                self.__popup_screen = self.__create_after_match_popup(data)
            case GamePopup.INSTRUCTION:
                self.__popup_screen = self.__create_instruction_popup()
            case GamePopup.SETTING:
                self.__popup_screen = self.__create_setting_popup()

    def close_popup(self):
        self.__popup_screen = None
        if self.game_manager and self.game_manager.pause == True:
            self.game_manager.pause = False

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

            self.__screen.blit(overlay, (0, 0))
            self.__popup_screen.render(self.__screen)

    def update_render_surface(self, surface: Surface):
        self.__screen = surface

    def render(self):
        self.mixer.play_queue()
        match self.__scene:
            case GameScene.GAME:
                self.__screen = self.game_manager.render()
            case GameScene.START:
                if self.history.data is None:
                    self.start_menu.continue_button.disabled()
                self.__screen = self.start_menu.render()

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
                    if self.game_manager:
                        self.game_manager.game_log.end_round(
                            self.game_manager.player_list
                        )
                        self.game_manager.game_log.export()

                        data = self.game_manager.__dict__()
                        data["from_log_name"] = f"{self.game_manager.game_log.name}"
                        self.history.update(data)
                        self.history.export()
                    return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    if self.__popup_screen:
                        button = self.__popup_screen.handle_event(event)
                        if button == "close":
                            self.mouse.default()
                            self.close_popup()
                        elif button:
                            match button.text:
                                case "Main Menu":
                                    self.close_popup()
                                    self.change_scene(GameScene.START)
                                    self.game_manager.new_game()
                                    self.mouse.default()

                                case "New Game":
                                    self.close_popup()
                                    self.change_scene(GameScene.GAME)
                                    self.game_manager.new_game()
                                    self.mixer.clear_queue()
                                    self.mouse.default()

                                case "Quit":
                                    self.game_manager.game_log.export()
                                    return {"exit": True}
                        return {"exit": False}
                    match self.__scene:
                        case GameScene.GAME:
                            if self.game_manager.animation_tile is None:
                                self.game_manager.handle_event(event)
                        case GameScene.START:
                            action = self.start_menu.handle_event(event)
                            log_name = None
                            end_game = False
                            if self.history.data:
                                log_name = (
                                    self.history.data["from_log_name"]
                                    if self.history.data.get("from_log_name")
                                    else None
                                )

                            if action == "New Game":
                                self.deck.random_seed = None
                                if self.history.data:
                                    end_game = self.history.data["end_game"]
                                self.history.data = None
                                for entry in os.listdir(HISTORY_PATH):
                                    file_path = os.path.join(HISTORY_PATH, entry)
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                if log_name:
                                    with open(f".log/{log_name}.json", "r") as file:
                                        json_data = json.load(file)
                                        if (
                                            len(json_data["rounds"]) > 0
                                            and not end_game
                                        ):
                                            json_data["rounds"].remove(
                                                json_data["rounds"][-1]
                                            )
                                    if len(json_data["rounds"]) == 0:
                                        os.remove(f".log/{log_name}.json")
                                    else:
                                        with open(f".log/{log_name}.json", "w") as file:
                                            json.dump(json_data, file)

                            if action == "New Game" or action == "Continue":
                                # Create game manager
                                self.mouse.default()
                                self.create_game_manager()
                                self.change_scene(GameScene.GAME)

                            elif action == "Instruction":
                                self.mouse.default()
                                self.popup(GamePopup.INSTRUCTION, None)
                            elif action == "Quit":
                                return {"exit": True}

                case pygame.MOUSEMOTION:
                    if self.__popup_screen:
                        button = self.__popup_screen.handle_event(event)
                        if button:
                            self.mouse.hover()
                        else:
                            self.mouse.default()
                        return {"exit": False}
                    match self.__scene:
                        case GameScene.GAME:
                            self.game_manager.handle_event(event)
                        case GameScene.START:
                            self.start_menu.handle_event(event)

                case pygame.KEYDOWN:
                    if self.__popup_screen and isinstance(
                        self.__popup_screen, Instruction
                    ):
                        action = self.__popup_screen.handle_event(event)
                        if action and action == "close":
                            self.close_popup()
                    match self.__scene:
                        case GameScene.GAME:
                            self.game_manager.handle_event(event)
                        case GameScene.START:
                            action = self.start_menu.handle_event(event)

        return {"exit": False}

    def create_game_manager(self):
        import sys

        # Run game
        if len(sys.argv) > 1 and any([argv.startswith("data=") for argv in sys.argv]):
            data = get_data_from_file(
                list(filter(lambda argv: argv.startswith("data="), sys.argv))[0].split(
                    "="
                )[-1]
            )
            self.game_manager = GameManager(
                self.get_render_surface(),
                self,
                init_deck=self.deck,
                hints_button=self.hints_button,
                game_history=self.history,
                start_data=data,
            )
        else:
            self.game_manager = GameManager(
                self.get_render_surface(),
                self,
                init_deck=self.deck,
                hints_button=self.hints_button,
                game_history=self.history,
            )
        self.handle_scene(GameScene.GAME, self.game_manager)

    def __create_after_match_popup(self, data: AfterMatchData) -> Surface:
        surface = self.create_popup_surface(0.8)
        surface.fill(pygame.Color(0, 0, 0, int(255 * 0.8)))
        return AfterMatchPopup(surface, data)

    def __create_instruction_popup(self) -> Surface:
        return self.instruction_manager

    def __create_setting_popup(self) -> Surface:
        return
