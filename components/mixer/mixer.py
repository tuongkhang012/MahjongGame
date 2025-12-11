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
from typing import Literal, Optional


class Mixer:
    """
    Mixer class to handle background music and sound effects.

    :cvar __queue: List of Sound objects representing the sound effects queue.
    :cvar bgm: Integer volume level for background music (0-100).
    :cvar sfx: Integer volume level for sound effects (0-100).
    :cvar bgm_state: Current state of background music (main_menu, game, riichi, oppo_riichi, None).
    :cvar bgm_opponent_riichi: List of Sound objects for opponent riichi background music.
    :cvar bgm_game: List of Sound objects for game background music.
    :cvar bgm_main_menu: List of Sound objects for main menu background music.
    :cvar bgm_riichi: List of Sound objects for riichi background music.
    :cvar current_bgm_sound: Currently playing Sound object for background music.
    :cvar current_bgm_channel: Currently playing Channel object for background music.

    :ivar player0: Dictionary of Sound objects for player 0 sound effects.
    :ivar player1: Dictionary of Sound objects for player 1 sound effects.
    :ivar player2: Dictionary of Sound objects for player 2 sound effects.
    :ivar player3: Dictionary of Sound objects for player 3 sound effects.
    :ivar discard_tile_sound: Sound object for discard tile sound effect.
    """
    __queue: list[Sound] = []

    bgm: int
    sfx: int

    bgm_state: Optional[Literal["main_menu", "game", "riichi", "oppo_riichi"]] = None
    bgm_opponent_riichi: list[Sound]
    bgm_game: list[Sound]
    bgm_main_menu: list[Sound]
    bgm_riichi: list[Sound]
    current_bgm_sound: Optional[Sound] = None
    current_bgm_channel: Optional[Channel] = None

    def __init__(self, bgm: int, sfx: int) -> None:
        """
        Assigns the initial values for bgm and sfx volume levels and loads sound effects and background music.

        :param bgm: Volume level for background music (0-100).
        :param sfx: Volume level for sound effects (0-100).
        """
        self.player0 = self.load_sfx_player(PLAYER0_SFX)
        self.player1 = self.load_sfx_player(PLAYER1_SFX)
        self.player2 = self.load_sfx_player(PLAYER2_SFX)
        self.player3 = self.load_sfx_player(PLAYER3_SFX)
        self.load_bgm(BGM_PATH)

        self.discard_tile_sound = Sound(DISCARD_TILE_SFX)
        self.state = "main_menu"

        self.bgm = bgm
        self.sfx = sfx

    def update_bgm_value(self, value: int) -> None:
        self.bgm = value
        self.current_bgm_sound.set_volume(self.bgm / 100)

    def update_sfx_value(self, value: int) -> None:
        self.sfx = value
        for sound in self.__queue:
            sound.set_volume(self.sfx / 100)

    def play_background_music(
        self, state: Optional[Literal["main_menu", "game", "riichi", "oppo_riichi"]]
    ):
        # If the bgm is already playing the requested state, do nothing
        if self.bgm_state == state:
            return

        # If there is a current bgm playing and the requested state is different, fade it out
        if (
            self.bgm_state != state
            and self.current_bgm_channel
            and self.current_bgm_channel.get_busy()
        ):
            self.current_bgm_sound.fadeout(1000)

        # If the requested state is None, stop the music
        if state is None:
            self.bgm_state = state
            return

        # Select a random sound from the appropriate bgm list
        sound: Optional[Sound] = None
        match state:
            case "main_menu":
                sound = self.get_random_sound(self.bgm_main_menu)
            case "game":
                sound = self.get_random_sound(self.bgm_game)
            case "oppo_riichi":
                sound = self.get_random_sound(self.bgm_opponent_riichi)
            case "riichi":
                sound = self.get_random_sound(self.bgm_riichi)

        # Play the selected sound if no music is currently playing
        if (
            (self.current_bgm_channel and not self.current_bgm_channel.get_busy())
            or self.current_bgm_sound is None
            or self.current_bgm_channel is None
        ):
            self.current_bgm_sound = sound
            self.current_bgm_sound.set_volume(self.bgm / 100)
            self.current_bgm_channel = self.current_bgm_sound.play(-1)
            self.bgm_state = state

    @staticmethod
    def get_random_sound(sound_list: list[Sound]) -> Sound:
        """
        Selects and returns a random Sound object from the provided list.
        :param sound_list: List of Sound objects to choose from.
        :return: A randomly selected Sound object.
        """
        import random

        return sound_list[random.randint(0, len(sound_list) - 1)]

    def play_queue(self) -> None:
        """
        Plays all sound effects in the queue sequentially.
        :return: None
        """
        while len(self.__queue) > 0:
            sfx = self.__queue.pop()
            sfx.set_volume(self.sfx / 100)
            sfx.play()

    def clear_queue(self) -> None:
        self.__queue = []

    @staticmethod
    def load_sfx_player(sound: dict) -> dict[str, Sound]:
        """
        Loads sound effects for a player from the provided dictionary.
        :param sound: Dictionary containing sound effect file paths.
        :return: Dictionary mapping sound effect names to Sound objects.
        """
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

    def load_bgm(self, sound: dict) -> None:
        """
        Loads background music from the provided dictionary.
        :param sound: Dictionary containing background music file paths.
        :return: None
        """
        self.bgm_main_menu = [
            Sound(sound["main_menu"])
        ]
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
        self,
        player_idx: int,
        action: ActionType,
        is_double_riichi: bool = False
    ) -> None:
        """
        Adds a sound effect to the queue based on the player's action.
        :param player_idx: Index of the player (0-3).
        :param action: ActionType representing the player's action.
        :param is_double_riichi: Boolean indicating if the riichi is a double riichi.
        :return: None
        """
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
                self.__queue.append(
                    getattr(self, f"player{player_idx}")["riichi"]
                )
        if action == ActionType.RON:
            self.__queue.append(getattr(self, f"player{player_idx}")["ron"])
        if action == ActionType.TSUMO:
            self.__queue.append(getattr(self, f"player{player_idx}")["tsumo"])
        if action == ActionType.TENPAI:
            self.__queue.append(getattr(self, f"player{player_idx}")["tenpai"])
        if action == ActionType.NO_TEN:
            self.__queue.append(getattr(self, f"player{player_idx}")["no_ten"])
