from pygame import Surface, Color
from pygame.freetype import Font
from utils.constants import ANCIENT_MODERN_FONT, COLOR_WHITE, COLOR_GREEN, COLOR_RED
import pygame
from utils.enums import TileSource
import typing
from utils.helper import build_center_rect, draw_hitbox

from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.hand_calculating.yaku import Yaku

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile
    from components.entities.player import Player


class AfterMatchPopup:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.agari_width_offset = 5
        self.call_width_offset = 10
        self.yaku_height_offset = 20

    def create_hands_surface(
        self,
        player_deck: list["Tile"],
        win_tile: "Tile",
        call_tiles_list: list["Tile"] = [],
        width_ratio: float = 1,
        height_ratio: float = 1,
    ) -> Surface:

        full_surface = self.__create_full_surface(
            width_ratio=width_ratio, height_ratio=height_ratio
        )
        max_hands_surface_height = 0
        total_width = 0
        tiles_surface_list: list[Surface] = []

        if win_tile not in player_deck:
            full_hands = player_deck + [win_tile]
        else:
            copy_player_deck = player_deck.copy()
            copy_player_deck.remove(win_tile)
            full_hands = copy_player_deck + [win_tile]

        win_tile_idx = len(full_hands) - 1

        for tile in call_tiles_list:
            if tile == win_tile:
                continue
            if tile not in full_hands:
                full_hands.append(tile)

        start_call_idx = win_tile_idx + 1

        for tile in full_hands:
            if tile.source == TileSource.DRAW:
                view_idx = 0
            elif tile.source == TileSource.PLAYER:
                view_idx = 3
            tile_surface = tile.tiles_cutter.cut_tiles(
                tile.type, tile.number, tile.aka, view_idx
            )
            tiles_surface_list.append(tile_surface)
            total_width += tile_surface.get_width()
            max_hands_surface_height = max(
                max_hands_surface_height, tile_surface.get_height()
            )

        hands_surface = Surface(
            (
                total_width
                + self.agari_width_offset
                + (self.call_width_offset if len(call_tiles_list) > 0 else 0),
                max_hands_surface_height,
            ),
            pygame.SRCALPHA,
        )

        scale_factor = total_width / sum(
            list(map(lambda tile_surface: tile_surface.get_width(), tiles_surface_list))
        )
        start_tile_position = 0
        for surface_idx, tile_surface in enumerate(tiles_surface_list):
            new_tile_surface = pygame.transform.scale_by(tile_surface, scale_factor)

            hands_surface.blit(new_tile_surface, (start_tile_position, 0))
            if surface_idx == start_call_idx - 1:
                start_tile_position += (
                    new_tile_surface.get_width() + self.call_width_offset
                )
            elif surface_idx == win_tile_idx - 1:
                start_tile_position += (
                    new_tile_surface.get_width() + self.agari_width_offset
                )
            else:
                start_tile_position += new_tile_surface.get_width()

        center_pos = build_center_rect(full_surface, hands_surface)
        draw_hitbox(hands_surface)
        full_surface.blit(hands_surface, (center_pos.x, center_pos.y))
        draw_hitbox(full_surface, (0, 0, 255))
        return full_surface

    def create_result_surface(
        self, result: HandResponse, width_ratio: float = 1, height_ratio: float = 1
    ) -> Surface:
        full_surface = self.__create_full_surface(
            width_ratio=width_ratio, height_ratio=height_ratio
        )

        # Build each Yaku surface list
        yaku_surface_list: list[tuple[Surface, Surface]] = []
        yaku_list: list[Yaku] = result.yaku
        for yaku in yaku_list:
            if yaku.han_closed:
                han = yaku.han_closed
            elif yaku.han_open:
                han = yaku.han_open

            yaku_surface = self.__create_font_surface(yaku.name)
            han_surface = self.__create_font_surface(han)

            yaku_surface_list.append((yaku_surface, han_surface))

        # Build Total Han, Fu surface list
        total_han_surface = self.__create_font_surface(
            f"{result.han} Han    {result.fu} Fu"
        )
        # total_fu_surface = self.__create_font_surface(f"Fu: ")
        total_cost_surface = self.__create_font_surface(
            f"Total: {result.cost["total"]}"
        )

        # Render all
        result_surface = self.__create_rescale_surface(
            full_surface, width_scale_by=0.5, height_scale_by=1
        )
        start_height = 0
        for yaku_surface, han_surface in yaku_surface_list:
            result_surface.blit(yaku_surface, (0, start_height))
            result_surface.blit(
                han_surface,
                (result_surface.get_width() - han_surface.get_width(), start_height),
            )
            start_height += yaku_surface.get_height() + self.yaku_height_offset

        seperator_surface = self.__create_seperator_surface(result_surface)
        result_surface.blit(seperator_surface, (0, start_height))
        start_height += seperator_surface.get_height() + self.yaku_height_offset

        result_surface.blit(total_han_surface, (0, start_height))

        start_height += total_han_surface.get_height() + self.yaku_height_offset
        # result_surface.blit(total_fu_surface, (0, start_height))

        # start_height += total_fu_surface.get_height() + self.yaku_height_offset
        result_surface.blit(total_cost_surface, (0, start_height))

        draw_hitbox(result_surface)
        center_pos = build_center_rect(full_surface, result_surface)
        full_surface.blit(result_surface, (center_pos.x, center_pos.y))
        draw_hitbox(full_surface, (0, 0, 255))
        return full_surface

    def create_players_surface(
        self,
        players: list["Player"],
        deltas: list[int],
        tsumi_number: int,
        kyoutaku_number: int,
        width_ratio: float = 1,
        height_ratio: float = 1,
    ):
        full_surface = self.__create_full_surface(width_ratio, height_ratio)

        players_surface = self.__create_rescale_surface(full_surface, 0.9)
        start_height = 0

        table_data = [["Rank", "Player", "Direction", "Points", ""]]

        rearrange_player = players.copy()
        rearrange_player.sort(key=lambda player: player.points, reverse=True)
        for i in range(0, 4):
            table_data.append(
                [
                    i,
                    rearrange_player[i],
                    rearrange_player[i].direction,
                    rearrange_player[i].points,
                    deltas[rearrange_player[i].player_idx] * 100,
                ]
            )

        # render table
        for idx, data in enumerate(table_data):
            rank_data = self.__create_font_surface(data[0])
            players_data = self.__create_font_surface(data[1])
            direction_data = self.__create_font_surface(data[2])
            points_data = self.__create_font_surface(data[3])

            delta_color = None
            if isinstance(data[4], int):
                if data[4] == 0:
                    delta_color = COLOR_WHITE
                elif data[4] > 0:
                    delta_color = COLOR_GREEN
                elif data[4] < 0:
                    delta_color = COLOR_RED

            deltas_data = self.__create_font_surface(
                data[4] if isinstance(data[4], int) and data[4] <= 0 else f"+{data[4]}",
                delta_color,
            )
            max_height = max(
                rank_data.get_height(),
                players_data.get_height(),
                direction_data.get_height(),
                points_data.get_height(),
                deltas_data.get_height(),
            )
            table_data_height = max_height + 20
            rank_column_surface = Surface(
                (players_surface.get_width() / len(data), table_data_height),
                pygame.SRCALPHA,
            )
            player_column_surface = Surface(
                (players_surface.get_width() / len(data), table_data_height),
                pygame.SRCALPHA,
            )
            direction_column_surface = Surface(
                (players_surface.get_width() / len(data), table_data_height),
                pygame.SRCALPHA,
            )
            points_column_surface = Surface(
                (players_surface.get_width() / len(data), table_data_height),
                pygame.SRCALPHA,
            )
            deltas_column_surface = Surface(
                (players_surface.get_width() / len(data), table_data_height),
                pygame.SRCALPHA,
            )
            draw_hitbox(rank_column_surface)
            draw_hitbox(player_column_surface)
            draw_hitbox(direction_column_surface)
            draw_hitbox(points_column_surface)
            draw_hitbox(deltas_column_surface)

            rank_column_surface.blit(
                rank_data,
                (
                    build_center_rect(rank_column_surface, rank_data).x,
                    build_center_rect(rank_column_surface, rank_data).y,
                ),
            )
            player_column_surface.blit(
                players_data,
                (
                    build_center_rect(player_column_surface, players_data).x,
                    build_center_rect(player_column_surface, players_data).y,
                ),
            )
            direction_column_surface.blit(
                direction_data,
                (
                    build_center_rect(player_column_surface, direction_data).x,
                    build_center_rect(player_column_surface, direction_data).y,
                ),
            )
            points_column_surface.blit(
                points_data,
                (
                    build_center_rect(points_column_surface, points_data).x,
                    build_center_rect(points_column_surface, points_data).y,
                ),
            )
            deltas_column_surface.blit(
                deltas_data,
                (
                    build_center_rect(deltas_column_surface, deltas_data).x,
                    build_center_rect(deltas_column_surface, deltas_data).y,
                ),
            )

            start_rank = 0
            start_players = rank_column_surface.get_width()
            start_direction = start_players + player_column_surface.get_width()
            start_points = start_direction + direction_column_surface.get_width()
            start_deltas = start_points + points_column_surface.get_width()

            players_surface.blit(rank_column_surface, (start_rank, start_height))
            players_surface.blit(player_column_surface, (start_players, start_height))
            players_surface.blit(
                direction_column_surface, (start_direction, start_height)
            )
            players_surface.blit(points_column_surface, (start_points, start_height))
            players_surface.blit(deltas_column_surface, (start_deltas, start_height))

            start_height += table_data_height

        center_pos = build_center_rect(full_surface, players_surface)
        full_surface.blit(players_surface, (center_pos.x, center_pos.y))
        return full_surface

    def create_option_buttons_surface(self, height_ratio: float = 1):
        full_surface = self.__create_full_surface(height_ratio=height_ratio)

        # Main menu button
        main_menu_text_surface = self.__create_font_surface("Main Menu")

        # New game button
        new_game_text_surface = self.__create_font_surface("New game")

        # Quit button
        quit_text_surface = self.__create_font_surface("Quit")

    def __create_full_surface(self, width_ratio: float = 1, height_ratio: float = 1):
        return Surface(
            (
                self.surface.get_size()[0] * width_ratio,
                self.surface.get_size()[1] * height_ratio,
            ),
            pygame.SRCALPHA,
        )

    def __create_font_surface(
        self,
        text: str,
        color: Color = COLOR_WHITE,
        font: str = ANCIENT_MODERN_FONT,
        font_size: int = 20,
    ) -> Surface:
        font = Font(ANCIENT_MODERN_FONT, font_size)
        font_surface, _ = font.render(str(text), color)
        return font_surface

    def __create_seperator_surface(self, surface: Surface) -> Surface:
        seperator_width = 0
        seperator_surface: Surface = None
        seperator_str = ""
        while seperator_width < surface.get_width():

            seperator_str += "-"
            seperator_surface = self.__create_font_surface(seperator_str)
            seperator_width = seperator_surface.get_width()

        return seperator_surface

    def __create_rescale_surface(
        self,
        surface: Surface,
        scale_by: float = 1,
        width_scale_by: float = None,
        height_scale_by: float = None,
    ):
        if not width_scale_by:
            width_scale_by = scale_by
        if not height_scale_by:
            height_scale_by = scale_by

        return Surface(
            (
                surface.get_width() * width_scale_by,
                surface.get_height() * height_scale_by,
            ),
            pygame.SRCALPHA,
        )
