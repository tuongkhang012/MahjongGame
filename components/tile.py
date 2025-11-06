from utils.enums import TilesType
from pygame import Rect
import pygame


class Tile:
    def __init__(self, type: TilesType, number: int):
        self.type = type
        self.number = number
        self.hidden = True
        self.__position = None

    def click(self):
        if self.hidden:
            return

        print(self.type, self.numbder)

    def check_collidepoint(self, position: tuple[int, int]) -> bool:
        return (
            pygame.Rect(self.__position).collidepoint(position[0], position[1])
            if self.__position is not None
            else False
        )

    def update_position(self, x: int, y: int, width: int, height: int):
        self.__position = (x, y, width, height)

    def get_position(self):
        return self.__position
