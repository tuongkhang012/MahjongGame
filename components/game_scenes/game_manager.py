import pygame
from utils.constants import (
    WINDOW_SIZE,
    FPS_LIMIT,
    GAME_TITLE,
    TILE_ANIMATION_DURATION,
    TILE_POPUP_DURATION,
    TILE_SCALE_BY,
)
from components.game_builder import GameBuilder
from utils.enums import Direction, ActionType, CallType, GameScene
from components.events.mouse_button_down import MouseButtonDown
from components.events.mouse_motion import MouseMotion

from pygame import Surface
from components.entities.player import Player
from components.entities.deck import Deck
from utils.helper import build_center_rect, map_action_to_call
from components.entities.fields.center_board_field import CenterBoardField
from components.entities.fields.discard_field import DiscardField
import typing
import random
from components.game_event_log import GameEventLog, GameEvent, GameRoundLog

# Tile
from components.entities.buttons.tile import Tile
from components.entities.fields.call_button_fields import CallButtonField

if typing.TYPE_CHECKING:
    from components.game_scenes.scenes_controller import ScenesController


class GameManager:
    screen: Surface
    scenes_controller: "ScenesController"

    # Player
    player_list: list[Player] = []
    current_player: Player
    prev_player: Player
    main_player: Player
    direction: list[Direction]

    # Deck
    deck: Deck

    # Field
    center_board_field: CenterBoardField

    # Turn
    current_turn: Direction

    # Round direction
    round_direction: Direction = None
    round_direction_number: int = None

    # AI relevant
    bot_move_timer: float = 0
    BOT_MOVE_DELAY: float = 1  # AI "thinks" for 1 seconds

    # Animation related
    animation_tile: Tile | None = None

    # Game logic relavent
    latest_discarded_tile: Tile | None = None
    latest_called_tile: Tile | None = None
    call_order: list[Player] = []
    calling_player: Player = None
    prev_called_player: Player = None
    action: ActionType = None
    prev_action: ActionType = None

    # Score relavent
    tsumi_number: int = 0
    kyoutaku_number: int = 0

    def __init__(
        self, screen: Surface, scenes_controller: "ScenesController", start_data=None
    ):
        pygame.init()
        # pygame.mixer.init()
        # pygame.freetype.init()

        pygame.display.set_caption(GAME_TITLE)

        # Display setting
        self.main_screen = screen
        self.screen = screen.copy()
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60
        self.last_time = pygame.time.get_ticks()  # For calculating delta time

        # Game log
        self.game_log = GameEventLog()

        # Init deck
        init_deck = Deck(self.game_log)
        self.builder = GameBuilder(self.screen, self.clock, init_deck, start_data)

        # Init game
        self.builder.new(self)
        self.__create_new_round_log()
        self.deck.add_new_dora()

        # Create class event listener
        self.mouse_button_down = MouseButtonDown(
            self.screen, self, init_deck.get_init_deck()
        )
        self.mouse_motion = MouseMotion(self.screen, self, init_deck.get_init_deck())
        self.call_button_field = CallButtonField(self.screen)

        self.scenes_controller = scenes_controller

    def render(self) -> Surface:
        # --- Calculate Delta Time ---
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0  # Time in seconds
        self.last_time = current_time

        # --- Update logic game ---
        self.update(delta_time)

        # --- Rendering ---
        self.screen.fill("aquamarine4")
        self.center_board_field.render(self.current_turn)
        for player in self.player_list:
            player.deck_field.render(player)

            if player == self.main_player:
                if self.calling_player and self.main_player == self.calling_player:
                    self.call_button_field.render(self.main_player.can_call)
                player.reveal_hand()

            if len(player.call_list) > 0:
                player.call_field.render(self.screen)

        if self.animation_tile:
            self.render_discarded_animation(self.animation_tile)

        self.main_screen.blit(self.screen, (0, 0))
        return self.main_screen

    def render_discarded_animation(self, tile: Tile):
        if not self.animation_tile:
            return

        # Calculate animation progress (0.0 to 1.0)
        progress = self.animation_timer / TILE_ANIMATION_DURATION

        # Zoom from 1x scale up to 3x scale
        scale = 1.0 + progress if 1.0 + progress < TILE_SCALE_BY else TILE_SCALE_BY

        base_image = tile.tiles_cutter.cut_tiles(tile.type, tile.number, tile.aka)

        # Apply scale and alpha
        scaled_image = pygame.transform.rotozoom(base_image, 0, scale)

        # Get position to center it on the screen
        pos = build_center_rect(self.screen, scaled_image)

        # Draw the animating tile
        self.screen.blit(scaled_image, pos)

    def start_discarded_animation(self, tile: Tile):
        if self.animation_tile:
            return

        # Start the animation
        self.animation_tile = tile
        self.animation_timer = 0.0
        self.current_discard_player_direction = self.current_turn

    def finish_discarded_animation(self):
        if not self.animation_tile or self.current_discard_player_direction is None:
            return

        # Reset animation state
        self.animation_tile = None
        self.animation_timer = 0.0
        self.current_discard_player_direction = None

        self.last_time = pygame.time.get_ticks()

    def update(self, delta_time: float):
        # --- Handle animation FIRST ---
        if self.animation_tile:
            self.animation_timer += delta_time

            # Check if animation is finished
            if (
                self.animation_timer >= TILE_ANIMATION_DURATION
                and self.animation_timer >= TILE_POPUP_DURATION
            ):
                self.finish_discarded_animation()

            # While animating, do nothing else (no AI moves, no input)
            return

        if len(self.call_order) > 0 or self.calling_player is not None:
            if self.calling_player is None:
                self.calling_player = self.call_order.pop()
            if self.calling_player == self.main_player:
                if self.action:
                    self.do_action()
                return
            else:
                # --- THIS IS BOT TURN ---
                # Add to the "thinking" timer
                self.bot_move_timer += delta_time
                # Wait until the "thinking" time (BOT_MOVE_DELAY) has passed
                if self.bot_move_timer < self.BOT_MOVE_DELAY:
                    return  # Not time to move yet
                self.action = self.calling_player.make_move()
                print("--- START CHII PON KAN RON ---")

        if self.current_player == self.main_player:
            if self.action:
                self.do_action()
            return

        if self.action is None:
            # --- THIS IS BOT TURN ---
            # Add to the "thinking" timer
            self.bot_move_timer += delta_time

            # Wait until the "thinking" time (BOT_MOVE_DELAY) has passed
            if self.bot_move_timer < self.BOT_MOVE_DELAY:
                return  # Not time to move yet

            # --- BOT action ---
            current_bot = self.current_player
            self.action = current_bot.make_move()

        if self.action:
            self.do_action()

    def switch_turn(self, turn: Direction = None, draw: bool = True):
        self.call_order = []

        if turn:
            self.prev_player = self.find_player(turn)
        else:
            self.prev_player = self.find_player(self.current_turn)
        self.prev_player.rearrange_deck()

        if turn:
            next_turn = turn
        else:
            next_turn = Direction((self.current_turn.value + 1) % 4)

        if self.latest_discarded_tile:
            print(f"Latest discard tile: {self.latest_discarded_tile}")
            for player in self.player_list:
                if player == self.prev_player:
                    continue
                if player.direction == next_turn:
                    player.check_call(
                        self.latest_discarded_tile,
                        is_current_turn=False,
                        round_wind=self.round_direction,
                        check_chii=True,
                    )
                else:
                    player.check_call(
                        self.latest_discarded_tile,
                        is_current_turn=False,
                        round_wind=self.round_direction,
                    )
                if len(player.can_call) > 0:
                    self.call_order.append(player)

            self.call_order.sort(
                key=lambda player: player.can_call[0].value, reverse=True
            )
            if len(self.call_order) > 0:
                self.calling_player = self.call_order.pop()
                return

        if turn:
            self.current_turn = turn
        else:
            self.current_turn = next_turn

        if draw:
            self.action = ActionType.DRAW

        self.current_player = self.find_player(self.current_turn)

        self.current_player.deck_field.build_tiles_position(self.current_player)
        print(
            f"Switch from turn player {self.prev_player.player_idx} to player {self.current_player.player_idx}"
        )

    def find_player(self, turn: Direction) -> Player:
        """
        Find player based on player's turn in current game direction
        """
        return self.player_list[self.direction.index(turn)]

    def do_action(self):
        print(f"########## START {self.action.name.upper()} ACTION ##########")
        print(
            f"Current deck size: {len(self.deck.draw_deck)}, current death field size: {len(self.deck.death_wall)}"
        )
        latest_discarded_tile: Tile = self.latest_discarded_tile

        if self.action:
            if self.calling_player:
                print(f"{self.action} from {self.calling_player}")
            else:
                print(f"{self.action} from {self.current_player}")

        match self.action:
            case ActionType.DRAW:
                try:
                    if self.prev_action == ActionType.KAN:
                        self.__reset_calling_state()
                        tile = self.current_player.draw(
                            self.deck.death_wall,
                            round_wind=self.round_direction,
                            tile=self.deck.death_wall[0],
                        )

                        if len(self.current_player.can_call) > 0:
                            self.call_order.append(self.current_player)

                    else:
                        self.__reset_calling_state()
                        tile = self.current_player.draw(
                            self.deck.draw_deck,
                            round_wind=self.round_direction,
                        )
                except IndexError as e:
                    print("SOME THING WRONG WITH DRAW: ", e.args)
                if len(self.current_player.can_call) > 0:
                    self.call_order.append(self.current_player)
                self.game_log.append_event(ActionType.DRAW, tile, self.current_player)
                print(
                    f"{self.current_player} draw {self.current_player.get_draw_tile()}"
                )

            case ActionType.DISCARD:
                tile: Tile = None
                if (
                    self.current_player.is_riichi() >= 0
                    and self.prev_action is not ActionType.RIICHI
                ):
                    tile = self.current_player.get_draw_tile()
                else:
                    try:
                        tile = list(
                            filter(
                                lambda tile: tile.is_clicked,
                                self.current_player.player_deck,
                            )
                        )[0]
                    except:
                        pass
                if tile:
                    self.__reset_calling_state()
                    self.current_player.discard(tile, self)
                    self.game_log.append_event(
                        ActionType.DISCARD, tile, self.current_player
                    )
                    self.switch_turn()

            case ActionType.CHII:
                calling_player = self.calling_player
                calling_player.build_chii(latest_discarded_tile)
                # TODO
                random_list = self.__get_random_callable_list(calling_player)

                calling_player.call(
                    latest_discarded_tile,
                    random_list,
                    map_action_to_call(self.action),
                    self.current_player,
                )
                self.game_log.append_event(
                    ActionType.CHII,
                    latest_discarded_tile,
                    calling_player,
                    calling_player.call_list[-1],
                )
                self.__handle_switch_turn()

            case ActionType.PON:
                calling_player = self.calling_player
                calling_player.build_pon(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)

                calling_player.call(
                    latest_discarded_tile,
                    random_list,
                    map_action_to_call(self.action),
                    self.current_player,
                )
                self.game_log.append_event(
                    ActionType.PON,
                    latest_discarded_tile,
                    calling_player,
                    calling_player.call_list[-1],
                )
                self.__handle_switch_turn()

            case ActionType.KAN:
                self.deck.add_new_dora()
                is_kakan = False
                calling_player = self.calling_player
                if self.prev_action == ActionType.DRAW:
                    is_kakan, from_who = calling_player.build_kan(
                        calling_player.get_draw_tile()
                    )
                else:
                    calling_player.build_kan(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)
                if self.prev_action == ActionType.DRAW:
                    calling_player.call(
                        calling_player.get_draw_tile(),
                        random_list,
                        map_action_to_call(self.action),
                        None if not is_kakan else self.player_list[from_who],
                        is_kakan,
                    )
                    self.game_log.append_event(
                        ActionType.KAN,
                        calling_player.get_draw_tile(),
                        calling_player,
                        calling_player.call_list[-1],
                    )
                else:
                    calling_player.call(
                        latest_discarded_tile,
                        random_list,
                        map_action_to_call(self.action),
                        self.current_player,
                    )
                    self.game_log.append_event(
                        ActionType.KAN,
                        latest_discarded_tile,
                        calling_player,
                        calling_player.call_list[-1],
                    )
                if calling_player.call_list[-1].is_kakan:
                    self.__reset_calling_state()

                    for player in self.player_list:
                        if player == calling_player:
                            continue
                        player.check_call(
                            calling_player.get_draw_tile(),
                            False,
                            round_wind=self.round_direction,
                            check_chii=False,
                        )

                        if CallType.RON in player.can_call:
                            self.call_order.append(player)
                            self.calling_player = self.call_order.pop()
                else:
                    self.__handle_switch_turn(True)

            case ActionType.RIICHI:
                calling_player = self.calling_player
                self.kyoutaku_number += 1
                calling_player.riichi()
                self.game_log.append_event(
                    ActionType.RIICHI,
                    None,
                    calling_player,
                )
                self.__handle_switch_turn()

            case ActionType.RON:
                calling_player = self.calling_player
                if self.prev_action == ActionType.KAN:
                    self.game_log.append_event(
                        ActionType.RON,
                        self.prev_called_player.get_draw_tile(),
                        calling_player,
                    )
                    return self.end_match(
                        calling_player,
                        self.prev_called_player,
                        self.prev_called_player.get_draw_tile(),
                    )
                else:
                    self.game_log.append_event(
                        ActionType.RON,
                        self.latest_discarded_tile,
                        calling_player,
                    )
                    return self.end_match(
                        calling_player, self.prev_player, self.latest_discarded_tile
                    )
                # End game

            case ActionType.TSUMO:
                calling_player = self.calling_player
                self.game_log.append_event(
                    ActionType.TSUMO,
                    calling_player.get_draw_tile(),
                    calling_player,
                )
                return self.end_match(
                    calling_player,
                    None,
                    calling_player.get_draw_tile(),
                )

            case ActionType.SKIP:
                if self.prev_action == ActionType.KAN and self.prev_called_player:
                    self.__reset_calling_state()
                    self.prev_action = ActionType.KAN
                    self.switch_turn(self.prev_called_player, True)
                elif len(self.call_order) == 0:
                    if self.prev_action == ActionType.DRAW:
                        self.__reset_calling_state()
                        self.switch_turn(self.current_player.direction, False)
                    else:
                        self.__reset_calling_state()
                        self.switch_turn()
                else:
                    self.calling_player = self.call_order.pop()

        if len(self.deck.death_wall) < 14:
            for _ in range(0, 14 - len(self.deck.death_wall)):
                self.deck.death_wall.append(self.deck.draw_deck[0])
                self.deck.draw_deck.remove(self.deck.draw_deck[0])
                self.deck.current_dora_idx -= 1

        self.bot_move_timer = 0
        self.current_player.deck_field.build_tiles_position(self.current_player)

        print(f"########## DONE {self.prev_action.name.upper()} ACTION ##########")

    def __handle_switch_turn(self, draw: bool = False):
        calling_player = self.calling_player

        self.__reset_calling_state()
        if self.prev_action == ActionType.RIICHI:
            calling_player.make_move()
        self.switch_turn(calling_player.direction, draw)

    def __reset_calling_state(self):
        # --- RESET CALLING STATE ---
        self.prev_action = self.action
        self.prev_called_player = self.calling_player
        self.latest_discarded_tile = None
        self.calling_player = None
        self.call_order = []
        self.action = None

        for player in self.player_list:
            player.reset_call()

    def __get_random_callable_list(self, calling_player: Player):
        return calling_player.callable_tiles_list[
            random.randint(0, len(calling_player.callable_tiles_list) - 1)
        ]

    def end_match(
        self,
        win_player: Player = None,
        roned_player: Player = None,
        win_tile: Tile = None,
    ):
        import datetime

        if win_player:
            # is_tsumo
            is_tsumo = True if self.action == ActionType.TSUMO else False

            # is_riichi
            riichi_turn = win_player.is_riichi()
            is_riichi = True if riichi_turn >= 0 else False

            # is_double_riichi
            is_daburu_riichi = True if riichi_turn == 0 else False

            # is_ippatsu
            is_ippatsu = True if riichi_turn == win_player.turn else False

            is_rinshan = True if win_player.get_draw_tile().from_death_wall else False
            is_chankan = (
                True
                if self.prev_action == ActionType.KAN and self.action == ActionType.RON
                else False
            )
            is_haitei = (
                True
                if self.action == ActionType.TSUMO
                and win_player.get_draw_tile() == win_tile
                and len(self.deck.draw_deck) == 0
                else False
            )
            is_houtei = (
                True
                if self.action == ActionType.RON
                and self.latest_discarded_tile == win_tile
                and len(self.deck.draw_deck) == 0
                else False
            )
            is_tenhou = (
                True
                if self.action == ActionType.TSUMO
                and win_player.direction == Direction.EAST
                and win_player.turn == 0
                and len(win_player.melds) == 0
                else False
            )
            is_chiihou = (
                True
                if self.action == ActionType.TSUMO
                and win_player.direction != Direction.EAST
                and win_player.turn == 0
                and len(win_player.melds) == 0
                else False
            )

            is_renhou = (
                True
                if self.action == ActionType.RON and win_player.turn == 0
                else False
            )

            result = self.builder.calculate_player_score(
                player=win_player,
                win_tile=win_tile,
                deck=self.deck,
                is_tsumo=is_tsumo,
                is_riichi=is_riichi,
                is_daburu_riichi=is_daburu_riichi,
                is_ippatsu=is_ippatsu,
                is_rinshan=is_rinshan,
                is_chankan=is_chankan,
                is_haitei=is_haitei,
                is_houtei=is_houtei,
                is_tenhou=is_tenhou,
                is_chiihou=is_chiihou,
                is_renhou=is_renhou,
            )
            deltas = [0, 0, 0, 0]
            total_cost = int(result.cost["total"] / 100)
            if self.action == ActionType.TSUMO:
                deltas[win_player.player_idx] += total_cost
                if win_player.direction == self.round_direction:
                    for i in range(0, len(deltas)):
                        if i == win_player.player_idx:
                            continue
                        deltas[i] -= int(total_cost / 3)
                else:
                    for i in range(0, len(deltas)):
                        if i == win_player.player_idx:
                            continue
                        if self.player_list[i].direction == self.round_direction:
                            deltas[i] -= int(total_cost / 4) * 2
                        else:
                            deltas[i] -= int(total_cost / 4)
            elif self.action == ActionType.RON:
                deltas[win_player.player_idx] += total_cost
                deltas[roned_player.player_idx] -= total_cost
            print(deltas)
            self.game_log.append_event(self.action, win_tile, win_player, None)

            self.game_log.end_round(self.player_list, deltas)
            self.game_log.export(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            self.scenes_controller.change_scene(GameScene.AFTER_MATCH)
        else:
            print("RYUUKYOKU")
            self.scenes_controller.change_scene(GameScene.AFTER_MATCH)

    def __create_new_round_log(self):
        hands = []
        for player in self.player_list:
            hands.append(list(map(lambda tile: tile.__str__(), player.player_deck)))

        match self.round_direction:
            case Direction.EAST:
                round_wind = f"East {self.round_direction_number}"
            case Direction.SOUTH:
                round_wind = f"South {self.round_direction_number}"
            case Direction.WEST:
                round_wind = f"West {self.round_direction_number}"
            case Direction.NORTH:
                round_wind = f"North {self.round_direction_number}"

        self.game_log.new_rounds(
            self.deck.random_seed,
            self.find_player(self.current_turn).player_idx,
            hands,
            round_wind,
            self.tsumi_number,
            self.kyoutaku_number,
        )
