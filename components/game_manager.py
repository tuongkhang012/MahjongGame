import pygame
from utils.constants import WINDOW_SIZE, FPS_LIMIT
from components.game_builder import GameBuilder
from utils.enums import Direction
from components.events.mouse_button_down import MouseButtonDown


class GameManager:
    def __init__(self):
        pygame.init()
        # Display setting
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen.fill("purple")

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60

        self.builder = GameBuilder(self.screen, self.clock)

        # Init game

        self.new()
        self.mouse_button_controller = MouseButtonDown(self.screen)

    def run(self) -> bool:

        # Listen user event
        event = self.listenEvent()
        if event["exit"] == True:
            return False
        else:
            return True

    def listenEvent(self) -> bool:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return {"exit": True}
                case pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_controller.run(event)

                case pygame.MOUSEMOTION:
                    pass
        return {"exit": False}

    def new(self):
        # Choose direction for player
        self.direction = self.builder.direction()

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

        # Draw tiles (13 tiles, main draws 14 tiles)
        self.player_deck = {
            "player1_deck": [],
            "player2_deck": [],
            "player3_deck": [],
            "player4_deck": [],
        }
        for i in range(1, 5):
            for k in range(1, 5):
                player_idx = self.direction.index(Direction(k))

                if i == 4:
                    self.player_deck[f"player{player_idx + 1}_deck"].append(
                        self.draw_deck.pop()
                    )
                else:
                    for j in range(1, 5):
                        self.player_deck[f"player{player_idx + 1}_deck"].append(
                            self.draw_deck.pop()
                        )

        # Remove hidden for player1
        for i in range(1, 5):
            print(f"Player {i} deck: ", self.player_deck[f"player{i}_deck"])

        for tile in self.player_deck["player1_deck"]:
            tile.hidden = False

        # View Dora
        self.dora = self.death_wall[5]

        for player_idx in range(1, 5):
            self.builder.visualize_player(
                player_idx, self.player_deck[f"player{player_idx}_deck"]
            )
