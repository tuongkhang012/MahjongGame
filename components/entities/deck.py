from components.entities.buttons.tile import Tile
from components.game_event_log import GameEventLog
from utils.enums import TileType, TileSource, CallType
from utils.game_history_data_dict import GameHistoryData
from components.entities.call import Call
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
    current_dora_idx: int
    dora: list[Tile] = []
    ura_dora: list[Tile] = []

    player_deck: list[list[Tile]] = []
    discard_tiles: list[list[Tile]] = []
    already_discard_tiles: list[list[Tile]] = []
    call_list: list[list[Call]] = []
    callable_tiles_list: list[list[list[Tile]]] = []
    latest_draw_tile: list[Tile] = []
    latest_discard_tile: Tile = None

    random_seed: str

    def __init__(self, seed: str = None):
        self.__init_deck = self.__init_full_deck()
        self.__init_seed = seed

    def create_new_deck(
        self,
        random_seed: str = None,
        data: GameHistoryData = None,
        start_data: Any | None = None,
    ) -> dict[str, list[Tile]]:
        # Create a random seed
        if random_seed:
            self.__init_seed = random_seed

        if self.__init_seed:
            self.random_seed = self.__init_seed
            self.__init_seed = None
        else:
            self.random_seed = generate_random_seed()
        self.current_dora_idx = 5
        self.death_wall: list[Tile] = []
        self.draw_deck: list[Tile] = []
        self.full_deck = []
        # Dora relative
        self.dora: list[Tile] = []
        self.ura_dora: list[Tile] = []
        # Build tiles wall
        new_deck = self.__create_init_deck()

        # Role 2 dices (from 2 -> 12)
        dices_score = sum(self.dices)

        # Cut wall
        if data:
            for tile in data["full_deck"]:
                for tmp_tile in new_deck:
                    if tmp_tile.hand136_idx == tile["hand136_idx"]:
                        self.full_deck.append(tmp_tile)
                        break

            for tile in data["death_wall"]:
                for tmp_tile in new_deck:
                    if tmp_tile.hand136_idx == tile["hand136_idx"]:
                        self.death_wall.append(tmp_tile)
                        break

            for tile in data["dora"]:
                for tmp_tile in new_deck:
                    if tmp_tile.hand136_idx == tile["hand136_idx"]:
                        self.dora.append(tmp_tile)
                        break

            for tile in data["draw_deck"]:
                for tmp_tile in new_deck:
                    if tmp_tile.hand136_idx == tile["hand136_idx"]:
                        self.draw_deck.append(tmp_tile)
                        break

            for hands in data["hands"]:
                init_hand = []

                for tile_data in hands:
                    for tmp_tile in new_deck:
                        if tmp_tile.hand136_idx == tile_data["hand136_idx"]:
                            if tile_data["from_death_wall"]:
                                tmp_tile.from_death_wall = True
                            init_hand.append(tmp_tile)
                            break

                self.player_deck.append(init_hand)

            for discards in data["already_discards"]:
                init_discard = []

                for tile_data in discards:
                    for tmp_tile in new_deck:
                        if tmp_tile.hand136_idx == tile_data["hand136_idx"]:
                            if tile_data["from_death_wall"]:
                                tmp_tile.from_death_wall = True
                            if tile_data["riichi_discard"]:
                                tmp_tile.discard_riichi()
                            init_discard.append(tmp_tile)
                            break

                self.already_discard_tiles.append(init_discard)

            for discards in data["discards"]:
                init_discard = []

                for tile_data in discards:
                    for tmp_tile in new_deck:
                        if tmp_tile.hand136_idx == tile_data["hand136_idx"]:
                            if tile_data["from_death_wall"]:
                                tmp_tile.from_death_wall = True
                            if tile_data["riichi_discard"]:
                                tmp_tile.discard_riichi()
                            init_discard.append(tmp_tile)
                            break

                self.discard_tiles.append(init_discard)

            for melds in data["melds"]:
                init_melds = []
                for meld_data in melds:
                    call_tiles: list[Tile] = []
                    print(meld_data)
                    for idx, tile_data in enumerate(meld_data["tiles"]):
                        suitable_tile = None
                        for each_tile in self.full_deck:
                            if each_tile.hand136_idx == tile_data["hand136_idx"]:
                                suitable_tile = each_tile
                                break

                        if tile_data["from_death_wall"]:
                            suitable_tile.from_death_wall = True
                        if (
                            meld_data["called_tile"] is not None
                            and idx == meld_data["called_tile"]
                        ):
                            suitable_tile.source = TileSource.PLAYER
                            print("I AM IN HEREEEEE")
                        call_tiles.append(suitable_tile)

                    new_call = Call(
                        CallType(meld_data["type"]),
                        call_tiles,
                        meld_data["who"],
                        meld_data["from_who"],
                        meld_data["kakan"],
                    )

                    init_melds.append(new_call)
                self.call_list.append(init_melds)

            for hand136_idx in data["latest_draw_tile_hand136_idx"]:
                for tile in self.full_deck:
                    if tile.hand136_idx == hand136_idx:
                        self.latest_draw_tile.append(tile)
                        break

            for tiles_list in data["callable_tiles_list"]:
                callable_list: list[list[Tile]] = []
                for call_list_hand136_idx in tiles_list:
                    tmp_list: list[Tile] = []
                    for tile_hand136_idx in call_list_hand136_idx:
                        if tile.hand136_idx == tile_hand136_idx:
                            tmp_list.append(tile)
                            break
                    callable_list.append(tmp_list)
                self.callable_tiles_list.append(callable_list)
            return
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
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name = f"rm"
                else:
                    tile_name = f"{tile_number}m"

            elif hand34_idx <= 17:
                tile_number = (hand34_idx % 9) + 1
                tile_type = TileType.PIN
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name = f"rp"
                else:
                    tile_name = f"{tile_number}p"

            elif hand34_idx <= 26:
                tile_number = (hand34_idx % 9) + 1
                tile_type = TileType.SOU
                if tile_number == 5 and i % 4 == 0:
                    is_aka = True
                    tile_name = f"rs"
                else:
                    tile_name = f"{tile_number}s"
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
            tile.undisabled()
            tile.undiscard_riichi()
            if len(sys.argv) > 1 and "debug" in sys.argv:
                tile.hidden = False
            else:
                tile.hidden = True
            full_deck.append(tile)

        return full_deck
