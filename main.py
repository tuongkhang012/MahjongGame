import pygame
from components.game_manager import GameManager
from utils.helper import get_data_from_file
import sys
import json

# Run game
if len(sys.argv) > 1 and any([argv.startswith("data=") for argv in sys.argv]):
    data = get_data_from_file(
        list(filter(lambda argv: argv.startswith("data="), sys.argv))[0].split("=")[-1]
    )
    game = GameManager(start_data=data)
else:
    game = GameManager()
running = True
while running:
    running = game.run()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
