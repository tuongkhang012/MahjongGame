from utils.constants import (
    PLAYER0_SFX,
    PLAYER1_SFX,
    PLAYER2_SFX,
    PLAYER3_SFX,
    DISCARD_TILE_SFX,
    BGM_PATH,
)

from utils.enums import ActionType
from pygame.mixer import Sound, Channel
from typing import Literal
import pygame


class Mixer:
    __queue: list[Sound] = []

    bgm: int
    sfx: int

    bgm_state: Literal["main_menu", "game", "riichi", "oppo_riichi"] = None
    bgm_opponent_riichi: list[Sound]
    bgm_game: list[Sound]
    bgm_main_menu: list[Sound]
    bgm_riichi: list[Sound]
    current_bgm_sound: Sound = None
    current_bgm_channel: Channel = None

    def __init__(self, bgm: int, sfx: int):
        self.player0 = self.load_sfx_player(PLAYER0_SFX)
        self.player1 = self.load_sfx_player(PLAYER1_SFX)
        self.player2 = self.load_sfx_player(PLAYER2_SFX)
        self.player3 = self.load_sfx_player(PLAYER3_SFX)
        self.load_bgm(BGM_PATH)

        self.discard_tile_sound = Sound(DISCARD_TILE_SFX)
        self.state = "main_menu"

        self.bgm = bgm
        self.sfx = sfx

    def update_bgm_value(self, value: int):
        self.bgm = value
        self.current_bgm_sound.set_volume(self.bgm / 100)

    def update_sfx_value(self, value: int):
        self.sfx = value
        for sound in self.__queue:
            sound.set_volume(self.sfx / 100)

    def play_background_music(
        self, state: Literal["main_menu", "game", "riichi", "oppo_riichi"]
    ):
        if self.bgm_state == state:
            return

        if (
            self.bgm_state != state
            and self.current_bgm_channel
            and self.current_bgm_channel.get_busy()
        ):
            self.current_bgm_sound.fadeout(1000)
        if state is None:
            self.bgm_state = state
            return

        match state:
            case "main_menu":
                sound = self.get_random_sound(self.bgm_main_menu)
            case "game":
                sound = self.get_random_sound(self.bgm_game)
            case "oppo_riichi":
                sound = self.get_random_sound(self.bgm_opponent_riichi)
            case "riichi":
                sound = self.get_random_sound(self.bgm_riichi)

        if (
            (self.current_bgm_channel and not self.current_bgm_channel.get_busy())
            or self.current_bgm_sound is None
            or self.current_bgm_channel is None
        ):
            self.current_bgm_sound = sound
            self.current_bgm_sound.set_volume(self.bgm / 100)
            self.current_bgm_channel = self.current_bgm_sound.play(-1)
            self.bgm_state = state

    def get_random_sound(self, sound_list: list[Sound]) -> Sound:
        import random

        return sound_list[random.randint(0, len(sound_list) - 1)]

    def play_queue(self):
        while len(self.__queue) > 0:
            sfx = self.__queue.pop()
            sfx.set_volume(self.sfx / 100)
            sfx.play()

    def clear_queue(self):
        self.__queue = []

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

    def load_bgm(self, sound: dict):
        self.bgm_main_menu = [Sound(sound["main_menu"])]
        self.bgm_game = [
            Sound(sound["game_1"]),
            Sound(sound["game_2"]),
        ]
        self.bgm_riichi = [
            Sound(sound["main_riichi_1"]),
            Sound(sound["main_riichi_2"]),
            Sound(sound["main_riichi_3"]),
        ]
        self.bgm_opponent_riichi = [
            Sound(sound["oppo_riichi_1"]),
            Sound(sound["oppo_riichi_2"]),
            Sound(sound["oppo_riichi_3"]),
        ]

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
