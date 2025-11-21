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
from utils.enums import Direction, ActionType
from components.events.mouse_button_down import MouseButtonDown
from components.events.mouse_motion import MouseMotion

from pygame import Surface
from components.player import Player
from components.deck import Deck
from utils.helper import build_center_rect, map_action_to_call
from components.fields.center_board_field import CenterBoardField
from components.fields.discard_field import DiscardField
import typing
import random

# Tile
from components.buttons.tile import Tile

# Call Relative import
from components.fields.call_button_fields import CallButtonField


class GameManager:
    __default_screen: Surface
    screen: Surface

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

    # AI relevant
    bot_move_timer: float = 0
    BOT_MOVE_DELAY: float = 1  # AI "thinks" for 1 seconds

    # Animation related
    animation_tile: Tile | None = None

    # Game logic relavent
    latest_discarded_tile: Tile | None = None
    call_order: list[Player] = []
    calling_player: Player = None
    action: ActionType = None
    prev_action: ActionType = None

    def __init__(self, start_data=None):
        pygame.init()
        # pygame.mixer.init()
        # pygame.freetype.init()

        pygame.display.set_caption(GAME_TITLE)

        # Display setting
        self.__default_screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen = pygame.Surface(
            (self.__default_screen.get_width(), self.__default_screen.get_height()),
            pygame.SRCALPHA,
        )
        self.screen.fill("aquamarine4")
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60
        self.last_time = pygame.time.get_ticks()  # For calculating delta time

        self.builder = GameBuilder(self.screen, self.clock, start_data)

        # Init game
        self.builder.new(self)

        # Create class event listener
        self.mouse_button_down = MouseButtonDown(self.screen, self, self.deck.full_deck)
        self.mouse_motion = MouseMotion(self.screen, self, self.deck.full_deck)
        self.call_button_field = CallButtonField(self.screen)

    def run(self) -> bool:
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

        self.__default_screen.blit(self.screen, (0, 0))

        # Listen user event
        event = self.listenEvent()
        if event["exit"] == True:
            return False
        else:
            return True

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
                        check_chii=True,
                    )
                else:
                    player.check_call(self.latest_discarded_tile, is_current_turn=False)
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

    def listenEvent(self) -> dict[str, bool]:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    if self.animation_tile is None:
                        self.mouse_button_down.run(event)

                case pygame.MOUSEMOTION:
                    self.mouse_motion.run(event)

        return {"exit": False}

    def do_action(self):
        print(f"########## START {self.action.name.upper()} ACTION ##########")
        print(
            f"Current deck size: {len(self.deck.draw_deck)}, current death field size: {len(self.deck.death_wall)}"
        )
        latest_discarded_tile: Tile = self.latest_discarded_tile

        if not self.current_player == self.main_player:
            if self.calling_player:
                print(f"{self.action} from {self.calling_player}")
            else:
                print(f"{self.action} from {self.current_player}")

        match self.action:
            case ActionType.DRAW:
                self.__reset_calling_state()
                try:
                    if self.prev_action == ActionType.KAN:
                        self.current_player.draw(
                            self.deck.death_wall, self.deck.death_wall[0]
                        )
                        if len(self.current_player.can_call) > 0:
                            self.call_order.append(self.current_player)
                        else:
                            self.deck.death_wall.append(self.deck.draw_deck[0])
                            self.deck.draw_deck.remove(self.deck.draw_deck[0])
                    else:
                        self.current_player.draw(self.deck.draw_deck)
                except IndexError as e:
                    print("SOME THING WRONG WITH DRAW: ", e.args)
                if len(self.current_player.can_call) > 0:
                    self.call_order.append(self.current_player)
                print(
                    f"{self.current_player} draw {self.current_player.get_draw_tile()}"
                )

            case ActionType.DISCARD:
                tile: Tile = None
                if self.current_player == self.main_player:
                    try:
                        tile = list(
                            filter(
                                lambda tile: tile.is_clicked,
                                self.main_player.player_deck,
                            )
                        )[0]
                    except:
                        pass

                self.__reset_calling_state()
                self.current_player.discard(tile, self)
                self.switch_turn()

            case ActionType.CHII:
                calling_player = self.calling_player
                calling_player.build_chii(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)

                calling_player.call(
                    latest_discarded_tile,
                    random_list,
                    map_action_to_call(self.action),
                    self.current_player,
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
                self.__handle_switch_turn()

            case ActionType.KAN:
                calling_player = self.calling_player
                if self.prev_action == ActionType.DRAW:
                    calling_player.build_kan(calling_player.get_draw_tile())
                else:
                    calling_player.build_kan(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)
                if self.prev_action == ActionType.DRAW:
                    calling_player.call(
                        calling_player.get_draw_tile(),
                        random_list,
                        map_action_to_call(self.action),
                        None,
                    )
                else:
                    calling_player.call(
                        latest_discarded_tile,
                        random_list,
                        map_action_to_call(self.action),
                        self.current_player,
                    )

                self.__handle_switch_turn(True)

            case ActionType.RIICHI:
                calling_player = self.calling_player
                calling_player.riichi()
                self.__handle_switch_turn()

            case ActionType.RON:
                calling_player = self.calling_player
                # self.action = ActionType.WIN

                # End game

            case ActionType.TSUMO:
                calling_player = self.calling_player
                # self.action = ActionType.WIN

            case ActionType.SKIP:
                if len(self.call_order) == 0:
                    self.__reset_calling_state()
                    self.switch_turn()
                else:
                    self.calling_player = self.call_order.pop()

        self.bot_move_timer = 0
        self.current_player.deck_field.build_tiles_position(self.current_player)

        print(f"########## DONE {self.prev_action.name.upper()} ACTION ##########")

    def __handle_switch_turn(self, draw: bool = False):
        calling_player = self.calling_player
        self.__reset_calling_state()
        self.switch_turn(calling_player.direction, draw)

    def __reset_calling_state(self):
        # --- RESET CALLING STATE ---
        self.prev_action = self.action
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

    def end_match(self, win_player: Player = None):
        if win_player:
            for player in self.player_list:
                self.builder.calculate_player_score(player, self.deck)
        else:
            print("RYUUKYOKU")
