import pygame
from utils.constants import FPS_LIMIT, WINDOW_SIZE
from components.game_manager import GameManager

# Run game
game = GameManager()
running = True
while running:
    running = game.run()

    # fill the screen with a color to wipe away anything from last frame

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
