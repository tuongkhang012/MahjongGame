import typing
import numpy as np
from components.entities.ai.helper import fill_row_by_count, fill_plane, fill_row, TILE_IDX, AKA_DORA_TILES
if typing.TYPE_CHECKING:
    from components.game_scenes.game_manager import GameManager
    from components.entities.buttons.tile import Tile


class Encoder:
    """
    Encode game state into input feature planes for CNN. (86 x 34 x 4)

    Plane layout:
    0: Own hand tiles
    1: Aka dora tiles in own hand
    2-5: Everyone's discards
    6-9: Everyone's melds
    10: Dora indicators
    11-13: Riichi status of players (0/1 planes)
    14-17: Rank positions of players (0/1 planes)
    18-25: Kyoku index (8 planes)
    26: Round wind
    27: Own wind
    28-40: Past 1
    41-49: Past 2
    50-58: Past 3
    59-67: Past 4
    68-76: Past 5
    77-85: Past 6
    Total: 86 planes
    """

    def __init__(self):
        self.P = 86
        self.H = 34
        self.W = 4
        self.pov_seat = 0  # default POV seat
        self.pov_order = list(range(4)) # default POV order

    def empty_plane(self) -> np.ndarray:
        return np.zeros((self.P, self.H, self.W), dtype=np.float32)

    def change_POV(self, pov_seat):
        self.pov_seat = pov_seat
        self.pov_order = list(range(4))
        self.pov_order = self.pov_order[pov_seat:] + self.pov_order[:pov_seat]

    @staticmethod
    def _from_arr_to_plane(X: list["Tile"]) -> np.ndarray:
        plane = np.zeros((34, 4), dtype=np.float32)
        counts = {i: 0 for i in range(34)}
        for tile in X:
            idx = TILE_IDX[str(tile)]
            counts[idx] += 1
        for idx, cnt in counts.items():
            fill_row_by_count(plane, idx, cnt)
        return plane

    # ---------------- main encoder ----------------
    def encode_now(self, X: np.ndarray, game_state: "GameManager"):
        player_list = game_state.player_list
        # Plane 0: Own hand tiles
        X[0, :, :] = self._from_arr_to_plane(player_list[self.pov_seat].player_deck)

        # Plane 1: Aka dora tiles in own hand
        plane = np.zeros((34, 4), dtype=np.float32)
        for tile in player_list[self.pov_seat].player_deck:
            if tile in AKA_DORA_TILES:
                fill_row(plane, TILE_IDX[tile])
        X[1, :, :] = plane

        # Planes 2-5: Every discards [self, right, across, left]
        j = 0
        for i in self.pov_order:
            discards = player_list[i].discard_tiles
            X[2 + j, :, :] = self._from_arr_to_plane(discards)
            j += 1

        # Planes 6-9: Every melds [self, right, across, left]
        j = 0
        for i in self.pov_order:
            meld_tiles = player_list[i].call_field.get_tiles_list()
            X[6 + j, :, :] = self._from_arr_to_plane(meld_tiles)
            j += 1

        # Plane 10: Dora indicators
        X[10, :, :] = self._from_arr_to_plane(game_state.deck.dora)

        # Planes 11-13: Riichi status of players [right, across, left]
        for i in range(1, 4):
            if player_list[self.pov_order[i]].is_riichi() >= 0:
                fill_plane(X[10 + i, :, :])

        # Planes 14-17: Rank positions of POV
        # TODO: NEED INITIAL WIND
        rank = 2
        fill_plane(X[14 + rank, :, :])

        # Planes 18-25: Kyoku index (8 planes)
        if game_state.round_direction.value == 0:
            kyoku_idx = game_state.round_direction_number - 1
        else:
            kyoku_idx = game_state.round_direction_number + 3
        fill_plane(X[18 + kyoku_idx, :, :])

        # Plane 26: Round wind
        round_wind = str(game_state.round_direction)[0]
        fill_row(X[26, :, :], TILE_IDX[round_wind])

        # Plane 27: Own wind
        own_wind = str(player_list[self.pov_seat].direction)[0]
        fill_row(X[27, :, :], TILE_IDX[own_wind])

    # def encode_history(self, X: np.ndarray, history: List[Tuple[List[PlayerView], GameState]]):
    #     """ Encode past 6 steps of history into planes. 13 planes for first step, 9 planes for each subsequent step."""
    #     # history[-1] is the most recent past step, each frame views store from 0~3, the self.pov_order store the order:
    #     # [POV, right of POV, opposite of POV, left of POV]
    #
    #     FIRST_FRAME_FLAG = True
    #     offset = 28
    #     for frame in history[::-1]:
    #
    #         # Plane 0: Own hand tiles
    #         past_views, past_game_state = frame
    #         X[offset + 0, :, :] = self._from_arr_to_plane(past_views[self.pov_order[0]].hand_tiles)
    #
    #         # Plane 1-4: Every discards [self, right, across, left]
    #         for i in range(4):
    #             discards = past_views[self.pov_order[i]].discards
    #             X[offset + 1 + i, :, :] = self._from_arr_to_plane(discards)
    #
    #         # Plane 5-8: Every melds [self, right, across, left]
    #         for i in range(4):
    #             meld_tiles = []
    #             for meld_type, tiles in past_views[self.pov_order[i]].melds:
    #                 meld_tiles += tiles
    #             X[offset + 5 + i, :, :] = self._from_arr_to_plane(meld_tiles)
    #
    #         if FIRST_FRAME_FLAG:
    #             # Plane 9: Dora indicators
    #             X[offset + 9, :, :] = self._from_arr_to_plane(past_game_state.dora_indicators)
    #             # Planes 10-12: Riichi status of players [right, across, left]
    #             for i in range(1, 4):
    #                 if past_views[self.pov_order[i]].riichi_declared:
    #                     fill_plane(X[offset + 9 + i, :, :])
    #             offset += 13
    #             FIRST_FRAME_FLAG = False
    #         else:
    #             offset += 9