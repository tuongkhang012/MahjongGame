from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import typing

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

    def click(self):
        return
