import pygame
from utils.constants import FPS_LIMIT, WINDOW_SIZE
from components.game_manager import GameManager

# Run game
game = GameManager()
running = True
while running:
    running = game.run()

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
