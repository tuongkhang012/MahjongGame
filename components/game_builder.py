from utils.enums import Direction
from components.image_cutter import TilesCutter
from utils.constants import TILES_IMAGE_LINK
from pygame import Surface

class GameBuilder:
    def __init__(self, screen: Surface, clock):
        self.screen = screen
        self.clock = clock
        self.tiles_cutter = TilesCutter(TILES_IMAGE_LINK)
        
    def direction(self) -> list[int]:
        import random
        current_direction = random.randint(1,4)
        standard = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_idx = standard.index(Direction(current_direction))
        return standard[current_idx:] + standard[:current_idx]
    
    def visualize_player(self, player_idx):
        match player_idx:
            case 1:
                tile = self.tiles_cutter.cut_tiles("dou", 9)
                self.screen.blit(tile, (0,0))
            case 2:
                pass
