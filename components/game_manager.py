import pygame
from utils.constants import WINDOW_SIZE, FPS_LIMIT
from components.game_builder import GameBuilder

class GameManager:
    def __init__(self):
        pygame.init()
        # Display setting
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen.fill("purple")

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60

        self.builder = GameBuilder(self.screen, self.clock)
        self.new()

    def run(self) -> bool:
        # Init game


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
                    print(event)
                case pygame.MOUSEMOTION:
                    pass
        return {"exit": False}
    
    def new(self):
        # Choose direction for player
        self.builder.direction()
        for player_idx in range(1,5):
            self.builder.visualize_player(player_idx)

