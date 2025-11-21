from components.buttons.tile import Tile
from utils.enums import TileType
from utils.helper import roll_dices


class Deck:
    # Main
    full_deck: list[Tile] = []
    death_wall: list[Tile] = []
    draw_deck: list[Tile] = []

    # Dora relative
    dora: list[Tile] = []
    ura_dora: list[Tile] = []

    def __init__(self):
        self.create_new_deck()

    def create_new_deck(self) -> dict[str, list[Tile]]:
        # Build tiles wall
        new_deck = self.__create_init_deck()

        # Role 2 dices (from 2 -> 12)
        dices_score = roll_dices()

        # Cut wall
        cutting_points = 34 * ((dices_score - 1) % 4 + 1) - 2 * dices_score
        self.full_deck = new_deck[cutting_points:] + new_deck[0 : cutting_points - 1]
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
