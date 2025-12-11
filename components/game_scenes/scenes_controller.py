from utils.enums import GameScene, GamePopup
from utils.constants import (
    GAME_TITLE,
    WINDOW_SIZE,
    FPS_LIMIT,
    HISTORY_PATH,
    ICON_LINK,
    COLOR_WHITE,
    LOG_PATH,
)
from utils.game_data_dict import AfterMatchData
import pygame
from pygame import Surface
import typing
from typing import Any
from utils.helper import get_config, get_data_from_file
from components.game_scenes.popup.after_match import AfterMatchPopup
from components.entities.mouse import Mouse
from components.game_history import GameHistory
from components.entities.deck import Deck
from components.game_scenes.game_manager import GameManager
from components.game_scenes.main_menu import MainMenu
import os
import json
from components.game_scenes.popup.instruction import Instruction
from components.entities.buttons.button import Button
from components.mixer.mixer import Mixer
from components.game_scenes.popup.setting import Setting
from typing import Optional

if typing.TYPE_CHECKING:
    from components.entities.buttons.button import Button
    from components.game_scenes.popup.popup import Popup


class ScenesController:
    """
    Scenes Controller to manage different game scenes.

    :cvar __scene: Current game scene.
    :cvar __screen: Current surface to draw on.
    :cvar __popup_renderer: Current popup screen, if any.
    :cvar game_manager: GameManager instance for the game scene.

    :ivar __default_screen: The main display surface to draw ``__screen`` on.
    :ivar clock: Pygame clock to manage frame rate.
    :ivar mouse: Mouse entity for cursor management.
    :ivar history: GameHistory object containing previous game data.
    :ivar deck: Deck instance for managing the game deck.
    :ivar instruction_manager: Instruction popup manager.
    :ivar hints_button: The button for hints in the game manager.
    :ivar setting_button: The button for open up settings in the game manager.
    :ivar mixer: Mixer instance for audio management.
    """

    __scene: GameScene
    __screen: Surface
    __popup_renderer: Optional[AfterMatchPopup | Instruction | Setting] = None

    game_manager: Optional[GameManager] = None
    start_menu: Optional[MainMenu] = None

    def __init__(self, history: GameHistory) -> None:
        """
        Initializes the ScenesController with the given game history.

        :param history: GameHistory object containing previous game data.
        :type history: GameHistory
        """
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption(GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(os.path.join(ICON_LINK, "icon.png")))
        # Display setting
        self.__default_screen = pygame.display.set_mode(WINDOW_SIZE)
        self.__screen = pygame.Surface(
            size=(
                self.__default_screen.get_width(),
                self.__default_screen.get_height(),
            ),
            flags=pygame.SRCALPHA,  # Allow transparency
        )

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60

        self.mouse: type[Mouse] = Mouse  # Mouse entity (static methods only)
        self.__scene = GameScene.START

        self.history = history

        # Retain the seed if there is previous game history that is not ended
        self.deck = Deck(self.history.data["seed"] if self.history.data else None)

        self.instruction_manager = Instruction(self.create_popup_surface(0.9))

        self.hints_button = self.__create_game_manager_button(
            os.path.join(ICON_LINK, "book.png")
        )
        self.setting_button = self.__create_game_manager_button(
            os.path.join(ICON_LINK, "setting.png")
        )

        config = get_config()
        self.mixer = Mixer(config["bgm"], config["sfx"])
        self.mixer.play_background_music("main_menu")

    def change_scene(self, scene: GameScene) -> None:
        self.__scene = scene

    def get_current_scene(self) -> GameScene:
        return self.__scene

    def handle_scene(self, scene: GameScene, handler: Any) -> None:
        """
        Assigns the handler to the appropriate scene based on the scene type.
        :param scene: The game scene type.
        :type scene: GameScene
        :param handler: The handler object for the scene.
        :type handler: Any
        :return: None
        """
        match scene:
            case GameScene.GAME:
                self.game_manager: "GameManager" = handler
            case GameScene.START:
                self.start_menu: "MainMenu" = handler

    def get_render_surface(self) -> Surface:
        return self.__screen

    def popup(self, game_popup: GamePopup, data: AfterMatchData | None) -> None:
        """
        Creates and displays a popup screen based on the specified game popup type.
        :param game_popup: The type of game popup to display.
        :type game_popup: GamePopup
        :param data: Data required for certain popup types.
        :type data: AfterMatchData
        :return: None
        """
        match game_popup:
            case GamePopup.AFTER_MATCH:
                self.__popup_renderer = self.__create_after_match_popup(data)
            case GamePopup.INSTRUCTION:
                self.__popup_renderer = self.__create_instruction_popup()
            case GamePopup.SETTING:
                self.__popup_renderer = self.__create_setting_popup()

    def close_popup(self) -> None:
        """
        Closes the current popup screen and resumes the game if it was paused.
        :return: None
        """
        self.__popup_renderer = None
        if self.game_manager and (self.game_manager.pause is True):
            self.game_manager.pause = False

    def create_popup_surface(self, size_ratio: float) -> Surface:
        """
        Creates a popup surface with the specified size ratio relative to the screen size.
        :param size_ratio: The size ratio for the popup surface.
        :type size_ratio: float
        :return: Popup surface.
        :rtype: Surface
        """
        screen_size = self.__screen.get_size()
        return Surface(
            size=(screen_size[0] * size_ratio, screen_size[1] * size_ratio),
            flags=pygame.SRCALPHA,
        )

    def render_popup(self) -> None:
        """
        Renders the current popup screen on top of the ``__screen`` with a semi-transparent overlay.
        If there is no popup, this method does nothing.
        :return: None
        """
        if self.__popup_renderer:
            # Create semi-transparent overlay
            overlay = self.__screen.copy().convert_alpha()
            overlay.fill(
                color=pygame.Color(0, 0, 0, int(255 / 2)),
                rect=None,
                special_flags=pygame.BLEND_RGBA_MULT
            )

            self.__screen.blit(overlay, dest=(0, 0))
            self.__popup_renderer.render(self.__screen)

    def update_render_surface(self, surface: Surface) -> None:
        self.__screen = surface

    def render(self) -> bool:
        """
        Act as both the render loop and event listener for the game scenes.
        :return: A boolean indicating whether to continue running the game.
        :rtype: bool
        """
        self.mixer.play_queue()

        # Let the current scene render itself
        match self.__scene:
            case GameScene.GAME:
                self.__screen = self.game_manager.render()

            case GameScene.START:
                if self.history.data is None:
                    self.start_menu.continue_button.disabled()
                self.__screen = self.start_menu.render()

        # Mixer controller
        if self.__popup_renderer and isinstance(self.__popup_renderer, AfterMatchPopup):
            # Stop BGM during after match popup
            self.mixer.play_background_music(None)
        else:
            match self.__scene:
                case GameScene.GAME:
                    if self.game_manager.is_main_riichi: # If main player declared riichi (prioritized)
                        self.mixer.play_background_music("riichi")
                    elif self.game_manager.is_oppo_riichi: # If any opponent declared riichi
                        self.mixer.play_background_music("oppo_riichi")
                    else: # Normal game BGM
                        self.mixer.play_background_music("game")
                case GameScene.START:
                    # Play main menu BGM
                    self.mixer.play_background_music("main_menu")

        self.render_popup()
        self.__default_screen.blit(self.__screen, (0, 0))

        # Listen user event
        event = self.listenEvent()
        if event["exit"]:
            return False
        else:
            return True

    def listenEvent(self) -> dict[str, bool]:
        """
        Listens for user events and handles them accordingly based on the current scene and popup state.
        :return: A dictionary indicating whether to exit the game.
        :rtype: dict[str, bool]
        """
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    while (
                        self.game_manager
                        and self.game_manager.animation_tile is not None
                        # Wait for animation to finish
                    ):
                        self.game_manager.render()
                    else:
                        if self.game_manager:
                            # Finalize and export game log
                            self.game_manager.game_log.end_round(
                                self.game_manager.player_list
                            )
                            self.game_manager.game_log.export()

                            # Update and export game history
                            data = self.game_manager.__dict__()
                            data["from_log_name"] = f"{self.game_manager.game_log.name}"
                            self.history.update(data)
                            self.history.export()

                        # Export settings if in setting popup
                        if self.__popup_renderer and isinstance(
                            self.__popup_renderer, Setting
                        ):
                            self.__popup_renderer.export()
                        return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    if self.__popup_renderer:
                        # Let the corresponding popup handle the event first
                        button = self.__popup_renderer.handle_event(event)
                        if button == "close":
                            # Close the popup and change mouse back to default
                            self.mouse.default()
                            self.close_popup()
                        elif button:
                            match button.text:
                                case "Main Menu":
                                    # Main menu button in after match popup
                                    self.close_popup()
                                    self.start_menu.continue_button.enabled()
                                    self.change_scene(GameScene.START)
                                    self.game_manager.new_game()
                                    self.mouse.default()

                                case "New Game":
                                    # New game button in after match popup
                                    self.close_popup()
                                    self.change_scene(GameScene.GAME)
                                    self.game_manager.new_game()
                                    self.mixer.clear_queue()
                                    self.mouse.default()

                                case "Quit":
                                    # Quit button in after match popup
                                    self.game_manager.game_log.export()
                                    return {"exit": True}
                        return {"exit": False}

                    # Let the current scene handle the event, only if no popup is active
                    match self.__scene:
                        case GameScene.GAME:
                            if self.game_manager.animation_tile is None:
                                self.game_manager.handle_event(event)
                        case GameScene.START:
                            action = self.start_menu.handle_event(event)
                            log_name = None
                            end_game = False
                            # Get previous log name if exist
                            if self.history.data:
                                log_name = (
                                    self.history.data["from_log_name"]
                                    if self.history.data.get("from_log_name")
                                    else None
                                )

                            if action == "New Game": # Starting a new game, need to clear previous history
                                # Clear previous game history if exist
                                self.deck.random_seed = None
                                if self.history.data:
                                    # Check if previous game is ended
                                    end_game = self.history.data["end_game"]
                                self.history.data = None
                                # Delete all history files
                                for entry in os.listdir(HISTORY_PATH):
                                    file_path = os.path.join(HISTORY_PATH, entry)
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                if log_name:
                                    log_path = os.path.join(LOG_PATH, f"{log_name}.json")
                                    with open(log_path, "r") as file:
                                        json_data = json.load(file)
                                        if (
                                            len(json_data["rounds"]) > 0
                                            and not end_game
                                        ):
                                            # If the previous game is not ended, remove the last round
                                            json_data["rounds"].remove(
                                                json_data["rounds"][-1]
                                            )
                                    if len(json_data["rounds"]) == 0:
                                        # If there is no round in the log, delete the log file
                                        os.remove(log_path)
                                    else:
                                        # Update the log file
                                        with open(log_path, "w") as file:
                                            json.dump(json_data, file)

                            if action == "New Game" or action == "Continue":
                                # Create game manager
                                self.mouse.default()
                                self.create_game_manager()
                                self.change_scene(GameScene.GAME)
                            elif action == "Setting":
                                self.mouse.default()
                                self.popup(GamePopup.SETTING, data=None)
                            elif action == "Instruction":
                                self.mouse.default()
                                self.popup(GamePopup.INSTRUCTION, data=None)
                            elif action == "Quit":
                                return {"exit": True}

                case pygame.MOUSEBUTTONUP:
                    # Let the popup handle dragging
                    if self.__popup_renderer:
                        self.__popup_renderer.handle_event(event)

                case pygame.MOUSEMOTION:
                    # Let the popup handle hover events
                    if self.__popup_renderer:
                        button = self.__popup_renderer.handle_event(event)
                        if button:
                            self.mouse.hover()
                        else:
                            self.mouse.default()
                        return {"exit": False}

                    # Let the current scene handle hover events, only if no popup is active
                    match self.__scene:
                        case GameScene.GAME:
                            self.game_manager.handle_event(event)
                        case GameScene.START:
                            self.start_menu.handle_event(event)

                case pygame.KEYDOWN:
                    if self.__popup_renderer and isinstance(
                        self.__popup_renderer, Instruction
                    ): # Let instruction popup handle key events
                        action = self.__popup_renderer.handle_event(event)
                        if action and action == "close":
                            self.close_popup()

                    # Let the current scene handle key events, only if no popup is active
                    match self.__scene:
                        case GameScene.GAME:
                            self.game_manager.handle_event(event)
                        case GameScene.START:
                            action = self.start_menu.handle_event(event)

        return {"exit": False}

    def create_game_manager(self):
        import sys

        if len(sys.argv) > 1 and any([argv.startswith("data=") for argv in sys.argv]): # If there is data argument
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
                setting_button=self.setting_button,
                game_history=self.history,
                start_data=data, # Preset data from file
            )
        else:
            self.game_manager = GameManager(
                self.get_render_surface(),
                self,
                init_deck=self.deck,
                hints_button=self.hints_button,
                setting_button=self.setting_button,
                game_history=self.history,
            )
        # Assign the game manager to the scene controller
        self.handle_scene(GameScene.GAME, self.game_manager)

    def __create_after_match_popup(self, data: AfterMatchData) -> AfterMatchPopup:
        """
        Creates an AfterMatchPopup with the given data.
        :param data: AfterMatchData object containing match results.
        :type data: AfterMatchData
        :return: the After Match Popup instance.
        :rtype: AfterMatchPopup
        """
        surface = self.create_popup_surface(0.9)
        surface.fill(pygame.Color(0, 0, 0, int(255 * 0.8))) # The after match popup is a black translucent surface
        return AfterMatchPopup(surface, data)

    def __create_instruction_popup(self) -> Instruction:
        """
        Creates an Instruction popup.
        :return: the Instruction popup instance.
        :rtype: Instruction
        """
        return self.instruction_manager

    def __create_setting_popup(self) -> Setting:
        """
        Creates a Setting popup.
        :return: the Setting popup instance.
        :rtype: Setting
        """
        surface = self.create_popup_surface(0.6)
        return Setting(surface, get_config(), self.mixer)

    @staticmethod
    def __create_game_manager_button(image_path: str) -> Button:
        """
        Creates a button for the game manager with the given image. (Used for hints and settings buttons)
        :param image_path: Path to the button image.
        :type image_path: str
        :return: the Button instance.
        :rtype: Button
        """
        button = Button()
        button_surface = pygame.transform.scale_by(pygame.image.load(image_path), 1.4)

        button_background = Surface(
            (
                button_surface.get_width() + 5,
                button_surface.get_height() + 5,
            ),
            pygame.SRCALPHA,
        )

        # Draw background
        pygame.draw.rect(
            button_background,
            pygame.Color(6, 118, 209),
            button_background.get_rect(),
            border_radius=10,
        )

        # Draw border
        pygame.draw.rect(
            button_background,
            COLOR_WHITE,
            button_background.get_rect(),
            width=2,
            border_radius=10,
        )

        button_background.blit(button_surface, (2.5, 2.5))
        button.set_surface(button_background)
        return button
