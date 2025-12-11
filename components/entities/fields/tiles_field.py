from pygame import Surface
from components.entities.fields.field import Field
import typing
from pygame.event import Event

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile


class TilesField(Field):
    __tiles_list: list["Tile"]
    __full_tiles_list: list["Tile"]

    draw_tile_offset: int = 20

    def __init__(
        self,
        screen: Surface,
        player_idx: int,
        tiles_list: list["Tile"],
        full_tiles_list: list["Tile"],
    ):
        super().__init__()
        self.screen = screen
        self.__tiles_list = tiles_list
        self.__full_tiles_list = full_tiles_list
        self.player_idx = player_idx

    def click(self, mouse_pos: tuple[int, int]) -> list["Tile"]:
        # Unclick all tiles
        for tile in self.get_tiles_list():
            tile.unclicked()

        # Check for collide tiles
        collide_tiles = list(
            filter(
                lambda _tile: _tile.check_collidepoint(self.build_local_mouse(mouse_pos))
                and not _tile.hidden,
                self.get_tiles_list(),
            )
        )

        if len(collide_tiles) > 0:
            return collide_tiles

        return None

    def hover(self, mouse_pos: tuple[int, int]) -> list["Tile"]:
        # Check for collide tiles
        collide_tile = list(
            filter(
                lambda tile: tile.check_collidepoint(self.build_local_mouse(mouse_pos))
                and not tile.hidden,
                self.get_tiles_list(),
            )
        )
        if len(collide_tile) > 0:
            return collide_tile

        return None

    def unhover(self):
        for tile in self.get_tiles_list():
            tile.unhovered()

            # Unhighlight all tiles
            for tmp_tile in self.__full_tiles_list:
                # If tile is highlighted, unhighlight it
                tmp_tile.is_highlighted and tmp_tile.unhighlighted()

            tile.update_hover()

    def get_tiles_list(self) -> list["Tile"]:
        return self.__tiles_list

    def update_tiles_list(self, tiles_list: list["Tile"]):
        self.__tiles_list = tiles_list
