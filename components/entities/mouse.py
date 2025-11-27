import pygame


class Mouse:
    def default():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def hover():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
