import pygame


class Mouse:
    def __init__(self):
        pass

    def default(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
