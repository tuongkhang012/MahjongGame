from pygame import Surface, Rect, Color
from pygame.event import Event
import pygame


class Popup:
    _absolute_position: Rect = None
    _surface: Surface = None
    bg_color: Color = None

    def __init__(self):
        self._absolute_position = Rect(0, 0, 0, 0)
        pass

    def render(self, screen: Surface):
        pass

    def handle_event(self, event: Event):
        pass

    def set_bg_color(self, color: Color):
        self.bg_color = color

    def check_collide(self, pos: tuple[int, int]) -> bool:
        return (
            self._absolute_position.collidepoint(pos[0], pos[1])
            if self._absolute_position
            else False
        )

    def draw_border_radius(self, border_color: Color = (255, 255, 255)):
        pygame.draw.rect(
            self._surface,
            self.bg_color,
            self._surface.get_rect(),
            border_radius=10,
        )

        pygame.draw.rect(
            self._surface, border_color, self._surface.get_rect(), 2, border_radius=10
        )

    def draw_surface_border_radius(
        self,
        surface: Surface,
        border_color: Color = (255, 255, 255),
    ):
        pygame.draw.rect(
            surface,
            self.bg_color,
            surface.get_rect(),
            border_radius=10,
        )
        pygame.draw.rect(surface, border_color, surface.get_rect(), 2, border_radius=10)

    def build_local_mouse(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (
            pos[0] - self._absolute_position.x,
            pos[1] - self._absolute_position.y,
        )

    def update_absolute_position(self, x: float, y: float):
        self._absolute_position.x = x
        self._absolute_position.y = y

    def check_collide(self, mouse_pos: tuple[int, int]):
        return (
            True
            if self._absolute_position
            and self._absolute_position.collidepoint(mouse_pos[0], mouse_pos[1])
            else False
        )

    def update_absolute_position_rect(self, rect: Rect):
        self._absolute_position = rect
