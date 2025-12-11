from typing import TypedDict, Literal, Optional
from utils.enums import ActionType, CallType
import typing
from utils.game_history_data_dict import GameHistoryData
import os
import datetime
import json

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile
    from components.entities.call import Call
    from components.entities.player import Player


class MeldLog(TypedDict):
    fromPlayer: int
    type: Literal["chi", "pon", "kan", "chakan"]
    called: int
    tiles: list[int]


class GameEvent(TypedDict):
    type: Literal["Discard", "Draw", "Call", "Dora"]
    tile: str
    player: int | None
    meld: MeldLog | None


class Agari(TypedDict):
    type: Literal["TSUMO", "RON"]
    player: int


class GameRoundLog(TypedDict):
    tenhou_seed: str
    dealer: int
    agari: list[Agari]
    hands: list[list[str]]
    round: list[str, int, int]
    events: list[GameEvent]
    ryuukyoku: bool
    ryuukyoku_tenpai: list[int] | None
    reaches: list[int]
    reach_turns: list[int]
    turns: list[int]
    deltas: list[int]


class GameEventLog:
    rounds: list[GameRoundLog]
    name: str

    def __init__(self, data: GameHistoryData):

        if data:
            self.name = data["from_log_name"]
            with open(f".log/{self.name}.json", "r") as file:
                json_data = json.load(file)
            self.rounds = json_data["rounds"]
            self.round = json_data["rounds"][-1]
            self.events = json_data["rounds"][-1]["events"]
            return
        self.name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.rounds = []
        self.round = None
        self.events = []

    def end_round(self, player_list: list["Player"], deltas: Optional[list[int]] = None):
        """
        Finalize the current round and store the turns and deltas.
        Then append the round to the rounds list.
        :param player_list: List of players in the game
        :type player_list: list[Player]
        :param deltas: List of score changes for each player
        :type deltas: Optional[list[int]]
        :return: None
        """
        self.round["turns"] = []
        for player in player_list:
            self.round["turns"].append(player.turn)
        if deltas:
            self.round["deltas"] = deltas
        self.rounds.append(self.round)

    def new_rounds(
        self,
        tenhou_seed: str,
        dealer: int,
        hands: list[list[str]],
        round_wind: str,
        tsumi_number: int,
        kyoutaku_number: int,
    ):
        self.round: GameRoundLog = {
            "tenhou_seed": tenhou_seed,
            "dealer": dealer,
            "agari": None,
            "events": [],
            "hands": hands,
            "deltas": [0, 0, 0, 0],
            "turns": [0, 0, 0, 0],
            "reaches": [],
            "reach_turns": [],
            "round": [round_wind, tsumi_number, kyoutaku_number],
            "ryuukyoku": False,
            "ryuukyoku_tenpai": None,
        }

    def append_event(
        self,
        type: ActionType,
        tile: "Tile",
        player: "Player" = None,
        call: "Call" = None,
    ):
        event_type = None
        match type:
            case ActionType.DRAW:
                event_type = "Draw"
            case ActionType.DISCARD:
                event_type = "Discard"
            case ActionType.DORA:
                new_event: GameEvent = {"type": "Dora", "tile": tile.__str__()}
                self.round["events"].append(new_event)
                return

            case ActionType.RIICHI:
                self.round["reaches"].append(player.player_idx)
                self.round["reach_turns"].append(player.turn)
                return
            case ActionType.TSUMO:
                self.round["agari"] = {"type": "TSUMO", "player": player.player_idx}
                return
            case ActionType.RON:
                self.round["agari"] = {"type": "RON", "player": player.player_idx}
                return
            case _:
                event_type = "Call"

        tile_str = tile.__str__()
        player = player.player_idx

        if event_type != "Call":
            new_event: GameEvent = {
                "type": event_type,
                "tile": tile_str,
                "player": player,
            }

        else:
            meld_type = None
            match call.type:
                case CallType.CHII:
                    meld_type = "chi"
                case CallType.PON:
                    meld_type = "pon"
                case CallType.KAN:
                    if call.is_kakan:
                        meld_type = "chakan"
                    else:
                        meld_type = "kan"

            new_meld: MeldLog = {
                "fromPlayer": call.meld.from_who,
                "called": call.tiles.index(tile),
                "tiles": list(map(lambda tile: tile.__str__(), call.tiles)),
                "type": meld_type,
            }

            new_event: GameEvent = {
                "type": event_type,
                "player": player,
                "meld": new_meld,
            }

        self.round["events"].append(new_event)

    def export(self):
        import json
        from pathlib import Path

        FILE_FOLDER = ".log/"
        if not os.path.exists(Path(FILE_FOLDER)):
            os.makedirs(FILE_FOLDER)
        os.system(f'attrib +h "{Path(FILE_FOLDER)}"')
        file_path = Path(f".log/{self.name}.json")

        with open(file_path, "w+") as file:
            json.dump({"rounds": self.rounds}, file, indent=2)
