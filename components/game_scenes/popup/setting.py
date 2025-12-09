from components.game_scenes.popup.popup import Popup
from pygame import Surface


class Setting(Popup):
    def __init__(self, screen: Surface):
        self.screen = screen
        super().__init__()
