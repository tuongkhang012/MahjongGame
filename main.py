import pygame
from components.game_scenes.game_manager import GameManager
from utils.helper import get_data_from_file
from utils.enums import GameScene
import sys
import json
from components.game_scenes.scenes_controller import ScenesController
from components.entities.deck import Deck

# Init Scene controller
scenes_controller = ScenesController()

# Run game
if len(sys.argv) > 1 and any([argv.startswith("data=") for argv in sys.argv]):
    data = get_data_from_file(
        list(filter(lambda argv: argv.startswith("data="), sys.argv))[0].split("=")[-1]
    )
    game_manager = GameManager(
        scenes_controller.get_render_surface(),
        scenes_controller,
        init_deck=Deck(),
        start_data=data,
    )
else:
    game_manager = GameManager(
        scenes_controller.get_render_surface(),
        scenes_controller,
        init_deck=Deck(),
    )
running = True

# Add handler for each scene
scenes_controller.handle_scene(GameScene.GAME, game_manager)
while running:
    running = scenes_controller.render()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
