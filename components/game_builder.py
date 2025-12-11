from components.entities.buttons.tile import Tile
from pygame import Surface
from utils.enums import TileType, ActionType, Direction, CallType
from components.entities.player import Player
from components.entities.deck import Deck
from utils.helper import (
    find_suitable_tile_in_list,
)
from typing import Any
import typing
from components.entities.fields.center_board_field import CenterBoardField
from utils.constants import HAND_CONFIG_OPTIONS
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_response import HandResponse
from components.entities.call import Call

if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager


class GameBuilder:
    """
    Game Builder class to initialize and manage game setup

    :ivar screen: Pygame Surface for rendering
    :ivar clock: Pygame Clock for managing time
    :ivar start_data: Optional data for starting the game
    :ivar deck: Deck object representing the game deck
    """
    def __init__(
        self, screen: Surface, clock, deck: Deck, start_data: Any | None = None
    ):
        self.screen = screen
        self.clock = clock
        self.start_data = start_data
        self.deck = deck

    def direction(self) -> list[Direction]:
        """
        Randomly determine player directions
        :return: List of Directions for players
        """
        import random

        current_direction = random.randint(0, 3)
        standard = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx] # Return list with current direction first

    def new(self, game_manager: "GameManager", keep_direction: bool = False) -> None:
        """
        Initialize a new game
        :param game_manager: GameManager instance
        :param keep_direction: Whether to keep the current round direction
        :return: None
        """
        direction, player_list, deck = self.init_game(
            game_manager.player_list, keep_direction
        )
        # Assign to game manager
        game_manager.direction = direction
        game_manager.player_list = player_list
        game_manager.deck = deck

        # Assign bot model
        self.assign_AI_agent(player_list, game_manager)

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

    def continue_game(self, game_manager: "GameManager"):
        self.deck.create_new_deck(
            random_seed=game_manager.game_history.data["seed"],
            data=game_manager.game_history.data,
        )
        direction = list(
            map(
                lambda direction_value: Direction(direction_value),
                game_manager.game_history.data["direction"],
            )
        )
        player_list: list[Player] = []

        for i in range(0, 4):
            call_list = self.deck.call_list[i]
            call_tiles_list = []
            for call in call_list:
                for called_tile in call.tiles:
                    call_tiles_list.append(called_tile)
            is_riichi = game_manager.game_history.data["is_reaches"][i]
            riichi_turn = None
            if is_riichi:
                riichi_turn = game_manager.game_history.data["reach_turn"][
                    game_manager.game_history.data["reaches"].index(i)
                ]
            new_player = Player(
                screen=self.screen,
                player_idx=i,
                direction=direction[i],
                full_deck=self.deck.full_deck,
                player_deck=self.deck.player_deck[i],
                discard_tiles=self.deck.discard_tiles[i],
                already_discard_tiles=self.deck.already_discard_tiles[i],
                call_list=self.deck.call_list[i],
                call_tiles_list=call_tiles_list,
                callable_tiles_list=self.deck.callable_tiles_list[i],
                can_call=list(
                    map(
                        lambda call_value: CallType(call_value),
                        game_manager.game_history.data["can_call"][i],
                    )
                ),
                is_riichi=is_riichi,
                riichi_turn=riichi_turn,
                draw_tile=self.deck.latest_draw_tile[i],
                points=game_manager.game_history.data["points"][i],
            )
            for tile in new_player.call_tiles_list:
                tile.update_tile_surface(i)
                tile.reveal()
            for tile in new_player.player_deck:
                tile.update_tile_surface(i)
            for tile in new_player.discard_tiles:
                tile.update_tile_surface(i)
                tile.reveal()

            new_player.points = game_manager.game_history.data["points"][i]
            player_list.append(new_player)

        # Assign to game manager
        game_manager.direction = direction
        game_manager.player_list = player_list
        game_manager.deck = self.deck

        # Assign bot model
        self.assign_AI_agent(player_list, game_manager)

        game_manager.latest_discarded_tile = self.deck.latest_discard_tile
        # Assign Turn and player to game manager
        game_manager.current_turn = Direction(
            game_manager.game_history.data["current_direction"]
        )
        game_manager.current_player = game_manager.find_player(
            game_manager.current_turn
        )
        game_manager.main_player = player_list[0]
        game_manager.round_direction = Direction(
            game_manager.game_history.data["round_direction"]
        )
        game_manager.round_direction_number = game_manager.game_history.data[
            "round_direction_number"
        ]
        game_manager.switch_turn(game_manager.current_turn, False)

        game_manager.tsumi_number = game_manager.game_history.data["tsumi_number"]
        game_manager.kyoutaku_number = game_manager.game_history.data["kyoutaku_number"]
        if game_manager.game_history.data.get("action") is not None:
            game_manager.action = ActionType(game_manager.game_history.data["action"])
        if game_manager.game_history.data.get("prev_action") is not None:
            game_manager.prev_action = ActionType(
                game_manager.game_history.data["prev_action"]
            )
        if game_manager.game_history.data.get("prev_called_player") is not None:
            game_manager.prev_called_player = player_list[
                game_manager.game_history.data["prev_called_player"]
            ]

        if game_manager.game_history.data.get("prev_player") is not None:
            game_manager.prev_player = player_list[
                game_manager.game_history.data["prev_player"]
            ]

        if game_manager.game_history.data.get("calling_player") is not None:
            game_manager.calling_player = player_list[
                game_manager.game_history.data["calling_player"]
            ]

        if game_manager.game_history.data.get("call_order"):
            game_manager.call_order = list(
                map(
                    lambda player_idx: player_list[player_idx],
                    game_manager.game_history.data["call_order"],
                )
            )

        # Center board field related
        game_manager.center_board_field = CenterBoardField(
            self.screen,
            (
                game_manager.round_direction,
                game_manager.round_direction_number,
            ),
            direction,
            self.deck,
            player_list,
            game_manager.tsumi_number,
            game_manager.kyoutaku_number,
        )

    def assign_round_direction(
        self, game_manager: "GameManager", keep_direction: bool = False
    ) -> None:
        """
        Assign or update the round direction in the game manager.
        :param game_manager: GameManager instance
        :param keep_direction: Whether to keep the current round direction
        :return: None
        """
        if not game_manager.round_direction:
            game_manager.round_direction = Direction(0)
            game_manager.round_direction_number = 1
            return
        if keep_direction:
            return
        if game_manager.round_direction_number == 4:
            game_manager.round_direction = Direction(
                (game_manager.round_direction.value + 1) % 4
            )
            game_manager.round_direction_number = 1
        else:
            game_manager.round_direction_number += 1

    def init_game(self, players: list[Player] = None, keep_direction: bool = False):
        self.deck.clear_seed()
        self.deck.create_new_deck(start_data=self.start_data)

        # Create player
        if not players:
            # Choose direction for player
            if self.start_data and self.start_data["direction"]: # Custom direction
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
            else: # Random direction
                direction = self.direction()
            print(f"Current player direction is {direction[0]}")
            player_list: list[Player] = []
            for i in range(4):
                player_list.append(
                    Player(self.screen, i, direction[i], self.deck.full_deck)
                )
        else: # Recurring game
            player_list = players
            direction: list[Direction] = []
            for i in range(4):
                player_list[i].renew_deck()
                if not keep_direction: # Rotate direction counter-clockwise
                    player_list[i].direction = Direction(
                        (player_list[i].direction.value - 1) % 4
                    )
                    direction.append(player_list[i].direction)
                    player_list[i].full_deck = self.deck.full_deck
                else:
                    direction.append(player_list[i].direction)

        if self.start_data and self.start_data["player_deck"]: # Custom player deck
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

        else: # Standard player deck
            for i in range(4):
                for k in range(4): # Draw 4 tiles for each player
                    player_idx = direction.index(Direction(k))
                    player = player_list[player_idx]
                    if i == 3: # Last loop, draw only 1 tile
                        player.draw(self.deck.draw_deck, None, check_call=False)
                    else:
                        for j in range(4):
                            player.draw(self.deck.draw_deck, None, check_call=False)

        # Rearrange deck for each player
        for player in player_list:
            player.rearrange_deck()
            player.deck_field.build_field_surface(player)
            player.deck_field.build_tiles_position(player)

        player_list[0].reveal_hand()

        return direction, player_list, self.deck

    @staticmethod
    def custom_deck(
        man: str | None,
        sou: str | None,
        pin: str | None,
        honors: str | None,
        player: Player,
        draw_deck: list[Tile],
    ) -> None:
        """
        Create a custom deck for a player based on provided tile strings.
        """
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

    @staticmethod
    def calculate_player_score(
        player: Player = None,
        round_wind: Direction = None,
        win_tile: Tile = None,
        deck: Deck = None,
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
        is_nagashi_mangan: bool = False,
        tsumi_number: int = 0,
        kyoutaku_number: int = 0,
        ura_dora: list[Tile] = [],
    ) -> HandResponse:
        """
        Calculate the player's score based on the current hand and game state.
        :return: HandResponse object containing the result of the hand calculation
        """

        # Init hand config for calculator
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
            player_wind=player.direction.value + 27 if player else None,
            tsumi_number=tsumi_number,
            kyoutaku_number=kyoutaku_number,
            is_nagashi_mangan=is_nagashi_mangan,
            round_wind=round_wind.value + 27 if round_wind else None,
            options=HAND_CONFIG_OPTIONS,
        )

        calculator = HandCalculator()

        if is_nagashi_mangan: # Handle nagashi mangan case
            result = calculator.estimate_hand_value(
                tiles=[], win_tile=None, config=config
            )
        else:
            copy_player_deck = player.player_deck.copy()

            if win_tile not in copy_player_deck:
                copy_player_deck.append(win_tile)

            hands = copy_player_deck + player.call_tiles_list # Add melds to hand for calculation

            copy_dora_list = deck.dora.copy()
            if len(ura_dora) > 0:
                copy_dora_list += ura_dora
            result = calculator.estimate_hand_value(
                list(map(lambda tile: tile.hand136_idx, hands)),
                win_tile.hand136_idx,
                player.melds,
                list(map(lambda tile: tile.hand136_idx, copy_dora_list)),
                config=config,
            )

        if result:
            print(result, result.yaku, result.cost)
            print(
                f"FINAL RESULT: {result} {result.yaku} and player scores: {result.cost['total']}"
            )
        return result

    @staticmethod
    def assign_AI_agent(player_list: list[Player], game_manager: "GameManager") -> None:
        """
        Assign AI agents to players based on game manager settings.
        :param player_list: List of Player objects
        :param game_manager: GameManager instance
        :return: None
        """
        for player in player_list:
            player.game_manager = game_manager

            if player.player_idx == 0:
                continue

            if getattr(game_manager, f"bot_{player.player_idx}_model") == "shanten":
                player.agent = None
                print(f"Assigning bot {player.player_idx} with no agent")
            elif (
                getattr(game_manager, f"bot_{player.player_idx}_model") == "aggressive"
            ):
                player.agent = game_manager.ai_agent_MID
                print(f"Assigning bot {player.player_idx} with agent MID")
            elif getattr(game_manager, f"bot_{player.player_idx}_model") == "passive":
                player.agent = game_manager.ai_agent_SMART
                print(f"Assigning bot {player.player_idx} with agent SMART")