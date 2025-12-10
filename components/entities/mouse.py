import pygame


class Mouse:
    @staticmethod
    def default():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    @staticmethod
    def hover():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
