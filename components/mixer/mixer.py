from utils.constants import PLAYER0_SFX, PLAYER1_SFX, PLAYER2_SFX, PLAYER3_SFX

# from utils.enums import


class Mixer:
    __queue: list

    def __init__(self):
        self.player0 = self.load_sfx_player(None)

    def load_sfx_player(self, sound: dict):
        pass

    def play_action_sound(self):
        pass
