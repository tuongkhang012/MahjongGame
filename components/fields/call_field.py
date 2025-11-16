from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import typing
from components.call import Call

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class CallField(TilesField):
    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__(screen, player_idx, tiles_list, full_tiles_list)
        self.__call_list: list[Call] = []

    def click(self):
        return

    def build_call_fields(self):
        self.surface = Surface

    def add_call(self, call: Call):
        self.__call_list.append(call)
        for tile in call.tiles:
            self.get_tiles_list().append(tile)

    def get_call_list(self) -> list[Call]:
        return self.__call_list
