from utils.enums import Direction
from components.image_cutter import ImageCutter
from utils.constants import TILES_IMAGE_LINK
from components.buttons.tile import Tile
from pygame import Surface
from utils.enums import TileType
from components.player import Player
from pygame import Rect
from components.deck import Deck
import sys
from utils.helper import find_suitable_tile_in_list
from typing import Any
import typing
from components.fields.center_board_field import CenterBoardField

if typing.TYPE_CHECKING:
    from components.game_manager import GameManager


class GameBuilder:
    def __init__(self, screen: Surface, clock, start_data: Any | None = None):
        self.screen = screen
        self.clock = clock
        self.start_data = start_data

    def direction(self) -> list[Direction]:
        import random

        current_direction = random.randint(0, 3)
        standard = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx]
        # return standard

    def new(self, game_manager: "GameManager"):
        direction, player_list, deck = self.init_game()

        # Assign to game manager
        game_manager.direction = direction
        game_manager.player_list = player_list
        game_manager.deck = deck

        # Assign Turn and player to game manager
        start_turn = Direction(0)
        game_manager.current_turn = start_turn
        game_manager.current_player = game_manager.find_player(
            game_manager.current_turn
        )
        game_manager.main_player = player_list[0]
        game_manager.switch_turn(game_manager.current_turn)

        # Center board field related
        game_manager.center_board_field = CenterBoardField(
            self.screen, direction, player_list
        )

    def init_game(self):
        # Choose direction for player
        if self.start_data and self.start_data["direction"]:
            direction: list[Direction] = []
            for direction_char in list(self.start_data["direction"]):
                match direction_char:
                    case "S":
                        direction.append(Direction.SOUTH)
                    case "W":
                        direction.append(Direction.WEST)
                    case "E":
                        direction.append(Direction.EAST)
                    case "N":
                        direction.append(Direction.NORTH)
        else:
            direction = self.direction()
        print(f"Current player direction is {direction[0]}")

        deck = Deck(self.start_data)

        # Create player
        player_list: list[Player] = []
        for i in range(4):
            player_list.append(Player(self.screen, i, direction[i], deck.full_deck))

        if self.start_data and self.start_data["player_deck"]:
            if (
                len(self.start_data["player_deck"]) < 4
                and len(self.start_data["player_deck"]) != 0
            ):
                raise ValueError(
                    f"Not enough custom deck player to init game! Please try again... Current numbers of players are {len(self.start_data["player_deck"])}"
                )
            for player_idx, player_deck in enumerate(self.start_data["player_deck"]):
                # Draw tiles (13 tiles, main draws 14 tiles)
                current_type = None
                honors = ""
                mans = ""
                sous = ""
                pins = ""
                for idx in range(len(player_deck) - 1, -1, -1):
                    tile_str = player_deck[idx]
                    match tile_str:
                        case "z":
                            current_type = "honors"
                        case "m":
                            current_type = "man"
                        case "p":
                            current_type = "pin"
                        case "s":
                            current_type = "sou"
                        case _:
                            match current_type:
                                case "honors":
                                    honors += tile_str
                                case "man":
                                    mans += tile_str
                                case "pin":
                                    pins += tile_str
                                case "sou":
                                    sous += tile_str
                try:
                    self.custom_deck(
                        man=mans,
                        sou=sous,
                        pin=pins,
                        honors=honors,
                        player=player_list[player_idx],
                        draw_deck=deck.draw_deck,
                    )
                except IndexError as e:
                    print("Error when creating custom deck! Regenerating deck...")
                    return self.init_game()

        else:
            for i in range(4):
                for k in range(4):
                    player_idx = direction.index(Direction(k))
                    player = player_list[player_idx]
                    if i == 3:
                        player.draw(deck.draw_deck, check_call=False)
                    else:
                        for j in range(4):
                            player.draw(deck.draw_deck, check_call=False)

        # Rearrange deck for each player
        for player in player_list:
            player.rearrange_deck()
            player.deck_field.build_field_surface(player)
            player.deck_field.build_tiles_position(player)

        main_player = player_list[direction.index(Direction(0))]
        main_player.deck_field.build_tiles_position(main_player)
        player_list[0].reveal_hand()

        return (direction, player_list, deck)

    def custom_deck(
        self,
        man: str | None,
        sou: str | None,
        pin: str | None,
        honors: str | None,
        player: Player,
        draw_deck: list[Tile],
    ) -> list[int]:
        tiles_list: list[dict] = []

        if man:
            for tile in list(man):
                if tile == "r":
                    tiles_list.append({"number": 5, "type": TileType.MAN, "aka": True})
                else:
                    tiles_list.append(
                        {"number": int(tile), "type": TileType.MAN, "aka": False}
                    )
        if sou:
            for tile in list(sou):
                if tile == "r":
                    tiles_list.append({"number": 5, "type": TileType.SOU, "aka": True})
                else:
                    tiles_list.append(
                        {"number": int(tile), "type": TileType.SOU, "aka": False}
                    )

        if pin:
            for tile in list(pin):
                if tile == "r":
                    tiles_list.append({"number": 5, "type": TileType.PIN, "aka": True})
                else:
                    tiles_list.append(
                        {"number": int(tile), "type": TileType.PIN, "aka": False}
                    )

        if honors:
            for tile in list(honors):
                if int(tile) >= 5:
                    tiles_list.append(
                        {"number": int(tile) - 4, "type": TileType.DRAGON, "aka": False}
                    )
                else:
                    tiles_list.append(
                        {
                            "number": int(tile),
                            "type": TileType.WIND,
                            "aka": False,
                        }
                    )

        for tile in tiles_list:
            found_tile = find_suitable_tile_in_list(
                tile["number"], tile["type"], tile["aka"], draw_deck
            )
            if found_tile:
                player.draw(draw_deck, found_tile, False)

        if len(player.player_deck) < 13:
            raise ValueError(
                f"Init deck invalid because the tiles from starter deck are lower than 13! Player {player.player_idx} have {len(player.player_deck)}"
            )

    def calculate_player_score(self, player: Player, deck: Deck) -> int:
        return
