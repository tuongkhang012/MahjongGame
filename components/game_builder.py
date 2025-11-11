from utils.enums import Direction
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK
from components.buttons.tile import Tile
from pygame import Surface
from utils.enums import TileType
from components.player import Player
from pygame import Rect
from components.deck import Deck


class GameBuilder:
    def __init__(self, screen: Surface, clock):
        self.screen = screen
        self.clock = clock

    def direction(self) -> list[Direction]:
        import random

        current_direction = random.randint(0, 3)
        standard = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx]
        # return standard

    def init_game(self):
        # Choose direction for player
        direction = self.direction()
        print(f"Current player direction is {direction[0]}")

        deck = Deck()

        # Create player
        player_list: list[Player] = []
        for i in range(4):
            player_list.append(Player(self.screen, i, direction[i]))

        # Draw tiles (13 tiles, main draws 14 tiles)
        for i in range(4):
            for k in range(4):
                player_idx = direction.index(Direction(k))
                player = player_list[player_idx]
                if i == 3:
                    player.draw(deck.draw_deck)
                else:
                    for j in range(4):
                        player.draw(deck.draw_deck)

        # Rearrange deck for each player
        for player in player_list:
            player.rearrange_deck()
            player.play_field.build_tiles_position(player)

        main_player = player_list[direction.index(Direction(0))]
        main_player.draw(deck.draw_deck)
        main_player.play_field.build_tiles_position(main_player)
        player_list[0].reveal_hand()

        return (direction, player_list, deck)
