from pygame import Rect, Surface
from components.entities.fields.field import Field
import pygame
import typing
from pygame.event import Event
from components.entities.mouse import Mouse
from utils.enums import ActionType

if typing.TYPE_CHECKING:
    from components.entities.player import Player
    from components.entities.buttons.tile import Tile
    from components.game_scenes.game_manager import GameManager


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

    def click(self, event: Event, game_manager: "GameManager"):
        player = game_manager.player_list[0]

        update_tiles: list[Tile] = []

        # Check for collide tiles
        collide_tiles = list(
            filter(
                lambda tile: tile.check_collidepoint(self.build_local_mouse(event.pos))
                and not tile.hidden,
                self.get_tiles_list(),
            )
        )
        for tile in collide_tiles:
            tile.clicked()
            update_tiles.append(tile)
            game_manager.action = player.make_move(ActionType.DISCARD)

        # Check for uncollided clicked tiles
        remaining_clicked_tiles = list(
            filter(
                lambda tile: not tile.check_collidepoint(
                    self.build_local_mouse(event.pos)
                )
                and not tile.hidden
                and tile.is_clicked,
                self.get_tiles_list(),
            )
        )
        for tile in remaining_clicked_tiles:
            tile.unclicked()
            update_tiles.append(tile)

        for tile in update_tiles:
            tile.update_clicked(game_manager)

    def unclicked(self, event: Event):
        pass

    def hover(
        self, event: Event, hover_animation: bool = True, hover_highlight: bool = True
    ) -> bool:
        is_hovering_tile = False
        update_tile_list: list[Tile] = []
        # Check for collide tiles
        collide_tile = list(
            filter(
                lambda tile: tile.check_collidepoint(self.build_local_mouse(event.pos))
                and not tile.hidden,
                self.get_tiles_list(),
            )
        )
        for tile in collide_tile:
            is_hovering_tile = True
            if hover_animation:
                tile.hovered()
                update_tile_list.append(tile)

            # Highlight all same tiles
            for tmp_tile in self.__full_tiles_list:
                if (
                    tmp_tile.number == tile.number
                    and tmp_tile.type == tile.type
                    and hover_highlight
                ):
                    tmp_tile.highlighted()
                    update_tile_list.append(tmp_tile)

        # Check for remaining hovered tiles
        remaining_hovered_tiles = list(
            filter(
                lambda tile: not tile.check_collidepoint(
                    self.build_local_mouse(event.pos)
                )
                and not tile.hidden
                and tile.is_hovered,
                self.get_tiles_list(),
            )
        )
        for tile in remaining_hovered_tiles:
            tile.unhovered()
            update_tile_list.append(tile)
            for tmp_tile in self.__full_tiles_list:
                tmp_tile.number == tile.number and tmp_tile.type == tile.type and tmp_tile.unhighlighted() and update_tile_list.append(
                    tmp_tile
                )

        for tile in update_tile_list:
            tile.update_hover()

        return is_hovering_tile

    def unhover(self):
        for tile in self.get_tiles_list():
            tile.unhovered()

            # Unhighlight all tiles
            for tmp_tile in self.__full_tiles_list:
                tmp_tile.is_highlighted and tmp_tile.unhighlighted()

            tile.update_hover()

    def get_tiles_list(self) -> list["Tile"]:
        return self.__tiles_list

    def update_tiles_list(self, tiles_list: list["Tile"]):
        self.__tiles_list = tiles_list
