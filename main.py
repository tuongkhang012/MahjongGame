import pygame
from utils.enums import GameScene
from utils.constants import HISTORY_PATH, SETTING_CONFIG_PATH, CONSTANT_SETTING_CONFIG
import json
from components.game_scenes.scenes_controller import ScenesController
from components.game_scenes.main_menu import MainMenu
import os
from components.game_history import GameHistory
from pathlib import Path

# Create the history folder if not exist
history_path = Path(HISTORY_PATH)
if not os.path.exists(history_path):
    os.makedirs(history_path)
os.system(f'attrib +h "{history_path}"') # Hide the folder (Windows only)

# Read previous game history if exist
files = []
for entry in os.listdir(history_path):
    file_path = os.path.join(history_path, entry)
    if os.path.isfile(file_path):
        files.append(file_path)

# Read the latest file (highest number)
if len(files) > 0:
    with open(files[-1], "+r") as file:
        json_data = json.load(file)
    game_history = GameHistory(json_data)

    if not json_data["end_game"]: # If the previous game is not ended, delete the file
        os.remove(files[-1])
else:
    game_history = GameHistory()

# Create the setting config file if not exist
config_path = Path(SETTING_CONFIG_PATH)
if not os.path.exists(config_path):
    with open(config_path, "w") as file:
        json.dump(CONSTANT_SETTING_CONFIG, file)


# Init Scene controller
scenes_controller = ScenesController(game_history)

# Initialize Main Menu Scene
start_menu = MainMenu(scenes_controller.get_render_surface(), scenes_controller)
running = True

# Let the ScenesController handle the starting scene
scenes_controller.handle_scene(GameScene.START, start_menu)

# Main Loop
while running:
    running = scenes_controller.render()

    # Update the display
    pygame.display.flip()


pygame.quit()
