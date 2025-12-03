import pygame
from components.game_scenes.game_manager import GameManager
from utils.helper import get_data_from_file
from utils.enums import GameScene
import sys
import json
from components.game_scenes.scenes_controller import ScenesController
from components.entities.deck import Deck
from components.game_scenes.main_menu import MainMenu
import os
from components.game_history import GameHistory

# Init game history
files = []
for entry in os.listdir(".history/"):
    file_path = os.path.join(".history/", entry)
    if os.path.isfile(file_path):
        files.append(file_path)
if len(files) > 0:
    with open(files[-1], "+r") as json_data:
        game_history = GameHistory(json.load(json_data))
    # os.remove(files[-1])
else:
    game_history = GameHistory()


# Init Scene controller
scenes_controller = ScenesController(game_history)

# Run game
if len(sys.argv) > 1 and any([argv.startswith("data=") for argv in sys.argv]):
    data = get_data_from_file(
        list(filter(lambda argv: argv.startswith("data="), sys.argv))[0].split("=")[-1]
    )
    game_manager = GameManager(
        scenes_controller.get_render_surface(),
        scenes_controller,
        init_deck=Deck(),
        game_history=game_history,
        start_data=data,
    )
else:
    game_manager = GameManager(
        scenes_controller.get_render_surface(),
        scenes_controller,
        init_deck=Deck(),
        game_history=game_history,
    )

start_menu = MainMenu(scenes_controller.get_render_surface(), scenes_controller)
running = True

# Add handler for each scene
scenes_controller.handle_scene(GameScene.GAME, game_manager)
scenes_controller.handle_scene(GameScene.START, start_menu)
while running:
    running = scenes_controller.render()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
