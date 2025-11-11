from components.fields.tiles_field import TilesField
from pygame import Rect, Surface
import typing

if typing.TYPE_CHECKING:
    from components.player import Player
    from components.buttons.tile import Tile


class PlayField(TilesField):
    def __init__(self, screen: Surface, tiles_list: list["Tile"]):
        super().__init__(screen, tiles_list)
