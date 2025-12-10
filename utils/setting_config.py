from typing import TypedDict, Literal


class SettingConfig(TypedDict):
    bgm: int
    sfx: int
    player_1: Literal["shanten", "aggressive", "passive"]
    player_2: Literal["shanten", "aggressive", "passive"]
    player_3: Literal["shanten", "aggressive", "passive"]
    name: str
