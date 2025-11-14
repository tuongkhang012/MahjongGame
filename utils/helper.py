from pygame import Surface, Rect, Color
import pygame
import sys
from utils.enums import CallType, ActionType


def roll_dices() -> int:
    from random import randint

    return randint(2, 12)


def build_center_rect(screen: Surface, image: Surface) -> Rect:
    return image.get_rect(center=screen.get_rect().center)


def draw_hitbox(surface: Surface, color: Color = (255, 0, 0)) -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        pygame.draw.rect(surface, color, surface.get_rect(), 2)


def map_call_to_action(call_type: CallType) -> ActionType:
    return ActionType(call_type.value)


def map_action_to_call(action: ActionType) -> CallType:
    try:
        return CallType(action.value)
    except:
        return None
