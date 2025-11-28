import pygame
import random
from pygame import Surface, Color, Vector2
from components.entities.particles.particle import Particle


class SmokeParticle(Particle):
    def __init__(
        self,
        frames: list[Surface],
        pos: tuple[float, float],
    ):
        vel = Vector2(
            random.uniform(-20, 20),   # x
            random.uniform(-60, -30),  # y (upward)
        )
        gravity = Vector2(0, 0)
        super().__init__(
            frames=frames,
            pos=pos,
            velocity=vel,
            gravity=gravity,
            frame_duration=0.1,
        )