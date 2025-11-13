from pygame import Surface, Rect, Color
import pygame
import sys


def roll_dices() -> int:
    from random import randint

    return randint(2, 12)


def build_center_rect(screen: Surface, image: Surface) -> Rect:
    return image.get_rect(center=screen.get_rect().center)


def draw_hitbox(surface: Surface, color: Color = (255, 0, 0)) -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        pygame.draw.rect(surface, color, surface.get_rect(), 2)
