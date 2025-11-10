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
from utils.enums import Direction
from components.events.mouse_button_down import MouseButtonDown
from components.events.mouse_motion import MouseMotion

from pygame import Surface
from components.player import Player
from components.deck import Deck
from utils.helper import build_center_rect
import typing

from components.buttons.tile import Tile


class GameManager:
    __default_screen: Surface
    screen: Surface

    # Player
    player_list: list[Player] = []

    # Deck
    deck: Deck

    # Turn
    current_turn: Direction

    # AI relevant
    bot_move_timer: float = 0
    BOT_MOVE_DELAY: float = 2  # AI "thinks" for 1 seconds

    # Animation related
    animation_tile: Tile | None = None

    def __init__(self):
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

        self.builder = GameBuilder(self.screen, self.clock)

        # Init game
        self.new()

        # Create class event listener
        self.mouse_button_down = MouseButtonDown(self.screen, self, self.deck.full_deck)
        self.mouse_motion = MouseMotion(self.screen, self, self.deck.full_deck)

    def run(self) -> bool:
        # --- Calculate Delta Time ---
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0  # Time in seconds
        self.last_time = current_time

        # --- Update logic game ---
        self.update(delta_time)

        # --- Rendering ---
        self.screen.fill("aquamarine4")
        for player in self.player_list:
            if player.player_idx == 0:
                player.reveal_hand()

            player.render_player_deck(self.screen)

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

        self.player_list[self.direction.index(self.current_turn)].play_tiles.append(
            self.animation_tile
        )

        # Reset animation state
        self.animation_tile = None
        self.animation_timer = 0.0
        self.current_discard_player_direction = None
        pass

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

        current_player_direction = self.direction[0]
        if self.current_turn == current_player_direction:
            current_player = self.player_list[0]
            tiles = list(
                filter(lambda tile: tile.is_clicked, current_player.player_deck)
            )
            for tile in tiles:
                current_player.discard(tile)
                self.switch_turn()

            self.bot_move_timer = 0
            return

        # --- THIS IS BOT TURN ---
        # Add to the "thinking" timer
        self.bot_move_timer += delta_time

        # Wait until the "thinking" time (BOT_MOVE_DELAY) has passed
        if self.bot_move_timer < self.BOT_MOVE_DELAY:
            return  # Not time to move yet

        # --- BOT action ---
        current_bot_index = self.direction.index(self.current_turn)

        # Get BOT player
        current_bot = self.player_list[current_bot_index]

        current_bot.make_move(self)
        current_bot.rearrange_deck()
        self.builder.build_tiles_position(current_bot)

        self.bot_move_timer = 0

        # Next turn
        self.switch_turn()

    def switch_turn(self, turn: Direction = None):
        prev_turn = self.direction.index(self.current_turn)
        prev_player = self.player_list[prev_turn]
        prev_player.rearrange_deck()

        if turn is None:
            self.current_turn = Direction((self.current_turn.value + 1) % 4)
        else:
            self.current_turn = turn

        current_player_idx = self.direction.index(self.current_turn)
        current_player = self.player_list[current_player_idx]
        current_player.draw(self.deck.draw_deck)
        self.builder.build_tiles_position(current_player)

    def listenEvent(self) -> dict[str, bool]:
        if self.animation_tile:
            # Still need to check for QUIT event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"exit": True}
            return {"exit": False}  # Ignore all other events

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down.run(event)

                case pygame.MOUSEMOTION:
                    self.mouse_motion.run(event)

        return {"exit": False}

    def new(self):
        self.direction, self.player_list, self.deck = self.builder.init_game()

        # Assign Turn
        for player in self.player_list:
            print(len(player.player_deck))
        self.current_turn = Direction(0)

    def rearrange_deck(self, player_deck: list[Tile]):
        player_deck.sort(key=lambda tile: (tile.type.value, tile.number))
        return player_deck

    def reset(self):
        pass
