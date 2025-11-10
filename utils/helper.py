from pygame import Surface, Rect


def roll_dices() -> int:
    from random import randint

    return randint(2, 12)


def build_center_rect(screen: Surface, image: Surface) -> Rect:
    return image.get_rect(center=screen.get_rect().center)
