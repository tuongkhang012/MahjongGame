from typing import TypedDict, Literal
from mahjong.meld import Meld


class TileData(TypedDict):
    hand136_idx: int
    riichi_discard: bool
    from_death_wall: bool
    string: str


class MeldData(TypedDict):
    type: str
    from_who: str
    who: str
    tiles: list[TileData]
    called_tile: int
    opened: bool
    kakan: bool


class GameHistoryData(TypedDict):
    # Game builder
    seed: str
    full_deck: list[TileData]
    draw_deck: list[TileData]
    death_wall: list[TileData]
    dora: list[TileData]
    kyoutaku_number: int
    tsumi_number: int
    call_order: list[int]
    calling_tile: TileData
    current_direction: int
    direction: list[int]
    action: int
    prev_action: int
    prev_called_player: int
    latest_discard_tile_hand136_idx: int
    latest_called_tile_hand136_idx: int
    calling_player: int

    # Wind
    round_direction: int
    round_direction_number: int

    # Player relative
    melds: list[list[MeldData]] | None
    hands: list[list[TileData]]
    discards: list[list[TileData]] | None
    already_discards: list[list[TileData]] | None
    reaches: list[int] | None
    reach_turn: list[int] | None
    points: list[int]
    latest_draw_tile_hand136_idx: list[int] | None
    can_call: list[list[int]] | None
    callable_tiles_list: list[list[list[int]]] | None

    # For center board render
    is_reaches: list[bool]
    is_temporary_furiten: list[bool]
    is_riichi_furiten: list[bool]
    is_discard_furiten: list[bool]

    # Log name
    from_log_name: str
