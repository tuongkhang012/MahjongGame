from typing import TypedDict, Literal


class SettingConfig(TypedDict):
    bgm: int
    sfx: int
    player_1: Literal["shanten", "agressive", "passive"]
    player_2: Literal["shanten", "agressive", "passive"]
    player_3: Literal["shanten", "agressive", "passive"]
    name: str
