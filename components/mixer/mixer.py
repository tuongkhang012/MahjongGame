from utils.constants import (
    PLAYER0_SFX,
    PLAYER1_SFX,
    PLAYER2_SFX,
    PLAYER3_SFX,
    DISCARD_TILE_SFX,
)

from utils.enums import ActionType
from pygame.mixer import Sound, Channel
import pygame


class Mixer:
    __queue: list[Sound] = []
    __channel: list[Channel] = []

    def __init__(self):
        self.player0 = self.load_sfx_player(PLAYER0_SFX)
        self.player1 = self.load_sfx_player(PLAYER1_SFX)
        self.player2 = self.load_sfx_player(PLAYER2_SFX)
        self.player3 = self.load_sfx_player(PLAYER3_SFX)
        self.discard_tile_sound = Sound(DISCARD_TILE_SFX)

    def play_queue(self):
        while len(self.__queue) > 0:
            sfx = self.__queue.pop()
            sfx.set_volume(0.7)
            sfx_channel = sfx.play()
            self.__channel.append(sfx_channel)

    def clear_queue(self):
        self.__queue = []
        for channel in self.__channel:
            channel.stop()

    def load_sfx_player(self, sound: dict) -> dict[str, Sound]:
        return {
            "chii": Sound(sound["chii"]),
            "pon": Sound(sound["pon"]),
            "kan": Sound(sound["kan"]),
            "riichi": Sound(sound["riichi"]),
            "ron": Sound(sound["ron"]),
            "tsumo": Sound(sound["tsumo"]),
            "double_riichi": Sound(sound["double_riichi"]),
            "tenpai": Sound(sound["tenpai"]),
            "no_ten": Sound(sound["no_ten"]),
        }

    def add_sound_queue(
        self, player_idx: int, action: ActionType, is_double_riichi: bool = False
    ):
        print(f"Adding sound queue for {action}")
        if action == ActionType.DISCARD:
            self.__queue.append(self.discard_tile_sound)
        if action == ActionType.CHII:
            self.__queue.append(getattr(self, f"player{player_idx}")["chii"])
        if action == ActionType.PON:
            self.__queue.append(getattr(self, f"player{player_idx}")["pon"])
        if action == ActionType.KAN:
            self.__queue.append(getattr(self, f"player{player_idx}")["kan"])
        if action == ActionType.RIICHI:
            if is_double_riichi:
                self.__queue.append(
                    getattr(self, f"player{player_idx}")["double_riichi"]
                )
            else:
                self.__queue.append(getattr(self, f"player{player_idx}")["riichi"])
        if action == ActionType.RON:
            self.__queue.append(getattr(self, f"player{player_idx}")["ron"])
        if action == ActionType.TSUMO:
            self.__queue.append(getattr(self, f"player{player_idx}")["tsumo"])
        if action == ActionType.TENPAI:
            self.__queue.append(getattr(self, f"player{player_idx}")["tenpai"])
        if action == ActionType.NO_TEN:
            self.__queue.append(getattr(self, f"player{player_idx}")["no_ten"])
