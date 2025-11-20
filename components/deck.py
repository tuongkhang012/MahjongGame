from components.buttons.tile import Tile
from utils.enums import TileType
from utils.helper import (
    roll_dices,
    get_data_from_file,
    parse_string_tile,
    split_every_n_chars,
    find_suitable_tile_in_list,
)
import sys
from typing import Any


class Deck:
    # Main
    full_deck: list[Tile] = []
    death_wall: list[Tile] = []
    draw_deck: list[Tile] = []

    # Dora relative
    dora: list[Tile] = []
    ura_dora: list[Tile] = []

    def __init__(self, start_data: Any | None = None):
        self.create_new_deck(start_data)

    def create_new_deck(self, start_data: Any | None = None) -> dict[str, list[Tile]]:
        self.full_deck: list[Tile] = []
        self.death_wall: list[Tile] = []
        self.draw_deck: list[Tile] = []

        # Dora relative
        self.dora: list[Tile] = []
        self.ura_dora: list[Tile] = []
        # Build tiles wall
        new_deck = self.__create_init_deck()

        # Role 2 dices (from 2 -> 12)
        dices_score = roll_dices()

        # Cut wall
        cutting_points = 34 * ((dices_score - 1) % 4 + 1) - 2 * dices_score

        if start_data and start_data["draw_deck"]:
            for tile in split_every_n_chars(start_data["draw_deck"], 2):
                tile_type, tile_number, tile_aka = parse_string_tile(tile)
                suitable_tile = find_suitable_tile_in_list(
                    tile_number, tile_type, tile_aka, new_deck
                )
                self.draw_deck.append(suitable_tile)
                new_deck.remove(suitable_tile)

        if start_data and start_data["death_wall"]:
            for tile in split_every_n_chars(start_data["death_wall"], 2):
                tile_type, tile_number, tile_aka = parse_string_tile(tile)
                suitable_tile = find_suitable_tile_in_list(
                    tile_number, tile_type, tile_aka, new_deck
                )
                self.death_wall.append(suitable_tile)
                new_deck.remove(suitable_tile)

        if len(self.draw_deck) > 0 and len(self.death_wall) > 0:
            for tile in self.draw_deck + self.death_wall:
                self.full_deck.append(tile)
            for tile in new_deck:
                self.full_deck.append(tile)
                self.draw_deck.insert(0, tile)

        else:
            self.full_deck = (
                new_deck[cutting_points:] + new_deck[0 : cutting_points - 1]
            )
            self.draw_deck = self.full_deck[2 * 7 :]
            self.death_wall = self.full_deck[0 : 2 * 7 - 1]

        self.dora.append(self.death_wall[5])

    def __create_init_deck(self) -> list[Tile]:
        from random import shuffle

        full_deck = []
        for i in range(4):
            dragon_tiles_deck = [Tile(TileType.DRAGON, x) for x in range(1, 4)]
            wind_tiles_deck = [Tile(TileType.WIND, x) for x in range(1, 5)]
            full_deck += dragon_tiles_deck + wind_tiles_deck
        for i in range(3):
            pin_tiles_deck = [Tile(TileType.PIN, x) for x in range(1, 10)]
            sou_tiles_deck = [Tile(TileType.SOU, x) for x in range(1, 10)]
            man_tiles_deck = [Tile(TileType.MAN, x) for x in range(1, 10)]

            full_deck += pin_tiles_deck + sou_tiles_deck + man_tiles_deck

        # Handle special case for AKA
        pin_tiles_deck = [Tile(TileType.PIN, x) for x in range(1, 10) if x != 5]
        sou_tiles_deck = [Tile(TileType.SOU, x) for x in range(1, 10) if x != 5]
        man_tiles_deck = [Tile(TileType.MAN, x) for x in range(1, 10) if x != 5]
        full_deck += (
            pin_tiles_deck
            + sou_tiles_deck
            + man_tiles_deck
            + [
                Tile(TileType.MAN, 5, True),
                Tile(TileType.PIN, 5, True),
                Tile(TileType.SOU, 5, True),
            ]
        )

        shuffle(full_deck)
        return full_deck
