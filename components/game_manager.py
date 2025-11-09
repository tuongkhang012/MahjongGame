import pygame
from utils.constants import WINDOW_SIZE, FPS_LIMIT, GAME_TITLE
from components.game_builder import GameBuilder
from utils.enums import Direction
from components.events.mouse_button_down import MouseButtonDown
from components.events.mouse_motion import MouseMotion
from components.buttons.tile import Tile
from pygame import Surface
from components.player import Player


class GameManager:
    __default_screen: Surface
    screen: Surface

    # Player
    player_list: list[Player] = []

    # Deck
    new_deck: list[Tile] = []
    death_wall: list[Tile] = []
    draw_deck: list[Tile] = []

    # Dora relative
    dora: list[Tile] = []
    ura_dora: list[Tile] = []

    # Turn
    current_turn: Direction

    # AI relevant
    bot_move_timer: float = 0
    BOT_MOVE_DELAY: float = 1  # AI "thinks" for 1 seconds

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
        self.mouse_button_down = MouseButtonDown(self.screen, self.new_deck)
        self.mouse_motion = MouseMotion(self.screen, self.new_deck)

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

        self.__default_screen.blit(self.screen, (0, 0))

        # Listen user event
        event = self.listenEvent()
        if event["exit"] == True:
            return False
        else:
            return True

    def update(self, delta_time: float):
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

        current_bot.make_move()
        self.builder.build_tiles_poistion(current_bot)

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
        current_player.draw(self.draw_deck)
        self.builder.build_tiles_poistion(current_player)

    def listenEvent(self) -> dict[str, bool]:
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
        # Choose direction for player
        self.direction = self.builder.direction()
        print(f"Current player direction is {self.direction[0]}")
        # Build tiles wall
        self.new_deck = self.builder.create_new_deck()

        # Role 2 dices (from 2 -> 12)
        dices_score = self.builder.roll_dices()
        # Cut wall
        cutting_points = 34 * ((dices_score - 1) % 4 + 1) - 2 * dices_score
        self.new_deck = (
            self.new_deck[cutting_points:] + self.new_deck[0 : cutting_points - 1]
        )
        self.draw_deck = self.new_deck[2 * 7 :]
        self.death_wall = self.new_deck[0 : 2 * 7 - 1]

        # Create player
        for i in range(4):
            self.player_list.append(Player(i))

        # Draw tiles (13 tiles, main draws 14 tiles)
        for i in range(4):
            for k in range(4):
                player_idx = self.direction.index(Direction(k))
                player = self.player_list[player_idx]
                if i == 3:
                    player.draw(self.draw_deck)
                else:
                    for j in range(4):
                        player.draw(self.draw_deck)

        # Rearrange deck for each player
        for player in self.player_list:
            player.rearrange_deck()
            self.builder.build_tiles_poistion(player)

        # Assign Turn
        self.current_turn = Direction(1)

        main_player = self.player_list[self.direction.index(Direction(1))]
        main_player.draw(self.draw_deck)
        self.builder.build_tiles_poistion(main_player)
        self.player_list[0].reveal_hand()

        # View Dora
        self.dora = self.death_wall[5]

    def rearrange_deck(self, player_deck: list[Tile]):
        player_deck.sort(key=lambda tile: (tile.type.value, tile.number))
        return player_deck

    def reset(self):
        pass
