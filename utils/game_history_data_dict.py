from typing import TypedDict


class TileData(TypedDict):
    """
    Data class for storing tile information.
    :cvar hand136_idx: The index of the tile in hand136 format.
    :cvar riichi_discard: A flag indicating if the tile was discarded after declaring riichi.
    :cvar from_death_wall: A flag indicating if the tile was drawn from the death wall.
    :cvar is_disabled: A flag indicating if the tile is disabled.
    :cvar string: The string representation of the tile.
    """
    hand136_idx: int
    riichi_discard: bool
    from_death_wall: bool
    is_disabled: bool
    string: str


class MeldData(TypedDict):
    """
    Data class for storing meld information.
    :cvar type: The type idx of meld (e.g., chi, pon, kan).
    :cvar from_who: The player from whom the meld was called. (relative direction)
    :cvar who: The idx player who made the meld.
    :cvar tiles: The tiles involved in the meld.
    :cvar called_tile: The tile that was called to form the meld.
    :cvar opened: A flag indicating if the meld is opened.
    :cvar kakan: A flag indicating if the meld is a kakan (added kan).
    """
    type: int
    from_who: str
    who: int
    tiles: list[TileData]
    called_tile: int | None
    opened: bool
    kakan: bool


class GameHistoryData(TypedDict):
    """
    Data class for storing game history information.

    :cvar seed: The seed used for the game.
    :cvar full_deck: The complete set of tiles used in the game.
    :cvar draw_deck: The deck of tiles available for drawing.
    :cvar death_wall: The tiles in the death wall.
    :cvar dora: The dora indicators.
    :cvar kyoutaku_number: The number of kyoutaku (riichi sticks).
    :cvar tsumi_number: The number of tsumi (deposits).
    :cvar call_order: The order in which players can call tiles.
    :cvar current_direction: The current direction of play.
    :cvar direction: The list of player directions.
    :cvar action: The current action being taken.
    :cvar prev_action: The previous action taken.
    :cvar prev_called_player: The player who made the previous call.
    :cvar prev_player: The previous player.
    :cvar latest_discard_tile_hand136_idx: The index of the latest discarded tile.
    :cvar latest_called_tile_hand136_idx: The index of the latest called tile.
    :cvar calling_player: The player who is currently calling a tile.
    :cvar end_game: A flag indicating if the game has ended.
    :cvar keep_direction: A flag indicating if the direction should be kept.
    :cvar round_direction: The current round direction.
    :cvar round_direction_number: The number of the current round direction.
    :cvar melds: The melds of each player.
    :cvar hands: The hands of each player.
    :cvar discards: The discards of each player.
    :cvar already_discards: The already discarded tiles of each player.
    :cvar reaches: The reach status of each player.
    :cvar reach_turn: The turn number when each player declared reach.
    :cvar points: The points of each player.
    :cvar latest_draw_tile_hand136_idx: The index of the latest drawn tile for each player.
    :cvar can_call: The list of tiles each player can call.
    :cvar callable_tiles_list: The list of callable tiles for each player.
    :cvar is_reaches: Flags indicating if each player has declared reach.
    :cvar is_temporary_furiten: Flags indicating if each player is in temporary furiten.
    :cvar is_riichi_furiten: Flags indicating if each player is in riichi furiten.
    :cvar is_discard_furiten: Flags indicating if each player is in discard furiten.
    :cvar from_log_name: The name of the log from which the data was sourced.
    """
    # Game builder
    seed: str
    full_deck: list[TileData]
    draw_deck: list[TileData]
    death_wall: list[TileData]
    dora: list[TileData]
    kyoutaku_number: int
    tsumi_number: int
    call_order: list[int]
    current_direction: int
    direction: list[int]
    action: int | None
    prev_action: int | None
    prev_called_player: int | None
    prev_player: int | None
    latest_discard_tile_hand136_idx: int | None
    latest_called_tile_hand136_idx: int | None
    calling_player: int | None
    end_game: bool
    keep_direction: bool
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
