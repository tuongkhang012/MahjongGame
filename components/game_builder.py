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

    def build_tiles_position(self, player: Player) -> None:
        start_x_center, start_y_center = self.calculate_center_range(
            player.player_idx, player.player_deck
        )
        for idx, tile in enumerate(player.player_deck):
            tile.update_tile_surface(player.player_idx)
            tile_surface = (
                tile.get_hidden_surface() if tile.hidden else tile.get_surface()
            )
            tile_width, tile_height = tile_surface.get_size()
            draw_tile_offset = 20

            match player.player_idx:
                case 0:
                    position_x = (
                        start_x_center
                        + tile_width * idx
                        + (
                            draw_tile_offset
                            if tile == player.player_deck[-1]
                            and len(player.player_deck) >= 14
                            else 0
                        )
                    )
                    position_y = start_y_center

                case 2:
                    position_x = (
                        start_x_center
                        - tile_width * idx
                        - (
                            draw_tile_offset
                            if tile == player.player_deck[-1]
                            and len(player.player_deck) >= 14
                            else 0
                        )
                    )
                    position_y = start_y_center

                case 3:
                    position_x = start_x_center
                    position_y = (
                        start_y_center
                        + tile_height / 2 * idx
                        + (
                            draw_tile_offset
                            if tile == player.player_deck[-1]
                            and len(player.player_deck) >= 14
                            else 0
                        )
                    )

                case 1:
                    position_x = start_x_center
                    if tile == player.player_deck[-1] and len(player.player_deck) >= 14:
                        position_y = start_y_center - tile_height / 2 - draw_tile_offset

                    else:
                        position_y = start_y_center + tile_height / 2 * idx

            tile.update_position(position_x, position_y, tile_width, tile_height)

    def calculate_center_range(self, player_idx: int, deck_list: list[Tile]):
        deck_size = len(deck_list)

        middle_height = self.screen.get_height() * 1 / 2
        middle_width = self.screen.get_width() * 1 / 2
        offset_height = self.screen.get_height() * 1 / 3
        offset_width = self.screen.get_width() * 1 / 3

        total_width = list(
            map(lambda tile: tile.get_surface().get_bounding_rect().width, deck_list)
        )
        total_heigth = list(
            map(lambda tile: tile.get_surface().get_bounding_rect().height, deck_list)
        )
        match player_idx:
            case 0:
                return (
                    middle_width
                    - (deck_size * (sum(total_width) / len(total_width)) / 2),
                    middle_height + offset_height,
                )
            case 1:
                return (
                    middle_width + offset_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )
            case 2:
                return (
                    middle_width
                    + (deck_size * (sum(total_width) / len(total_width)) / 2),
                    middle_height - offset_height,
                )
            case 3:
                return (
                    middle_width - offset_width,
                    middle_height
                    - (deck_size * (sum(total_heigth) / len(total_heigth)) / 4),
                )

    def init_game(self):
        # Choose direction for player
        direction = self.direction()
        print(f"Current player direction is {direction[0]}")

        deck = Deck()

        # Create player
        player_list: list[Player] = []
        for i in range(4):
            player_list.append(Player(i, direction[i]))

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
            self.build_tiles_position(player)

        main_player = player_list[direction.index(Direction(0))]
        main_player.draw(deck.draw_deck)
        self.build_tiles_position(main_player)
        player_list[0].reveal_hand()

        return (direction, player_list, deck)
