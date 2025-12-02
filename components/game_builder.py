from components.entities.buttons.tile import Tile
from pygame import Surface
from utils.enums import TileType, ActionType, Direction
from components.entities.player import Player
from components.entities.deck import Deck
from utils.helper import find_suitable_tile_in_list
from typing import Any
import typing
from components.entities.fields.center_board_field import CenterBoardField
from utils.constants import HAND_CONFIG_OPTIONS
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_response import HandResponse

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


class GameBuilder:
    def __init__(
        self, screen: Surface, clock, deck: Deck, start_data: Any | None = None
    ):
        self.screen = screen
        self.clock = clock
        self.start_data = start_data
        self.deck = deck

    def direction(self) -> list[Direction]:
        import random

        current_direction = random.randint(0, 3)
        standard = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx]
        # return standard

    def new(self, game_manager: "GameManager", keep_direction: bool = False):
        direction, player_list, deck = self.init_game(
            game_manager.player_list, keep_direction
        )
        # Assign to game manager
        game_manager.direction = direction
        game_manager.player_list = player_list
        game_manager.deck = deck

        for player in player_list:
            player.game_manager = game_manager

            if (
                hasattr(game_manager, "ai_seat_idx")
                and player.player_idx in game_manager.ai_seat_idx
            ):
                print(f"Assigning AI agent to player {player.player_idx}")
                if player.player_idx == 1:
                    player.agent = game_manager.ai_agent_MID
                else:
                    player.agent = game_manager.ai_agent_SMART
            else:
                player.agent = None

        # Assign Turn and player to game manager
        start_turn = Direction(0)
        game_manager.current_turn = start_turn
        game_manager.current_player = game_manager.find_player(
            game_manager.current_turn
        )
        game_manager.main_player = player_list[0]
        game_manager.switch_turn(game_manager.current_turn)

        self.assign_round_direction(game_manager, keep_direction)

        # Center board field related
        game_manager.center_board_field = CenterBoardField(
            self.screen,
            (game_manager.round_direction, game_manager.round_direction_number),
            direction,
            deck,
            player_list,
            game_manager.tsumi_number,
            game_manager.kyoutaku_number,
        )

    def assign_round_direction(
        self, game_manager: "GameManager", keep_direction: bool = False
    ):
        if not game_manager.round_direction:
            game_manager.round_direction = Direction(0)
            game_manager.round_direction_number = 1
            return
        if keep_direction:
            return
        if game_manager.round_direction_number == 4:
            game_manager.round_direction = Direction(
                (game_manager.round_direction.value - 1) % 4
            )
            game_manager.round_direction_number = 1
        else:
            game_manager.round_direction_number += 1

    def init_game(self, players: list[Player] = None, keep_direction: bool = False):
        self.deck.create_new_deck(self.start_data)

        # Create player
        if not players:
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
            player_list: list[Player] = []
            for i in range(4):
                player_list.append(
                    Player(self.screen, i, direction[i], self.deck.full_deck)
                )
        else:
            player_list = players
            direction: list[Direction] = []
            for i in range(4):
                player_list[i].renew_deck()
                if not keep_direction:
                    player_list[i].direction = Direction(
                        (player_list[i].direction.value - 1) % 4
                    )
                    direction.append(player_list[i].direction)
                    player_list[i].full_deck = self.deck.full_deck
                else:
                    direction.append(player_list[i].direction)

        if self.start_data and self.start_data["player_deck"]:
            if (
                len(self.start_data["player_deck"]) < 4
                and len(self.start_data["player_deck"]) != 0
            ):
                raise ValueError(
                    f"Not enough custom deck player to init game! Please try again... Current numbers of players are {len(self.start_data['player_deck'])}"
                )
            for player_idx, player_deck in enumerate(self.start_data["player_deck"]):
                # Draw tiles (13 tiles)
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
                        draw_deck=self.deck.draw_deck,
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
                        player.draw(self.deck.draw_deck, None, check_call=False)
                    else:
                        for j in range(4):
                            player.draw(self.deck.draw_deck, None, check_call=False)

        # Rearrange deck for each player
        for player in player_list:
            player.rearrange_deck()
            player.deck_field.build_field_surface(player)
            player.deck_field.build_tiles_position(player)

        main_player = player_list[direction.index(Direction(0))]
        main_player.deck_field.build_tiles_position(main_player)
        player_list[0].reveal_hand()

        return (direction, player_list, self.deck)

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
                player.draw(
                    draw_deck, round_wind=None, tile=found_tile, check_call=False
                )

        if len(player.player_deck) < 13:
            raise ValueError(
                f"Init deck invalid because the tiles from starter deck are lower than 13! Player {player.player_idx} have {len(player.player_deck)}"
            )

    def calculate_player_score(
        self,
        player: Player,
        round_wind: Direction,
        win_tile: Tile,
        deck: Deck,
        is_tsumo: bool = False,
        is_riichi: bool = False,
        is_daburu_riichi: bool = False,
        is_ippatsu: bool = False,
        is_rinshan: bool = False,
        is_chankan: bool = False,
        is_haitei: bool = False,
        is_houtei: bool = False,
        is_tenhou: bool = False,
        is_chiihou: bool = False,
        is_renhou: bool = False,
        tsumi_number: int = 0,
        kyoutaku_number: int = 0,
    ) -> HandResponse:

        # is_rinshan, include in parameters
        # is_chankan, include in parameters

        # is_haitei
        config = HandConfig(
            is_tsumo=is_tsumo,
            is_riichi=is_riichi,
            is_ippatsu=is_ippatsu,
            is_rinshan=is_rinshan,
            is_chankan=is_chankan,
            is_haitei=is_haitei,
            is_houtei=is_houtei,
            is_tenhou=is_tenhou,
            is_chiihou=is_chiihou,
            is_renhou=is_renhou,
            is_daburu_riichi=is_daburu_riichi,
            player_wind=player.direction.value + 27,
            tsumi_number=tsumi_number,
            kyoutaku_number=kyoutaku_number,
            round_wind=round_wind.value + 27,
            options=HAND_CONFIG_OPTIONS,
        )

        calculator = HandCalculator()
        copy_player_deck = player.player_deck.copy()

        if win_tile not in copy_player_deck:
            copy_player_deck.append(win_tile)

        hands = copy_player_deck + player.call_tiles_list
        result = calculator.estimate_hand_value(
            list(map(lambda tile: tile.hand136_idx, hands)),
            win_tile.hand136_idx,
            player.melds,
            list(map(lambda tile: tile.hand136_idx, deck.dora)),
            config=config,
        )
        print(
            f"FINAL RESULT: {result} {result.yaku} and player scores: {result.cost['total']}"
        )
        return result
