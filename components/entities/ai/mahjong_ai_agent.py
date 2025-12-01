from __future__ import annotations

import torch
import typing

from utils.enums import ActionType, CallType
from components.entities.ai.model import MahjongCNN
from components.entities.ai.encoder import Encoder

if typing.TYPE_CHECKING:
    from components.entities.player import Player
    from components.game_scenes.game_manager import GameManager


class MahjongAIAgent:
    def __init__(
        self,
        discard_path: str,
        chi_path: str,
        pon_path: str,
        riichi_path: str,
        device: str = "cpu",
    ):
        self.device = device
        self.encoder = Encoder()

        self.discard_model = MahjongCNN().to(device)
        self.discard_model.load_state_dict(
            torch.load(discard_path, map_location=device)
        )
        self.discard_model.eval()

        self.chi_model = MahjongCNN().to(device)
        self.chi_model.load_state_dict(torch.load(chi_path, map_location=device))
        self.chi_model.eval()

        self.pon_model = MahjongCNN().to(device)
        self.pon_model.load_state_dict(torch.load(pon_path, map_location=device))
        self.pon_model.eval()

        self.riichi_model = MahjongCNN().to(device)
        self.riichi_model.load_state_dict(torch.load(riichi_path, map_location=device))
        self.riichi_model.eval()

    def make_move(self, player: Player) -> ActionType:
        gm = player.game_manager  # set in GameBuilder.new

        if CallType.RON in player.can_call:
            return ActionType.RON
        if CallType.TSUMO in player.can_call:
            return ActionType.TSUMO

        if CallType.KAN in player.can_call:
            return ActionType.KAN

        X = self.encoder.empty_plane()
        self.encoder.change_POV(player.player_idx)
        self.encoder.encode_now(X, game_state=gm)  # np.ndarray (86, 34, 4)
        x = torch.from_numpy(X).unsqueeze(0).to(self.device)  # (1,86,34,4)

        if CallType.RIICHI in player.can_call:
            with torch.no_grad():
                _, _, _, out_riichi = self.riichi_model(x)
            probs_riichi = torch.softmax(out_riichi, dim=-1)[0]
            if probs_riichi[1].item() > 0.5:
                return ActionType.RIICHI
            else:
                return ActionType.SKIP

        # 5) Pon / Chi decisions
        if CallType.PON in player.can_call:
            with torch.no_grad():
                _, _, out_pon, _ = self.pon_model(x)
            probs_pon = torch.softmax(out_pon, dim=-1)[0]
            if probs_pon[1].item() > 0.5:
                return ActionType.PON
            else:
                return ActionType.SKIP

        if CallType.CHII in player.can_call:
            with torch.no_grad():
                _, out_chi, _, _ = self.chi_model(x)
            probs_chi = torch.softmax(out_chi, dim=-1)[0]
            print("Chi probs:", probs_chi)
            if probs_chi[1].item() > 0.5:
                return ActionType.CHII
            else:
                return ActionType.SKIP

        with torch.no_grad():
            out_discard, _, _, _ = self.discard_model(x)
        logits_discard = out_discard[0]  # (34,)

        tile_idx = int(torch.argmax(logits_discard).item())
        tile_idx = max(0, min(tile_idx, len(player.player_deck) - 1))
        tile = player.player_deck[tile_idx]
        tile.clicked()
        return ActionType.DISCARD
