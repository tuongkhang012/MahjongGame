from components.entities.buttons.tile import Tile
from components.game_event_log import GameEventLog
from utils.enums import TileType
from utils.enums import ActionType
from utils.helper import (
    roll_dices,
    get_data_from_file,
    parse_string_tile,
    split_every_n_chars,
    find_suitable_tile_in_list,
    convert_tiles_list_to_hand34,
)
from shared.random_seed import generate_random_seed
import sys
from typing import Any


class Deck:
    # Init all tile in deck
    __init_deck: list[Tile] = []

    # Game log for dora
    game_log: GameEventLog

    # Main
    full_deck: list[Tile] = []
    death_wall: list[Tile] = []
    draw_deck: list[Tile] = []

    # Dora relative
    current_dora_idx: int = 5
    dora: list[Tile] = []
    ura_dora: list[Tile] = []

    random_seed: str

    def __init__(self, game_log: GameEventLog):
        self.__init_deck = self.__init_full_deck()
        self.game_log = game_log

    def create_new_deck(self, start_data: Any | None = None) -> dict[str, list[Tile]]:
        # Create a random seed
        self.random_seed = generate_random_seed()

        self.death_wall: list[Tile] = []
        self.draw_deck: list[Tile] = []

        # Dora relative
        self.dora: list[Tile] = []
        self.ura_dora: list[Tile] = []
        # Build tiles wall
        new_deck = self.__create_init_deck()

        # Role 2 dices (from 2 -> 12)
        dices_score = sum(self.dices)

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
                suitable_tile.from_death_wall = True
                self.death_wall.append(suitable_tile)
                new_deck.remove(suitable_tile)

        if len(self.draw_deck) > 0 and len(self.death_wall) > 0:
            for tile in self.draw_deck + self.death_wall:
                self.full_deck.append(tile)
            for tile in new_deck:
                self.full_deck.append(tile)
                self.draw_deck.insert(0, tile)

        else:
            self.full_deck = new_deck[cutting_points:] + new_deck[0:cutting_points]
            self.draw_deck = self.full_deck[2 * 7 :]
            self.death_wall = self.full_deck[0 : 2 * 7]
            for tile in self.death_wall:
                tile.from_death_wall = True

        if not all(
            [
                tile_count == 4
                for tile_count in convert_tiles_list_to_hand34(self.full_deck)
            ]
        ) and len(convert_tiles_list_to_hand34(self.full_deck) == 34):
            raise ValueError("Some tiles are missing!")

    def add_new_dora(self):
        self.dora.append(self.death_wall[self.current_dora_idx])
        self.game_log.append_event(
            ActionType.DORA, self.death_wall[self.current_dora_idx]
        )
        self.current_dora_idx += 2

    def __init_full_deck(self) -> list[Tile]:
        import math

        full_deck: list[Tile] = []

        for i in range(136):
            hand34_idx = math.floor(i / 4)
            tile_number = None
            tile_type = None
            is_aka = False
            tile_name = ""
            if hand34_idx <= 8:
                tile_number = (hand34_idx % 9) + 1
                tile_type = TileType.MAN
                tile_name = f"{tile_number}m"
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name += "r"
            elif hand34_idx <= 17:
                tile_number = (hand34_idx % 9) + 1
                tile_type = TileType.PIN
                tile_name = f"{tile_number}p"
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name += "r"

            elif hand34_idx <= 26:
                tile_number = (hand34_idx % 9) + 1
                tile_type = TileType.SOU
                tile_name = f"{tile_number}s"
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name += "r"
            elif hand34_idx <= 30:
                tile_number = ((hand34_idx + 1) % 7) + 1
                tile_type = TileType.WIND
                tile_name = f"{tile_number}z"
            elif hand34_idx <= 33:
                tile_number = ((hand34_idx + 1) % 7) - 3
                tile_type = TileType.DRAGON
                tile_name = f"{tile_number + 4}z"

            new_tile = Tile(i, tile_type, tile_number, tile_name, is_aka)
            full_deck.append(new_tile)

        return full_deck

    def get_init_deck(self) -> list[Tile]:
        return self.__init_deck

    def __create_init_deck(self) -> list[Tile]:
        from shared.reproduce_tenhou import reproduce_tenhou

        full_deck = []

        result = reproduce_tenhou(self.random_seed, 1)
        tenhou = result[0][0]
        self.dices = result[0][1]

        for i in tenhou:
            tile = list(filter(lambda tile: tile.hand136_idx == i, self.__init_deck))[0]
            full_deck.append(tile)

        return full_deck
