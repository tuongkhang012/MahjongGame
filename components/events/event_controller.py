from components.buttons.tile import Tile
from pygame.event import Event


class EventController:
    def __init__(self, tiles_list: list[Tile] = []):
        self.__tiles_list = tiles_list

    def update_tiles_list(self, tiles_list: list[Tile]):
        self.__tiles_list = tiles_list
        return self

    def get_tiles_list(self):
        return self.__tiles_list
