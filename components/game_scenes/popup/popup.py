from pygame import Surface, Rect
from pygame.event import Event


class Popup:
    _absolute_position: Rect
    _surface: Surface

    def __init__(self):
        pass

    @staticmethod
    def render(self, screen: Surface) -> Surface:
        pass

    @staticmethod
    def handle_event(self, event: Event):
        pass

    @classmethod
    def check_collide(self, pos: tuple[int, int]) -> bool:
        return self._absolute_position.collidepoint(pos[0], pos[1])

    @classmethod
    def build_local_mouse(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (
            pos[0] - self._absolute_position.x,
            pos[1] - self._absolute_position.y,
        )

    @classmethod
    def update_absolute_position(self, x: float, y: float):
        self._absolute_position.x = x
        self._absolute_position.y = y

    @classmethod
    def update_absolute_position_rect(self, rect: Rect):
        self._absolute_position = rect
