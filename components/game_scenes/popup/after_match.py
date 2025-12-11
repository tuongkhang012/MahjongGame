from pygame import Surface, Color, Rect
from pygame.event import Event
from pygame.freetype import Font
from utils.constants import (
    ANCIENT_MODERN_FONT,
    COLOR_WHITE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_GREY,
)
import pygame
from utils.enums import TileSource
import typing
from utils.helper import build_center_rect, draw_hitbox
from utils.game_data_dict import AfterMatchData
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.hand_calculating.yaku import Yaku
from components.entities.buttons.button import Button
from components.game_scenes.popup.popup import Popup

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile
    from components.entities.player import Player


class AfterMatchPopup(Popup):
    __absolute_position: Rect

    def __init__(self, surface: Surface, data: AfterMatchData):
        self._surface = surface
        self.agari_width_offset = 5
        self.call_width_offset = 10
        self.yaku_height_offset = 20
        self.table_data_offset = 20
        self.clickable_buttons: list[tuple[tuple[int, int], Button]] = []
        self.hoverable_buttons: list[tuple[tuple[int, int], Button]] = []
        # Create after_match pop up

        self.update_data(data)

    def render(self, screen: Surface):
        if self.ryuukyoku:
            self.render_ryuukyoku(screen)
        else:
            self.render_houra(screen)

    def render_ryuukyoku(self, screen: Surface):
        RYUUKYOU_TEXT_OFFSET = 40
        RYUUKYOKU_REASON_TEXT_OFFSET = 20
        ryuukyoku_text_surface = self.__create_font_surface("RYUUKYOKU", font_size=40)
        center_pos = build_center_rect(self._surface, ryuukyoku_text_surface)
        self._surface.blit(ryuukyoku_text_surface, (center_pos.x, RYUUKYOU_TEXT_OFFSET))

        if self.ryuukyoku_reason:
            reason_text_surface = self.__create_font_surface(f"{self.ryuukyoku_reason}")
            center_pos = build_center_rect(self._surface, reason_text_surface)
            self._surface.blit(
                reason_text_surface,
                (
                    center_pos.x,
                    ryuukyoku_text_surface.get_height()
                    + RYUUKYOU_TEXT_OFFSET
                    + RYUUKYOKU_REASON_TEXT_OFFSET,
                ),
            )

        # Build player current position
        self.__players_surface = self.create_players_surface(
            players=self.player_list,
            deltas=self.deltas,
            tsumi_number=self.tsumi_number,
            kyoutaku_number=self.kyoutaku_number,
            dora=self.dora,
            ura_dora=self.ura_dora,
            ryuukyoku=True,
            width_ratio=1 / 2,
            height_ratio=5 / 8,
        )
        center_pos = build_center_rect(self._surface, self.__players_surface)
        self.players_surface_position = (
            center_pos.x,
            self._surface.get_height() / 4,
        )
        self._surface.blit(self.__players_surface, self.players_surface_position)

        # Build change scene button (New Game, Main Menu, Quit)
        self.option_buttons_surface_position = (0, 7 * self._surface.get_height() / 8)
        self.option_buttons_surface = self.create_option_buttons_surface(
            height_ratio=1 / 8
        )
        self._surface.blit(
            self.option_buttons_surface, self.option_buttons_surface_position
        )

        center_pos = build_center_rect(screen, self._surface)
        self.update_absolute_position_rect(
            Rect(
                center_pos.x,
                center_pos.y,
                self._surface.get_width(),
                self._surface.get_height(),
            )
        )
        screen.blit(self._surface, (center_pos.x, center_pos.y))

    def render_houra(self, screen: Surface):
        # Build render hands surface
        self.hands_surface_position = (0, 0)
        self.__hands_surface = self.create_hands_surface(
            self.player_deck, self.win_tile, self.call_tiles_list, height_ratio=1 / 8
        )
        self._surface.blit(self.__hands_surface, self.hands_surface_position)

        # Build Yaku, Fu, Han and total points
        self.result_surface_position = (0, self._surface.get_height() / 8)
        self.__result_surface = self.create_result_surface(
            self.match_result, width_ratio=1 / 2, height_ratio=3 / 4
        )
        self._surface.blit(self.__result_surface, self.result_surface_position)

        # Build player current position
        self.players_surface_position = (
            self._surface.get_width() / 2,
            self._surface.get_height() / 8,
        )
        self.__players_surface = self.create_players_surface(
            players=self.player_list,
            deltas=self.deltas,
            tsumi_number=self.tsumi_number,
            kyoutaku_number=self.kyoutaku_number,
            dora=self.dora,
            ura_dora=self.ura_dora,
            ryuukyoku=False,
            width_ratio=1 / 2,
            height_ratio=3 / 4,
        )

        self._surface.blit(self.__players_surface, self.players_surface_position)

        # Build change scene button (New Game, Main Menu, Quit)
        self.option_buttons_surface_position = (0, 7 * self._surface.get_height() / 8)
        self.option_buttons_surface = self.create_option_buttons_surface(
            height_ratio=1 / 8
        )
        self._surface.blit(
            self.option_buttons_surface, self.option_buttons_surface_position
        )

        center_pos = build_center_rect(screen, self._surface)
        self.update_absolute_position_rect(
            Rect(
                center_pos.x,
                center_pos.y,
                self._surface.get_width(),
                self._surface.get_height(),
            )
        )
        screen.blit(self._surface, (center_pos.x, center_pos.y))

    def update_data(self, data: AfterMatchData):
        self.player_deck = data["player_deck"]
        self.win_tile = data["win_tile"]
        self.call_tiles_list = data["call_tiles_list"]
        self.deltas = data["deltas"]
        self.player_list = data["player_list"]
        self.match_result = data["result"]

        self.tsumi_number = data["tsumi_number"]
        self.kyoutaku_number = data["kyoutaku_number"]
        self.dora = data["dora"]
        self.ura_dora = data["ura_dora"]
        self.ryuukyoku = data["ryuukyoku"]
        self.ryuukyoku_reason = data["ryuukyoku_reason"]

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

        for tile in reversed(call_tiles_list):
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

            hands_surface.blit(
                new_tile_surface,
                (
                    start_tile_position,
                    hands_surface.get_height() - new_tile_surface.get_height(),
                ),
            )
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
            f"Total: {result.cost['total']}"
        )

        # Render all
        result_surface = self.__create_rescale_surface(
            full_surface, width_scale_by=0.5, height_scale_by=1
        )
        seperator_surface = self.__create_seperator_surface(result_surface)

        total_surface_height = (
            sum(
                list(
                    map(
                        lambda surfaces: max(
                            surfaces[0].get_height(), surfaces[1].get_height()
                        ),
                        yaku_surface_list,
                    )
                )
            )
            + seperator_surface.get_height()
            + max(total_cost_surface.get_height(), total_han_surface.get_height())
            + +(len(yaku_surface_list) + 1) * self.yaku_height_offset
        )
        wrap_surface = Surface(
            (result_surface.get_width(), total_surface_height), pygame.SRCALPHA
        )
        start_height = 0
        for yaku_surface, han_surface in yaku_surface_list:
            wrap_surface.blit(yaku_surface, (0, start_height))
            wrap_surface.blit(
                han_surface,
                (wrap_surface.get_width() - han_surface.get_width(), start_height),
            )
            start_height += yaku_surface.get_height() + self.yaku_height_offset

        wrap_surface.blit(seperator_surface, (0, start_height))
        start_height += seperator_surface.get_height() + self.yaku_height_offset

        wrap_surface.blit(total_han_surface, (0, start_height))

        wrap_surface.blit(
            total_cost_surface,
            (result_surface.get_width() - total_cost_surface.get_width(), start_height),
        )

        center_pos = build_center_rect(result_surface, wrap_surface)
        result_surface.blit(wrap_surface, (center_pos.x, center_pos.y))

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
        dora: list["Tile"],
        ura_dora: list["Tile"],
        ryuukyoku: bool,
        width_ratio: float = 1,
        height_ratio: float = 1,
    ):
        full_surface = self.__create_full_surface(width_ratio, height_ratio)

        players_surface = self.__create_rescale_surface(full_surface, 0.9)
        start_height = 0

        table_data = [["Rank", "Player", "Direction", "Points", ""]]

        rearrange_player = players.copy()
        rearrange_player.sort(
            key=lambda player: (-player.points, player.get_initial_direction().value)
        )
        for i in range(0, 4):
            match i:
                case 0:
                    rank_str = "1st"
                case 1:
                    rank_str = "2nd"
                case 2:
                    rank_str = "3rd"
                case 3:
                    rank_str = "4th"
            table_data.append(
                [
                    rank_str,
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
            table_data_height = max_height + self.table_data_offset
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

        # Dora indicators
        if not ryuukyoku:
            PADDING_DORA_URA_DORA = 60
            start_height += PADDING_DORA_URA_DORA
            dora_surface = self.build_dora_ura_dora_surface(full_surface, "Dora", dora)

            if len(ura_dora) > 0:
                ura_dora_surface = self.build_dora_ura_dora_surface(
                    full_surface, "Ura Dora", ura_dora
                )
            full_surface.blit(dora_surface, (0, start_height))
            if len(ura_dora) > 0:
                full_surface.blit(
                    ura_dora_surface, (full_surface.get_width() / 2, start_height)
                )
            if len(ura_dora) > 0:
                start_height += (
                    max(dora_surface.get_height(), ura_dora_surface.get_height())
                    + self.table_data_offset
                )
            else:
                start_height += dora_surface.get_height() + self.table_data_offset

            tsumi_text_surface = self.__create_font_surface(f"Honba: {tsumi_number}")
            kyoutaku_text_surface = self.__create_font_surface(
                f"Kyoutaku: {kyoutaku_number}"
            )
            tsumi_surface = Surface(
                (full_surface.get_width() / 2, tsumi_text_surface.get_height()),
                pygame.SRCALPHA,
            )
            kyoutaku_surface = Surface(
                (full_surface.get_width() / 2, kyoutaku_text_surface.get_height()),
                pygame.SRCALPHA,
            )

            center_pos = build_center_rect(tsumi_surface, tsumi_text_surface)
            tsumi_surface.blit(tsumi_text_surface, (center_pos.x, 0))

            center_pos = build_center_rect(kyoutaku_surface, kyoutaku_text_surface)
            kyoutaku_surface.blit(kyoutaku_text_surface, (center_pos.x, 0))

            full_surface.blit(tsumi_surface, (0, start_height))
            full_surface.blit(
                kyoutaku_surface, (full_surface.get_width() / 2, start_height)
            )

        center_pos = build_center_rect(full_surface, players_surface)
        full_surface.blit(players_surface, (center_pos.x, center_pos.y))
        draw_hitbox(full_surface, COLOR_WHITE)
        return full_surface

    def build_dora_ura_dora_surface(
        self, full_surface: Surface, text: str, tiles_list: list["Tile"]
    ):
        PADDING_TEXT_AND_TILE = 10
        font_surface = self.__create_font_surface(text)
        tiles_surface_list: list[Surface] = []
        for tile in tiles_list:
            tile_surface = tile.tiles_cutter.cut_tiles(
                tile.type, tile.number, tile.aka, 0
            )
            tiles_surface_list.append(tile_surface)
        tiles_text_list_surface = Surface(
            (
                full_surface.get_width() / 2,
                font_surface.get_height()
                + PADDING_TEXT_AND_TILE
                + max(
                    list(
                        map(
                            lambda surface: surface.get_height(),
                            tiles_surface_list,
                        )
                    )
                ),
            ),
            pygame.SRCALPHA,
        )
        center_pos = build_center_rect(tiles_text_list_surface, font_surface)
        tiles_text_list_surface.blit(font_surface, (center_pos.x, 0))

        PADDING_EACH_TILE = 10
        tiles_list_full_surface = Surface(
            (
                sum(list(map(lambda surface: surface.get_width(), tiles_surface_list)))
                + PADDING_EACH_TILE * (len(tiles_surface_list) - 1),
                max(
                    list(map(lambda surface: surface.get_height(), tiles_surface_list))
                ),
            ),
            pygame.SRCALPHA,
        )
        start_width = 0
        for tile_surface in tiles_surface_list:
            tiles_list_full_surface.blit(tile_surface, (start_width, 0))
            start_width += tile_surface.get_width() + PADDING_EACH_TILE

        center_pos = build_center_rect(tiles_text_list_surface, tiles_list_full_surface)
        tiles_text_list_surface.blit(
            tiles_list_full_surface,
            (center_pos.x, font_surface.get_height() + PADDING_TEXT_AND_TILE),
        )
        return tiles_text_list_surface

    def create_option_buttons_surface(self, height_ratio: float = 1):
        full_surface = self.__create_full_surface(height_ratio=height_ratio)

        # Main menu button
        main_menu_surface = self.__create_rescale_surface(
            full_surface, width_scale_by=1 / 3
        )

        main_menu_button = Button(
            "Main Menu", Font(ANCIENT_MODERN_FONT, 20), COLOR_WHITE, COLOR_GREY
        )
        main_menu_button.set_surface(
            self.__create_rescale_surface(main_menu_surface, 0.5)
        )
        main_menu_button.draw_rect()
        center_pos = build_center_rect(main_menu_surface, main_menu_button.surface)
        main_menu_button.update_position(
            center_pos.x,
            center_pos.y,
            main_menu_button.surface.get_width(),
            main_menu_button.surface.get_height(),
        )
        main_menu_button.render(main_menu_surface)

        # New game button
        new_game_surface = self.__create_rescale_surface(
            full_surface, width_scale_by=1 / 3
        )

        new_game_button = Button(
            "New Game", Font(ANCIENT_MODERN_FONT, 20), COLOR_WHITE, COLOR_GREY
        )
        new_game_button.set_surface(
            self.__create_rescale_surface(new_game_surface, 0.5)
        )
        new_game_button.draw_rect()
        center_pos = build_center_rect(new_game_surface, new_game_button.surface)
        new_game_button.update_position(
            center_pos.x,
            center_pos.y,
            new_game_button.surface.get_width(),
            new_game_button.surface.get_height(),
        )
        new_game_button.render(new_game_surface)

        # Quit button
        quit_surface = self.__create_rescale_surface(full_surface, width_scale_by=1 / 3)

        quit_button = Button(
            "Quit", Font(ANCIENT_MODERN_FONT, 20), COLOR_WHITE, COLOR_GREY
        )
        quit_button.set_surface(self.__create_rescale_surface(quit_surface, 0.5))
        quit_button.draw_rect()
        center_pos = build_center_rect(quit_surface, quit_button.surface)
        quit_button.update_position(
            center_pos.x,
            center_pos.y,
            quit_button.surface.get_width(),
            quit_button.surface.get_height(),
        )
        quit_button.render(quit_surface)

        draw_hitbox(main_menu_surface)
        draw_hitbox(new_game_surface)
        draw_hitbox(quit_surface)

        quit_surface_position = (2 * full_surface.get_width() / 3, 0)
        new_game_surface_position = (full_surface.get_width() / 3, 0)
        main_menu_surface_position = (0, 0)

        full_surface.blit(main_menu_surface, main_menu_surface_position)
        full_surface.blit(new_game_surface, new_game_surface_position)
        full_surface.blit(quit_surface, quit_surface_position)

        self.hoverable_buttons = [
            (quit_surface_position, quit_button),
            (new_game_surface_position, new_game_button),
            (main_menu_surface_position, main_menu_button),
        ]
        self.clickable_buttons = [
            (quit_surface_position, quit_button),
            (new_game_surface_position, new_game_button),
            (main_menu_surface_position, main_menu_button),
        ]

        return full_surface

    def __create_full_surface(self, width_ratio: float = 1, height_ratio: float = 1):
        return Surface(
            (
                self._surface.get_size()[0] * width_ratio,
                self._surface.get_size()[1] * height_ratio,
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

    def handle_event(self, event: Event) -> Button | None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN | pygame.MOUSEMOTION:
                if self.check_collide(event.pos):
                    # Check collide with scene change option
                    local_mouse = self.build_local_mouse(event.pos)

                    option_buttons_rect = self.option_buttons_surface.get_rect().copy()
                    option_buttons_rect.x = self.option_buttons_surface_position[0]
                    option_buttons_rect.y = self.option_buttons_surface_position[1]
                    mouse_inside_option_surface = (
                        local_mouse[0] - option_buttons_rect.x,
                        local_mouse[1] - option_buttons_rect.y,
                    )
                    if self.option_buttons_surface.get_rect().collidepoint(
                        mouse_inside_option_surface
                    ):
                        for position, button in self.clickable_buttons:
                            if Rect(
                                position[0],
                                position[1],
                                option_buttons_rect.width / 3,
                                option_buttons_rect.height,
                            ).collidepoint(mouse_inside_option_surface):
                                mouse_inside_each_button = (
                                    mouse_inside_option_surface[0] - position[0],
                                    mouse_inside_option_surface[1] - position[1],
                                )
                                if button.get_position().collidepoint(
                                    mouse_inside_each_button
                                ):
                                    return button
