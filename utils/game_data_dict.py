from typing import TypedDict
import typing
from mahjong.hand_calculating.hand_response import HandResponse

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile
    from components.entities.player import Player
    from utils.enums import Direction


class AfterMatchData(TypedDict):
    player_deck: list["Tile"]
    win_tile: "Tile"
    call_tiles_list: list["Tile"]
    result: HandResponse
    player_list: list["Player"]
    deltas: list[int]
    tsumi_number: int
    kyoutaku_number: int
    ryuukyoku: bool
    ryuukyoku_reason: str | None
