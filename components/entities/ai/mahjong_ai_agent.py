from __future__ import annotations

import random

import torch
import typing

from utils.enums import ActionType, CallType
from components.entities.ai.model import MahjongCNN
from components.entities.ai.encoder import Encoder
from components.entities.ai.helper import TILE_IDX, AKA_DORA_TILES
from utils.enums import TileSource
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

        if CallType.RYUUKYOKU in player.can_call:
            return ActionType.SKIP

        if CallType.RON in player.can_call:
            return ActionType.RON
        if CallType.TSUMO in player.can_call:
            return ActionType.TSUMO

        if CallType.KAN in player.can_call:
            ANKAN_FLAG = False
            player.build_kan(player.get_draw_tile())
            for call in player.callable_tiles_list:
                if len(call) == 4:
                    IS_ANKAN = True

                    for tile in call:
                        if tile.source == TileSource.PLAYER:
                            IS_ANKAN = False
                            break

                    if IS_ANKAN:
                        ANKAN_FLAG = True
                        break
            if ANKAN_FLAG:
                print("Choosing ANKAN")
                return ActionType.KAN
            else:
                print("Skipping KAN")
                return ActionType.SKIP

        X = self.encoder.empty_plane()
        self.encoder.change_POV(player.player_idx)
        self.encoder.encode_now(X, game_state=gm)  # np.ndarray (86, 34, 4)
        x = torch.from_numpy(X).unsqueeze(0).to(self.device)  # (1,86,34,4)

        if CallType.RIICHI in player.can_call:
            with torch.no_grad():
                _, _, _, out_riichi = self.riichi_model(x)
            probs_riichi = torch.softmax(out_riichi, dim=-1)[0]
            print("Riichi probs:", probs_riichi)
            if probs_riichi[1].item() > 0.5:
                return ActionType.RIICHI
            else:
                return ActionType.SKIP

        # Pon / Chi decisions
        if CallType.PON in player.can_call:
            with torch.no_grad():
                _, _, out_pon, _ = self.pon_model(x)
            probs_pon = torch.softmax(out_pon, dim=-1)[0]
            print("Test:", torch.softmax(out_pon, dim=-1))
            print("Pon probs:", probs_pon)
            if probs_pon[1].item() > 0.5:
                return ActionType.PON
            else:
                return ActionType.SKIP

        if CallType.CHII in player.can_call:
            with torch.no_grad():
                _, out_chi, _, _ = self.chi_model(x)
            probs_chi = torch.softmax(out_chi, dim=-1)[0]
            print("Chi probs:", probs_chi.argmax())
            prob_list = list(map(lambda prob: prob.item(), probs_chi))
            if prob_list.index(max(prob_list)) == 0:
                return ActionType.SKIP
            else:
                return ActionType.CHII

        AKA_DORA_KIND_INDICES = [4, 13, 22]

        with torch.no_grad():
            out_discard, _, _, _ = self.discard_model(x)
        logits_discard = out_discard[0]  # (34,)
        tile_kind_idx = int(torch.argmax(logits_discard).item())

        if tile_kind_idx not in AKA_DORA_KIND_INDICES:
            discard_index = -1
            for i, tile in enumerate(player.player_deck):
                if tile_kind_idx == TILE_IDX[str(tile)]:
                    discard_index = i
                    break

        else:
            # This is a 5-tile kind (4, 13, or 22), so we must check for Akadora prioritization.
            non_akadora_indices = []
            akadora_index = -1

            for i, tile in enumerate(player.player_deck):
                if tile_kind_idx == TILE_IDX[str(tile)]:
                    if str(tile) in AKA_DORA_TILES:
                        akadora_index = i
                    else:
                        non_akadora_indices.append(i)

            if non_akadora_indices:
                # Discard a regular 5-tile first.
                discard_index = non_akadora_indices[0]
            elif akadora_index != -1:
                # Only discard the Akadora if no regular 5-tiles of that kind exist.
                discard_index = akadora_index
            else:
                raise ValueError(f"Consistency check failed for tile kind {tile_kind_idx}.")

        tile = player.player_deck[discard_index]
        tile.clicked()
        return ActionType.DISCARD
