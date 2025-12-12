import typing
from typing import TypedDict, Optional
from mahjong.hand_calculating.hand_response import HandResponse

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile
    from components.entities.player import Player


class AfterMatchData(TypedDict):
    """
    Data class representing the state of the game after a match has concluded.
    :cvar player_deck: The tiles in the player's hand at the end of the match.
    :cvar win_tile: The tile that completed the player's hand, if applicable.
    :cvar dora: List of dora indicator tiles.
    :cvar ura_dora: List of ura dora indicator tiles.
    :cvar call_tiles_list: List of tiles that were called (melded) by the player.
    :cvar result: The result of the hand calculation.
    :cvar player_list: List of all players in the game.
    :cvar deltas: List of score changes for each player.
    :cvar tsumi_number: The number of consecutive dealer wins (tsumi).
    :cvar kyoutaku_number: The number of riichi sticks on the table.
    :cvar ryuukyoku: Boolean indicating if the hand ended in a draw.
    :cvar ryuukyoku_reason: Reason for the draw, if applicable.
    """
    player_deck: Optional[list["Tile"]]
    win_tile: Optional["Tile"]
    dora: list["Tile"]
    ura_dora: list["Tile"]
    call_tiles_list: Optional[list["Tile"]]
    result: Optional[HandResponse]
    player_list: list["Player"]
    deltas: list[int]
    tsumi_number: int
    kyoutaku_number: int
    ryuukyoku: bool
    ryuukyoku_reason: Optional[str]
