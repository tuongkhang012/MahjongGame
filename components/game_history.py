import typing

from utils.enums import Direction
from utils.game_history_data_dict import GameHistoryData
from utils.constants import HISTORY_PATH
import os
import json

if typing.TYPE_CHECKING:
    from components.entities.call import Call
    from components.entities.player import Player
    from components.entities.deck import Deck


class GameHistory:
    data: GameHistoryData = None

    def __init__(self, data: GameHistoryData = None):
        if data:
            self.update(data)

    def update(self, data: GameHistoryData):
        if self.data is None:
            self.data = {}
        self.data["end_game"] = data["end_game"]
        self.data["death_wall"] = data["death_wall"]
        self.data["discards"] = data["discards"]
        self.data["already_discards"] = data["already_discards"]
        self.data["dora"] = data["dora"]
        self.data["draw_deck"] = data["draw_deck"]
        self.data["full_deck"] = data["full_deck"]
        self.data["hands"] = data["hands"]
        self.data["melds"] = data["melds"]
        self.data["points"] = data["points"]
        self.data["reach_turn"] = data["reach_turn"]
        self.data["reaches"] = data["reaches"]
        self.data["is_reaches"] = data["is_reaches"]
        self.data["round_direction"] = data["round_direction"]
        self.data["round_direction_number"] = data["round_direction_number"]
        self.data["seed"] = data["seed"]
        self.data["is_discard_furiten"] = data["is_discard_furiten"]
        self.data["is_riichi_furiten"] = data["is_riichi_furiten"]
        self.data["is_temporary_furiten"] = data["is_temporary_furiten"]
        self.data["current_direction"] = data["current_direction"]
        self.data["direction"] = data["direction"]
        self.data["kyoutaku_number"] = data["kyoutaku_number"]
        self.data["tsumi_number"] = data["tsumi_number"]
        self.data["from_log_name"] = (
            data["from_log_name"] if data.get("from_log_name") else None
        )
        self.data["call_order"] = data["call_order"]
        self.data["calling_player"] = data["calling_player"]
        self.data["can_call"] = data["can_call"]
        self.data["action"] = data["action"]
        self.data["prev_action"] = data["prev_action"]
        self.data["prev_called_player"] = data["prev_called_player"]
        self.data["latest_called_tile_hand136_idx"] = data[
            "latest_called_tile_hand136_idx"
        ]
        self.data["latest_discard_tile_hand136_idx"] = data[
            "latest_discard_tile_hand136_idx"
        ]
        self.data["latest_draw_tile_hand136_idx"] = data["latest_draw_tile_hand136_idx"]
        self.data["callable_tiles_list"] = data["callable_tiles_list"]
        self.data["prev_player"] = data["prev_player"]
        self.data["keep_direction"] = data["keep_direction"]

    def clear(self):
        self.data = None

    def export(self) -> None:
        """
        Export the current game history data to a new JSON file in the history directory.
        The file is named with the next available number based on existing files.
        :return: None
        """
        files = []
        directory = HISTORY_PATH
        # Append all files in the directory to the list
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(files)

        # Create a new file with the next number
        file_path = os.path.join(
            directory, f"{len(files)}.json"
        )

        # Write the data to the file
        with open(file_path, "w+") as file:
            json.dump(self.data, file, indent=4)
