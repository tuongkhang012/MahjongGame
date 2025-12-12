from typing import Literal, TypedDict


class SettingConfig(TypedDict):
    """
    Configuration for game settings.

    :cvar bgm: Background music setting (int).
    :cvar sfx: Sound effects setting (int).
    :cvar player_1: Strategy for player 1 (str).
    :cvar player_2: Strategy for player 2 (str).
    :cvar player_3: Strategy for player 3 (str).
    :cvar name: Name of the configuration (str).
    """
    bgm: int
    sfx: int
    player_1: Literal["shanten", "aggressive", "passive"]
    player_2: Literal["shanten", "aggressive", "passive"]
    player_3: Literal["shanten", "aggressive", "passive"]
    name: str
