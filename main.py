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
        print(file_path)
        files.append(file_path)
if len(files) > 0:
    with open(files[-1], "+r") as file:
        json_data = json.load(file)
    if not json_data["end_game"]:
        game_history = GameHistory(json_data)
        os.remove(files[-1])
    else:
        game_history = GameHistory()
else:
    game_history = GameHistory()


# Init Scene controller
scenes_controller = ScenesController(game_history)


start_menu = MainMenu(scenes_controller.get_render_surface(), scenes_controller)
running = True

# Add handler for each scene
scenes_controller.handle_scene(GameScene.START, start_menu)
while running:
    running = scenes_controller.render()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
