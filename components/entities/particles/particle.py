import pygame
import random
from pygame import Surface, Color, Rect, Vector2

from shared.image_cutter import ImageCutter


class Particle:
    """
    Base Particle class
    """
    def __init__(
        self,
        frames: list[Surface],
        pos: tuple[float, float],
        velocity: Vector2,
        gravity: Vector2,
        frame_duration: float = 0.06,
    ):
        self.pos = Vector2(pos)
        self.velocity = velocity
        self.gravity = gravity

        self.frames: list[Surface] = frames

        self.frame_idx: int = 0
        self.frame_time: float = 0.0
        self.frame_duration: float = frame_duration

        self.dead: bool = False

    def update(self, delta_time: float) -> None:
        if self.dead:
            return

        # Update animation frame
        self.frame_time += delta_time
        while self.frame_time >= self.frame_duration:
            self.frame_time -= self.frame_duration
            self.frame_idx += 1
            if self.frame_idx >= len(self.frames):
                self.dead = True
                return

        # Update position
        self.velocity += self.gravity * delta_time
        self.pos += self.velocity * delta_time

    def draw(self, screen: Surface):
        if self.dead:
            return
        frame = self.frames[self.frame_idx]
        rect = frame.get_rect(center=(self.pos.x, self.pos.y))
        screen.blit(frame, rect)