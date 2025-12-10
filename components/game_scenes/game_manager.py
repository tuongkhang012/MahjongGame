import pygame
from utils.constants import (
    WINDOW_SIZE,
    FPS_LIMIT,
    GAME_TITLE,
    TILE_ANIMATION_DURATION,
    TILE_POPUP_DURATION,
    TILE_SCALE_BY,
    DISCARD_MODEL,
    CHI_MODEL,
    PON_MODEL,
    RIICHI_MODEL,
    COMBINED_MODEL,
)

from mahjong.agari import Agari
from components.game_builder import GameBuilder
from utils.enums import Direction, ActionType, CallType, GamePopup, TileType

from utils.game_data_dict import AfterMatchData
from utils.game_history_data_dict import GameHistoryData, MeldData, TileData

from pygame import Surface
from pygame.event import Event
from components.entities.player import Player
from components.entities.deck import Deck
from utils.helper import (
    build_center_rect,
    map_action_to_call,
    count_shanten_points,
    get_config,
)
from components.entities.fields.center_board_field import CenterBoardField
from components.entities.mouse import Mouse
import typing
import random
from components.game_event_log import GameEventLog
from components.entities.ai.mahjong_ai_agent import MahjongAIAgent
from components.entities.buttons.chii import Chii
from components.game_scenes.popup.choose_chii import ChiiPicker
from components.game_scenes.popup.popup import Popup
from components.game_history import GameHistory

# Tile
from components.entities.buttons.tile import Tile
from components.entities.fields.call_button_fields import CallButtonField

if typing.TYPE_CHECKING:
    from components.game_scenes.scenes_controller import ScenesController
    from components.entities.buttons.button import Button
    from components.game_scenes.popup.setting import PickerDataType, BotModelType


class GameManager:
    screen: Surface
    hints_button: "Button"
    scenes_controller: "ScenesController"
    pause: bool = False
    popup: Popup = None
    # Player
    player_list: list[Player] = []
    current_player: Player
    prev_player: Player
    main_player: Player
    direction: list[Direction]

    # Deck
    deck: Deck

    # Field
    center_board_field: CenterBoardField

    # Turn
    current_turn: Direction

    # Round direction
    round_direction: Direction = None
    round_direction_number: int = None

    # AI relevant
    bot_move_timer: float = 0
    BOT_MOVE_DELAY: float = 1  # AI "thinks" for 1 seconds

    # Animation related
    animation_tile: Tile | None = None

    # Game logic relavent
    latest_discarded_tile: Tile | None = None
    latest_called_tile: Tile | None = None
    call_order: list[Player] = []
    calling_player: Player = None
    prev_called_player: Player = None
    action: ActionType = None
    prev_action: ActionType = None
    kan_count: int = 0
    is_disable_round: bool = False
    disable_reason: str = None
    ron_count: int = 0
    picked_chii: list[Tile] = None

    # Score relavent
    tsumi_number: int = 0
    kyoutaku_number: int = 0

    # riichi
    is_main_riichi: bool = False
    is_oppo_riichi: bool = False

    # Change direction when new game
    keep_direction: bool = False
    end_game: bool = False

    def __init__(
        self,
        screen: Surface,
        scenes_controller: "ScenesController",
        init_deck: Deck,
        hints_button: "Button",
        setting_button: "Button",
        game_history: GameHistory,
        start_data=None,
    ):
        # Display setting
        self.main_screen = screen
        self.screen = screen.copy()
        self.clock = (
            pygame.time.Clock()
        )  # TODO: Maybe don't need it since scene_controller has one
        self.clock.tick(FPS_LIMIT)  # limits FPS to 60
        self.last_time = pygame.time.get_ticks()  # For calculating delta time

        # Game log
        self.game_log = GameEventLog(game_history.data)

        # Init deck
        self.builder = GameBuilder(self.screen, self.clock, init_deck, start_data)

        # AI designated seat
        config = get_config()
        self.bot_1_model: BotModelType = config["player_1"]
        self.bot_2_model: BotModelType = config["player_2"]
        self.bot_3_model: BotModelType = config["player_3"]

        self.ai_agent_SMART = MahjongAIAgent(
            DISCARD_MODEL, CHI_MODEL, PON_MODEL, RIICHI_MODEL
        )

        self.ai_agent_MID = MahjongAIAgent(
            COMBINED_MODEL, COMBINED_MODEL, COMBINED_MODEL, COMBINED_MODEL
        )

        self.game_history = game_history

        if self.game_history.data is None:
            # Init game
            self.builder.new(self)
            self.__create_new_round_log()
            self.deck.add_new_dora()
            self.game_log.append_event(
                ActionType.DORA, self.deck.death_wall[self.deck.current_dora_idx]
            )
        else:
            if self.game_history.data["end_game"] == True:
                self.builder
                for i in range(0, 4):
                    self.builder.deck.clear_seed()
                    self.builder.deck.create_new_deck()
                    self.player_list.append(
                        Player(
                            self.screen,
                            i,
                            Direction(self.game_history.data["direction"][i]),
                            full_deck=self.builder.deck.full_deck,
                            points=self.game_history.data["points"][i],
                        )
                    )
                self.keep_direction = self.game_history.data["keep_direction"]
                self.new_game()
                self.game_history.data = None
            else:
                self.builder.continue_game(self)

        self.call_button_field = CallButtonField(self.screen)

        # Hints button init
        PADDING_HINTS_BUTTON_Y = 20
        PADDING_HINTS_BUTTON_X = 100
        self.hints_button = hints_button
        self.hints_button.update_position(
            self.screen.get_width()
            - PADDING_HINTS_BUTTON_X
            - self.hints_button.get_surface().get_width(),
            PADDING_HINTS_BUTTON_Y,
        )

        self.setting_button = setting_button
        self.setting_button.update_position(
            self.screen.get_width()
            - PADDING_HINTS_BUTTON_X
            - self.setting_button.get_surface().get_width(),
            PADDING_HINTS_BUTTON_Y * 2 + self.hints_button.get_surface().get_height(),
        )

        self.scenes_controller = scenes_controller

    def render(self) -> Surface:
        # --- Calculate Delta Time ---
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0  # Time in seconds
        self.last_time = current_time

        # --- Update logic game ---
        if not self.pause:
            self.update(delta_time)

        # --- Rendering ---
        self.screen.fill("aquamarine4")

        self.center_board_field.render(self.current_turn)
        self.call_button_field.render_particles(self.screen)
        for player in self.player_list:
            player.deck_field.render(player)

            if player == self.main_player:
                if self.calling_player and self.main_player == self.calling_player:

                    self.call_button_field.render(self.main_player.can_call)
                player.reveal_hand()

            if len(player.call_list) > 0:
                player.call_field.render(self.screen)

        self.hints_button.render(self.screen)
        self.setting_button.render(self.screen)
        if self.animation_tile:
            self.render_discarded_animation(self.animation_tile)

        if self.popup:
            self.popup.render(self.screen)

        self.main_screen.blit(self.screen, (0, 0))
        return self.main_screen

    def render_discarded_animation(self, tile: Tile):
        if not self.animation_tile:
            return

        # Calculate animation progress (0.0 to 1.0)
        progress = self.animation_timer / TILE_ANIMATION_DURATION

        # Zoom from 1x scale up to 3x scale
        scale = 1.0 + progress if 1.0 + progress < TILE_SCALE_BY else TILE_SCALE_BY

        base_image = tile.tiles_cutter.cut_tiles(tile.type, tile.number, tile.aka)

        # Apply scale and alpha
        scaled_image = pygame.transform.rotozoom(base_image, 0, scale)

        # Get position to center it on the screen
        pos = build_center_rect(self.screen, scaled_image)

        # Draw the animating tile
        self.screen.blit(scaled_image, pos)

    def start_discarded_animation(self, tile: Tile):
        if self.animation_tile:
            return

        # Start the animation
        self.animation_tile = tile
        self.animation_timer = 0.0
        self.current_discard_player_direction = self.current_turn

    def finish_discarded_animation(self):
        if not self.animation_tile or self.current_discard_player_direction is None:
            return

        # Reset animation state
        self.animation_tile = None
        self.animation_timer = 0.0
        self.current_discard_player_direction = None

        self.last_time = pygame.time.get_ticks()
        self.detect_mouse_pos(pygame.mouse.get_pos())

    def handle_event(self, event: Event):
        if self.pause:
            return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                player = self.player_list[0]
                call_button_field = self.call_button_field

                if self.hints_button.check_collidepoint(event.pos):
                    self.scenes_controller.popup(GamePopup.INSTRUCTION, None)
                    self.scenes_controller.mouse.default()
                    self.pause = True

                if self.setting_button.check_collidepoint(event.pos):
                    self.scenes_controller.popup(GamePopup.SETTING, None)
                    self.scenes_controller.mouse.default()
                    self.pause = True

                if player == self.current_player and player.deck_field.check_collide(
                    event.pos
                ):
                    clicked_tiles = player.deck_field.click(event.pos)
                    if clicked_tiles is None:
                        return
                    for tile in clicked_tiles:
                        if tile.is_disabled:
                            return
                        tile.clicked()
                    self.action = player.make_move(ActionType.DISCARD)
                    self.scenes_controller.mouse.default()
                    for tile in [
                        tile
                        for tile in self.deck.full_deck
                        if tile.is_hovered or tile.is_highlighted
                    ]:
                        tile.unhovered()
                        tile.unhighlighted()

                if self.popup:
                    if self.popup.check_collide(event.pos):
                        self.picked_chii = self.popup.handle_event(event.pos)
                        self.action = ActionType.CHII
                        self.popup = None

                    else:
                        self.popup = None

                if player == self.calling_player and call_button_field.check_collide(
                    event.pos
                ):
                    call_button_click = call_button_field.click(event.pos, self)

                    if isinstance(call_button_click, Chii):
                        if (
                            self.calling_player
                            and self.calling_player == self.main_player
                        ):
                            self.calling_player.build_chii(self.latest_discarded_tile)

                        if (
                            self.calling_player
                            and self.calling_player == self.main_player
                            and len(self.calling_player.callable_tiles_list) > 1
                        ):
                            self.popup = ChiiPicker(
                                self.calling_player.callable_tiles_list,
                                self.latest_discarded_tile,
                            )
                            self.action = None
                        else:
                            self.picked_chii = self.calling_player.callable_tiles_list[
                                0
                            ]

            case pygame.MOUSEMOTION:
                self.detect_mouse_pos(event.pos)
            case pygame.KEYDOWN:
                if event.key == pygame.K_F9:
                    pygame.image.save(self.render(), "game_scene_screenshot.png")
                    print("Game scene screenshot saved!")

    def detect_mouse_pos(self, mouse_pos: tuple[int, int]):
        player = self.player_list[0]

        hover_button = False
        if self.hints_button.check_collidepoint(
            mouse_pos
        ) or self.setting_button.check_collidepoint(mouse_pos):
            hover_button = True

        hover_picking_chii = None
        if self.popup and self.popup.check_collide(mouse_pos):
            hover_picking_chii = self.popup.handle_event(mouse_pos)

        hover_tiles = None
        if player.deck_field.check_collide(mouse_pos):
            hover_tiles = (
                player.deck_field.hover(mouse_pos)
                if hover_tiles is None
                else hover_tiles
            )
        if self.center_board_field.check_collide(mouse_pos):
            for discard_field in self.center_board_field.get_discard_fields():
                if discard_field.check_collide(mouse_pos):
                    if hover_tiles:
                        break

                    hover_tiles = discard_field.hover(mouse_pos)
                    break

        for player in self.player_list:
            if player.call_field.check_collide(mouse_pos):
                if hover_tiles:
                    break
                hover_tiles = player.call_field.hover(mouse_pos)
                break

        for tile in self.deck.full_deck:
            if hover_tiles and tile in hover_tiles:
                continue
            if tile.hidden:
                continue
            tile.unhighlighted()
            tile.unhovered()

        if hover_tiles:
            for hover_tile in hover_tiles:
                hover_tile.hovered()
                hover_tile.update_hover()

                same_tile_list = list(
                    filter(
                        lambda tile: tile.type == hover_tile.type
                        and tile.number == hover_tile.number
                        and not tile.hidden,
                        self.deck.full_deck,
                    )
                )
                for same_tile in same_tile_list:
                    same_tile.highlighted()

        call_button_hover = None

        if self.call_button_field.check_collide(mouse_pos):
            call_button_hover = self.call_button_field.hover(mouse_pos)
        else:
            self.call_button_field.unhover()

        if hover_tiles or call_button_hover or hover_picking_chii or hover_button:
            self.scenes_controller.mouse.hover()
        else:
            self.scenes_controller.mouse.default()

    def update(self, delta_time: float):
        # --- Passing time for particles ---
        self.call_button_field.update_particles(delta_time)

        # --- Handle animation FIRST ---
        if self.animation_tile:
            self.animation_timer += delta_time

            # Check if animation is finished
            if (
                self.animation_timer >= TILE_ANIMATION_DURATION
                and self.animation_timer >= TILE_POPUP_DURATION
            ):
                self.finish_discarded_animation()

            # While animating, do nothing else (no AI moves, no input)
            return

        if len(self.call_order) > 0 or self.calling_player is not None:
            if self.calling_player is None:
                self.calling_player = self.call_order.pop()
            if self.calling_player == self.main_player:
                if self.action:
                    self.do_action()
                return
            else:
                # --- THIS IS BOT TURN ---
                # Add to the "thinking" timer
                self.bot_move_timer += delta_time
                # Wait until the "thinking" time (BOT_MOVE_DELAY) has passed
                if self.bot_move_timer < self.BOT_MOVE_DELAY:
                    return  # Not time to move yet
                self.action = self.calling_player.make_move()
                print("--- START CHII PON KAN RON ---")

        if self.current_player == self.main_player:
            if self.action:
                self.do_action()
            return

        if self.action is None:
            # --- THIS IS BOT TURN ---
            # Add to the "thinking" timer
            self.bot_move_timer += delta_time

            # Wait until the "thinking" time (BOT_MOVE_DELAY) has passed
            if self.bot_move_timer < self.BOT_MOVE_DELAY:
                return  # Not time to move yet

            # --- BOT action ---
            current_bot = self.current_player
            self.action = current_bot.make_move()

        if self.action:
            self.do_action()

    def switch_turn(self, turn: Direction = None, draw: bool = True):
        self.call_order = []

        if turn:
            self.prev_player = self.find_player(turn)
        else:
            self.prev_player = self.find_player(self.current_turn)
        self.prev_player.rearrange_deck()

        if turn:
            next_turn = turn
        else:
            next_turn = Direction((self.current_turn.value + 1) % 4)

        if self.latest_discarded_tile:
            print(f"Latest discard tile: {self.latest_discarded_tile}")

            # Checking for kaze4
            if all([player.turn == 1 for player in self.player_list]) and all(
                [len(player.discard_tiles) == 1 for player in self.player_list]
            ):
                discard_tile = self.player_list[0].discard_tiles[0]
                if all(
                    [
                        player.discard_tiles[0].type == discard_tile.type
                        and player.discard_tiles[0].number == discard_tile.number
                        for player in self.player_list
                    ]
                ) and all(
                    [
                        player.discard_tiles[0].hand34_idx in [27, 28, 29, 30]
                        for player in self.player_list
                    ]
                ):
                    self.action = ActionType.RYUUKYOKU
                    self.is_disable_round = True
                    self.disable_reason = "Suufon Renda"
                    return

            for player in self.player_list:
                if player == self.prev_player:
                    continue
                if player.direction == next_turn:
                    player.check_call(
                        self.latest_discarded_tile,
                        is_current_turn=False,
                        round_wind=self.round_direction,
                        check_chii=True,
                    )
                else:
                    player.check_call(
                        self.latest_discarded_tile,
                        is_current_turn=False,
                        round_wind=self.round_direction,
                    )
                if len(player.can_call) > 0:
                    self.call_order.append(player)
            self.call_order.sort(
                key=lambda player: (
                    player.can_call[0].value,
                    -((self.prev_player.direction.value - player.direction.value) % 4),
                ),
                reverse=True,
            )
            if len(self.call_order) > 0:
                self.calling_player = self.call_order.pop()
                return

            # Checking for Kan4
            elif len(self.call_order) == 0 and self.kan_count == 4:
                self.action = ActionType.RYUUKYOKU
                self.is_disable_round = True
                self.disable_reason = "Suukaikan"
                return

            # Checking for Reach4
            if (
                all(
                    [CallType.RON not in player.can_call for player in self.player_list]
                )
                and len(self.game_log.round["reaches"]) == 4
            ):
                self.action = ActionType.RYUUKYOKU
                self.is_disable_round = True
                self.disable_reason = "Suucha Riichi"
                return

        if turn:
            self.current_turn = turn
        else:
            self.current_turn = next_turn

        if draw:
            if len(self.deck.draw_deck) == 0:
                self.action = ActionType.RYUUKYOKU
                return
            self.action = ActionType.DRAW

        self.current_player = self.find_player(self.current_turn)

        self.current_player.deck_field.build_tiles_position(self.current_player)
        print(
            f"Switch from turn player {self.prev_player.player_idx} to player {self.current_player.player_idx}"
        )

    def find_player(self, turn: Direction) -> Player:
        """
        Find player based on player's turn in current game direction
        """
        return self.player_list[self.direction.index(turn)]

    def do_action(self):
        print(f"########## START {self.action.name.upper()} ACTION ##########")
        print(
            f"Current deck size: {len(self.deck.draw_deck)}, current death field size: {len(self.deck.death_wall)}"
        )
        latest_discarded_tile: Tile = self.latest_discarded_tile
        if self.action:
            if self.calling_player:
                print(f"{self.action} from {self.calling_player}")
            else:
                print(f"{self.action} from {self.current_player}")

        match self.action:
            case ActionType.DRAW:
                if sum([player.turn for player in self.player_list]) == 0:
                    for player in self.player_list:
                        if player.check_yao9():
                            player.can_call = [CallType.RYUUKYOKU, CallType.SKIP]
                            self.call_order.append(player)

                            print(f"{player} have yao9. Can declare Ryuukyoku...")
                    if len(self.call_order) > 0:
                        self.calling_player = self.call_order.pop()
                        return

                try:
                    if self.prev_action == ActionType.KAN:
                        self.__reset_calling_state()
                        tile = self.current_player.draw(
                            self.deck.death_wall,
                            round_wind=self.round_direction,
                            tile=self.deck.death_wall[0],
                        )

                    else:
                        self.__reset_calling_state()
                        tile = self.current_player.draw(
                            self.deck.draw_deck,
                            round_wind=self.round_direction,
                        )
                except IndexError as e:
                    print("SOME THING WRONG WITH DRAW: ", e.args)
                if len(self.current_player.can_call) > 0 and self.kan_count < 4:
                    self.call_order.append(self.current_player)
                elif self.current_player.is_riichi() >= 0:
                    tile.clicked()
                    self.action = ActionType.DISCARD

                self.game_log.append_event(ActionType.DRAW, tile, self.current_player)
                print(
                    f"{self.current_player} draw {self.current_player.get_draw_tile()}"
                )

            case ActionType.DISCARD:
                tile: Tile = None
                if (
                    self.current_player.is_riichi() >= 0
                    and self.prev_action is not ActionType.RIICHI
                ):
                    tile = self.current_player.get_draw_tile()
                else:
                    try:
                        tile = list(
                            filter(
                                lambda tile: tile.is_clicked,
                                self.current_player.player_deck,
                            )
                        )[0]
                    except:
                        pass
                if tile:
                    if (
                        self.current_player.is_riichi() >= 0
                        and len(
                            list(
                                filter(
                                    lambda tile: tile.is_discard_from_riichi(),
                                    self.current_player.discard_tiles,
                                )
                            )
                        )
                        == 0
                    ):
                        tile.discard_riichi()
                    self.__reset_calling_state()
                    self.current_player.discard(tile, self)
                    self.scenes_controller.mixer.add_sound_queue(
                        self.current_player, ActionType.DISCARD
                    )
                    self.game_log.append_event(
                        ActionType.DISCARD, tile, self.current_player
                    )
                    self.switch_turn()

            case ActionType.CHII:
                calling_player = self.calling_player
                if calling_player != self.main_player:
                    calling_player.build_chii(latest_discarded_tile)
                    self.picked_chii = self.__get_random_callable_list(calling_player)

                calling_player.call(
                    latest_discarded_tile,
                    self.picked_chii,
                    map_action_to_call(self.action),
                    self.current_player,
                )

                self.game_log.append_event(
                    ActionType.CHII,
                    latest_discarded_tile,
                    calling_player,
                    calling_player.call_list[-1],
                )
                self.scenes_controller.mixer.add_sound_queue(
                    calling_player.player_idx, ActionType.CHII
                )
                self.__handle_switch_turn(calling_player)

            case ActionType.PON:
                calling_player = self.calling_player
                calling_player.build_pon(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)

                calling_player.call(
                    latest_discarded_tile,
                    random_list,
                    map_action_to_call(self.action),
                    self.current_player,
                )
                self.game_log.append_event(
                    ActionType.PON,
                    latest_discarded_tile,
                    calling_player,
                    calling_player.call_list[-1],
                )
                self.scenes_controller.mixer.add_sound_queue(
                    calling_player.player_idx, ActionType.PON
                )
                self.__handle_switch_turn(calling_player)

            case ActionType.KAN:
                self.kan_count += 1
                self.deck.add_new_dora()
                self.game_log.append_event(
                    ActionType.DORA, self.deck.death_wall[self.deck.current_dora_idx]
                )
                is_kakan = False
                calling_player = self.calling_player
                if self.prev_action == ActionType.DRAW:
                    is_kakan, from_who = calling_player.build_kan(
                        calling_player.get_draw_tile()
                    )
                else:
                    calling_player.build_kan(latest_discarded_tile)

                random_list = self.__get_random_callable_list(calling_player)
                if self.prev_action == ActionType.DRAW:
                    calling_player.call(
                        calling_player.get_draw_tile(),
                        random_list,
                        map_action_to_call(self.action),
                        None if not is_kakan else self.player_list[from_who],
                        is_kakan,
                    )

                    self.game_log.append_event(
                        ActionType.KAN,
                        calling_player.get_draw_tile(),
                        calling_player,
                        calling_player.call_list[-1],
                    )
                    self.scenes_controller.mixer.add_sound_queue(
                        calling_player.player_idx, ActionType.KAN
                    )
                else:
                    calling_player.call(
                        latest_discarded_tile,
                        random_list,
                        map_action_to_call(self.action),
                        self.current_player,
                    )
                    self.game_log.append_event(
                        ActionType.KAN,
                        latest_discarded_tile,
                        calling_player,
                        calling_player.call_list[-1],
                    )
                    self.scenes_controller.mixer.add_sound_queue(
                        calling_player.player_idx, ActionType.KAN
                    )
                if calling_player.call_list[-1].is_kakan:
                    self.__reset_calling_state()
                    ron_able = False
                    for player in self.player_list:
                        if player == calling_player:
                            continue
                        player.check_call(
                            calling_player.get_draw_tile(),
                            False,
                            round_wind=self.round_direction,
                            check_chii=False,
                        )

                        if CallType.RON in player.can_call:
                            self.call_order.append(player)
                            self.calling_player = self.call_order.pop()
                            ron_able = True

                    if not ron_able:
                        self.__handle_switch_turn(calling_player, True, reset=False)

                else:
                    self.__handle_switch_turn(calling_player, True)

            case ActionType.RIICHI:
                calling_player = self.calling_player
                self.kyoutaku_number += 1
                self.center_board_field.update_kyoutaku_number(self.kyoutaku_number)
                calling_player.riichi()
                self.game_log.append_event(
                    ActionType.RIICHI,
                    None,
                    calling_player,
                )
                if calling_player.turn == 0:
                    is_daburu_riichi = True
                else:
                    is_daburu_riichi = False
                self.scenes_controller.mixer.add_sound_queue(
                    calling_player.player_idx, ActionType.RIICHI, is_daburu_riichi
                )
                if calling_player == self.main_player:
                    self.is_main_riichi = True
                else:
                    self.is_oppo_riichi = True
                self.__handle_switch_turn(calling_player)

            case ActionType.RON:
                calling_player = self.calling_player
                if self.prev_action == ActionType.KAN:

                    if len(self.call_order) > 0:
                        for player in self.call_order:
                            if CallType.RON in player.can_call:
                                self.ron_count += 1

                        # Checking for Ron3
                        if self.ron_count >= 2:
                            self.action = ActionType.RYUUKYOKU
                            self.is_disable_round = True
                            self.disable_reason = "Sanchahou"
                            return self.end_match()
                        else:
                            self.game_log.append_event(
                                ActionType.RON,
                                self.prev_called_player.get_draw_tile(),
                                calling_player,
                            )
                            self.scenes_controller.mixer.add_sound_queue(
                                calling_player.player_idx, ActionType.RON
                            )
                            return self.end_match(
                                calling_player,
                                self.prev_called_player,
                                self.prev_called_player.get_draw_tile(),
                            )
                    else:
                        self.game_log.append_event(
                            ActionType.RON,
                            self.prev_called_player.get_draw_tile(),
                            calling_player,
                        )
                        self.scenes_controller.mixer.add_sound_queue(
                            calling_player.player_idx, ActionType.RON
                        )
                        return self.end_match(
                            calling_player,
                            self.prev_called_player,
                            self.prev_called_player.get_draw_tile(),
                        )
                else:
                    if len(self.call_order) > 0:
                        for player in self.call_order:
                            if CallType.RON in player.can_call:
                                self.ron_count += 1

                        # Checking for Ron3
                        if self.ron_count >= 2:
                            self.action = ActionType.RYUUKYOKU
                            self.is_disable_round = True
                            self.disable_reason = "Sanchahou"
                            return self.end_match()
                        else:
                            self.game_log.append_event(
                                ActionType.RON,
                                self.latest_discarded_tile,
                                calling_player,
                            )
                            self.scenes_controller.mixer.add_sound_queue(
                                calling_player.player_idx, ActionType.RON
                            )
                            return self.end_match(
                                calling_player,
                                self.prev_player,
                                self.latest_discarded_tile,
                            )
                    else:
                        self.game_log.append_event(
                            ActionType.RON,
                            self.latest_discarded_tile,
                            calling_player,
                        )
                        self.scenes_controller.mixer.add_sound_queue(
                            calling_player.player_idx, ActionType.RON
                        )
                        return self.end_match(
                            calling_player, self.prev_player, self.latest_discarded_tile
                        )
                # End game

            case ActionType.TSUMO:
                calling_player = self.calling_player
                self.game_log.append_event(
                    ActionType.TSUMO,
                    calling_player.get_draw_tile(),
                    calling_player,
                )
                self.scenes_controller.mixer.add_sound_queue(
                    calling_player.player_idx, ActionType.TSUMO
                )
                print(
                    "I am checking here", calling_player.get_draw_tile().from_death_wall
                )
                return self.end_match(
                    calling_player,
                    None,
                    calling_player.get_draw_tile(),
                )

            case ActionType.SKIP:
                if (
                    CallType.RON in self.calling_player.can_call
                    and self.calling_player.is_riichi() >= 0
                ):
                    self.calling_player.riichi_furiten = True
                elif CallType.RON in self.calling_player.can_call:
                    self.calling_player.temporary_furiten = True

                if CallType.RYUUKYOKU in self.calling_player.can_call:
                    self.calling_player.skip_yao9()
                if self.prev_action == ActionType.KAN and self.prev_called_player:
                    self.__reset_calling_state()
                    self.prev_action = ActionType.KAN
                    self.switch_turn(self.prev_called_player, True)
                elif len(self.call_order) == 0:
                    if self.prev_action == ActionType.DRAW:
                        self.__reset_calling_state()
                        self.switch_turn(self.current_player.direction, False)
                    else:
                        self.__reset_calling_state()
                        self.switch_turn()
                else:
                    self.action = None
                    self.calling_player = self.call_order.pop()

            case ActionType.RYUUKYOKU:
                if self.calling_player and self.calling_player.check_yao9():
                    self.is_disable_round = True
                    self.disable_reason = "Kyuushu Kyuuhai"
                return self.end_match()

        if len(self.deck.death_wall) < 14:
            for _ in range(0, 14 - len(self.deck.death_wall)):
                self.deck.death_wall.append(self.deck.draw_deck[0])
                self.deck.draw_deck.remove(self.deck.draw_deck[0])
                self.deck.current_dora_idx -= 1

        self.bot_move_timer = 0
        self.current_player.deck_field.build_tiles_position(self.current_player)

        print(f"########## DONE {self.prev_action.name.upper()} ACTION ##########")

    def __handle_switch_turn(
        self, calling_player: Player, draw: bool = False, reset: bool = True
    ):

        if reset:
            self.__reset_calling_state()
        if self.prev_action == ActionType.RIICHI:
            calling_player.make_move()
        self.switch_turn(calling_player.direction, draw)

    def __reset_calling_state(self):
        # --- RESET CALLING STATE ---
        self.picked_chii = None
        self.prev_action = self.action
        self.prev_called_player = self.calling_player
        self.latest_discarded_tile = None
        self.calling_player = None
        self.call_order = []
        self.action = None

        for player in self.player_list:
            player.reset_call()

    def __get_random_callable_list(self, calling_player: Player):
        return calling_player.callable_tiles_list[
            random.randint(0, len(calling_player.callable_tiles_list) - 1)
        ]

    def end_match(
        self,
        win_player: Player = None,
        roned_player: Player = None,
        win_tile: Tile = None,
        disable_reason: str = None,
    ):
        self.pause = True
        deltas = [0, 0, 0, 0]
        for player in self.player_list:
            if count_shanten_points(player.player_deck) == 0:
                player.reveal_hand()
        if self.is_disable_round:
            self.game_log.round = None

            popup_data: AfterMatchData = {
                "deltas": deltas,
                "win_tile": None,
                "kyoutaku_number": self.kyoutaku_number,
                "player_list": self.player_list,
                "result": None,
                "player_deck": None,
                "call_tiles_list": None,
                "tsumi_number": self.tsumi_number,
                "ryuukyoku": True,
                "ryuukyoku_reason": self.disable_reason,
                "dora": [],
                "ura_dora": [],
            }
            self.scenes_controller.popup(GamePopup.AFTER_MATCH, popup_data)

            return
        if win_player:
            # is_tsumo
            is_tsumo = True if self.action == ActionType.TSUMO else False

            # is_riichi
            riichi_turn = win_player.is_riichi()
            is_riichi = True if riichi_turn >= 0 else False
            ura_dora = []
            if is_riichi:
                start_ura_dora_idx = 4
                for i in range(0, len(self.deck.dora)):
                    ura_dora.append(self.deck.death_wall[start_ura_dora_idx])
                    start_ura_dora_idx += 2

            # is_double_riichi
            is_daburu_riichi = True if riichi_turn == 0 else False

            # is_ippatsu
            is_ippatsu = (
                True
                if win_player.is_riichi() >= 0 and riichi_turn == win_player.turn - 1
                else False
            )

            is_rinshan = True if win_player.get_draw_tile().from_death_wall else False
            is_chankan = (
                True
                if self.prev_action == ActionType.KAN and self.action == ActionType.RON
                else False
            )
            is_haitei = (
                True
                if self.action == ActionType.TSUMO
                and win_player.get_draw_tile() == win_tile
                and len(self.deck.draw_deck) == 0
                else False
            )
            is_houtei = (
                True
                if self.action == ActionType.RON
                and self.latest_discarded_tile == win_tile
                and len(self.deck.draw_deck) == 0
                else False
            )
            is_tenhou = (
                True
                if self.action == ActionType.TSUMO
                and win_player.direction == Direction.EAST
                and win_player.turn == 0
                and len(win_player.melds) == 0
                else False
            )
            is_chiihou = (
                True
                if self.action == ActionType.TSUMO
                and win_player.direction != Direction.EAST
                and win_player.turn == 0
                and len(win_player.melds) == 0
                else False
            )

            is_renhou = (
                True
                if self.action == ActionType.RON and win_player.turn == 0
                else False
            )

            result = self.builder.calculate_player_score(
                player=win_player,
                round_wind=self.round_direction,
                win_tile=win_tile,
                deck=self.deck,
                is_tsumo=is_tsumo,
                is_riichi=is_riichi,
                is_daburu_riichi=is_daburu_riichi,
                is_ippatsu=is_ippatsu,
                is_rinshan=is_rinshan,
                is_chankan=is_chankan,
                is_haitei=is_haitei,
                is_houtei=is_houtei,
                is_tenhou=is_tenhou,
                is_chiihou=is_chiihou,
                is_renhou=is_renhou,
                tsumi_number=self.tsumi_number,
                kyoutaku_number=self.kyoutaku_number,
                ura_dora=ura_dora,
            )
            total_cost = int(result.cost["total"] / 100)
            if self.action == ActionType.TSUMO:
                deltas[win_player.player_idx] += total_cost
                divided_cost = (
                    total_cost - self.tsumi_number * 3 - self.kyoutaku_number * 10
                )
                if win_player.direction == Direction.EAST:
                    self.keep_direction = True
                    for i in range(0, len(deltas)):
                        if i == win_player.player_idx:
                            continue

                        deltas[i] -= int(divided_cost / 3) + self.tsumi_number
                else:
                    for i in range(0, len(deltas)):
                        if i == win_player.player_idx:
                            continue
                        if self.player_list[i].direction == Direction.EAST:
                            deltas[i] -= int(divided_cost / 4) * 2 + self.tsumi_number
                        else:
                            deltas[i] -= int(divided_cost / 4) + self.tsumi_number
            elif self.action == ActionType.RON:
                actual_cost = total_cost - self.kyoutaku_number * 10
                if win_player.direction == Direction.EAST:
                    self.keep_direction = True
                deltas[win_player.player_idx] += total_cost
                deltas[roned_player.player_idx] -= actual_cost

            self.game_log.append_event(self.action, win_tile, win_player, None)
            copy_player_deck = win_player.player_deck.copy()
            if win_tile not in copy_player_deck:
                copy_player_deck.append(win_tile)
            popup_data: AfterMatchData = {
                "deltas": deltas,
                "win_tile": win_tile,
                "kyoutaku_number": self.kyoutaku_number,
                "player_list": self.player_list,
                "result": result,
                "player_deck": win_player.player_deck,
                "call_tiles_list": win_player.call_tiles_list,
                "tsumi_number": self.tsumi_number,
                "ryuukyoku": False,
                "ryuukyoku_reason": None,
                "ura_dora": ura_dora,
                "dora": self.deck.dora,
            }
            self.kyoutaku_number = 0
            if win_player.direction == Direction.EAST:
                self.tsumi_number += 1
            else:
                self.tsumi_number = 0
        else:
            # Check nagashi mangan player
            is_nagashi_mangan = False
            nagashi_mangan_player = None
            for direction in Direction:
                player = self.find_player(Direction(direction.value))
                if len(player.get_all_discarded_tiles()) == len(player.discard_tiles):
                    found_not_suitable_tile = False
                    for tile in player.discard_tiles:
                        if tile.type not in [TileType.DRAGON, TileType.WIND] and not (
                            tile.number == 1 or tile.number == 9
                        ):
                            found_not_suitable_tile = True
                            break

                    if not found_not_suitable_tile:
                        is_nagashi_mangan = True
                        nagashi_mangan_player = player
                        break

            # Handle nagashi mangan
            if is_nagashi_mangan:
                result = self.builder.calculate_player_score(is_nagashi_mangan=True)
                total_cost = int(result.cost["total"] / 100)
                deltas[nagashi_mangan_player.player_idx] += total_cost

                if nagashi_mangan_player.direction == Direction.EAST:
                    for i in range(0, len(deltas)):
                        if i == nagashi_mangan_player.player_idx:
                            continue

                        deltas[i] -= int(total_cost / 3)
                else:
                    for i in range(0, len(deltas)):
                        if i == nagashi_mangan_player.player_idx:
                            continue
                        if self.player_list[i].direction == Direction.EAST:
                            deltas[i] -= int(total_cost / 4) * 2
                        else:
                            deltas[i] -= int(total_cost / 4)

                for player in self.player_list:
                    if count_shanten_points(player.player_deck) == 0:
                        if player.direction == Direction.EAST:
                            self.keep_direction = True

            # Tenpai player
            else:
                max_deltas_points = 30
                tenpai_players: list[Player] = []
                for player in self.player_list:
                    if count_shanten_points(player.player_deck) == 0:
                        tenpai_players.append(player)
                if not (len(tenpai_players) == 0 or len(tenpai_players) == 4):
                    for player in self.player_list:
                        if player in tenpai_players:
                            if player.direction == Direction.EAST:
                                self.keep_direction = True
                            deltas[player.player_idx] += int(
                                max_deltas_points / len(tenpai_players)
                            )
                        if player not in tenpai_players:
                            deltas[player.player_idx] -= int(
                                max_deltas_points / (4 - len(tenpai_players))
                            )
                if self.main_player in tenpai_players:
                    self.scenes_controller.mixer.add_sound_queue(
                        self.main_player.player_idx, ActionType.TENPAI
                    )
                else:
                    self.scenes_controller.mixer.add_sound_queue(
                        self.main_player.player_idx, ActionType.NO_TEN
                    )

                self.game_log.round["ryuukyoku_tenpai"] = (
                    None
                    if len(tenpai_players) == 0
                    else list(map(lambda player: player.player_idx, tenpai_players))
                )

            self.game_log.round["ryuukyoku"] = True

            self.game_log.round["deltas"] = deltas
            popup_data: AfterMatchData = {
                "deltas": deltas,
                "player_deck": None,
                "win_tile": None,
                "call_tiles_list": None,
                "kyoutaku_number": self.kyoutaku_number,
                "player_list": self.player_list,
                "result": None,
                "tsumi_number": self.tsumi_number,
                "ryuukyoku": True,
                "ryuukyoku_reason": self.disable_reason,
                "ura_dora": [],
                "dora": [],
            }

        for idx, delta in enumerate(deltas):
            self.player_list[idx].points += delta * 100

        self.game_log.end_round(self.player_list, deltas)
        self.end_game = True
        game_history_data = self.__dict__()
        game_history_data["from_log_name"] = self.game_log.name
        self.game_history.update(game_history_data)
        self.game_history.export()
        self.game_log.export()

        self.scenes_controller.popup(GamePopup.AFTER_MATCH, popup_data)

        files = self.ai_agent_MID.load_files()
        self.ai_agent_MID.read_files(files)
        files = self.ai_agent_SMART.load_files()
        self.ai_agent_SMART.read_files(files)

    def __create_new_round_log(self):
        hands = []
        for player in self.player_list:
            hands.append(list(map(lambda tile: tile.__str__(), player.player_deck)))

        match self.round_direction:
            case Direction.EAST:
                round_wind = f"East {self.round_direction_number}"
            case Direction.SOUTH:
                round_wind = f"South {self.round_direction_number}"
            case Direction.WEST:
                round_wind = f"West {self.round_direction_number}"
            case Direction.NORTH:
                round_wind = f"North {self.round_direction_number}"

        self.game_log.new_rounds(
            self.deck.random_seed,
            self.find_player(self.current_turn).player_idx,
            hands,
            round_wind,
            self.tsumi_number,
            self.kyoutaku_number,
        )

    def new_game(self):
        self.call_button_field = CallButtonField(self.screen)
        self.pause = False
        self.prev_player: Player = None

        self.bot_move_timer: float = 0
        self.BOT_MOVE_DELAY: float = 1

        self.animation_tile: Tile | None = None

        # Game logic relavent
        self.latest_discarded_tile: Tile | None = None
        self.latest_called_tile: Tile | None = None
        self.call_order: list[Player] = []
        self.calling_player: Player = None
        self.prev_called_player: Player = None
        self.action: ActionType = None
        self.prev_action: ActionType = None
        self.kan_count: int = 0
        self.is_disable_round: bool = False
        self.disable_reason: str = None
        self.ron_count: int = 0

        self.is_main_riichi = False
        self.is_oppo_riichi = False

        # Init game
        self.builder.new(self, self.keep_direction)

        # Change direction when new game
        self.keep_direction: bool = False
        self.__create_new_round_log()
        self.deck.add_new_dora()
        self.game_log.append_event(
            ActionType.DORA, self.deck.death_wall[self.deck.current_dora_idx]
        )

    def __dict__(self):
        data: GameHistoryData = {
            "end_game": self.end_game,
            "seed": self.deck.random_seed,
            "death_wall": self.__map_tiles_data(self.deck.death_wall),
            "full_deck": self.__map_tiles_data(self.deck.full_deck),
            "draw_deck": self.__map_tiles_data(self.deck.draw_deck),
            "dora": self.__map_tiles_data(self.deck.dora),
            "round_direction": self.round_direction.value,
            "round_direction_number": self.round_direction_number,
            "discards": [],
            "already_discards": [],
            "melds": [],
            "hands": [],
            "points": [],
            "can_call": [],
            "callable_tiles_list": [],
            "prev_player": self.prev_player.player_idx if self.prev_player else None,
            "reaches": self.game_log.round["reaches"],
            "reach_turn": self.game_log.round["reach_turns"],
            "is_reaches": [],
            "is_riichi_furiten": [],
            "is_temporary_furiten": [],
            "is_discard_furiten": [],
            "current_direction": self.current_turn.value,
            "direction": [],
            "kyoutaku_number": self.kyoutaku_number,
            "tsumi_number": self.tsumi_number,
            "latest_draw_tile_idx": [],
            "call_order": list(map(lambda player: player.player_idx, self.call_order)),
            "action": self.action.value if self.action else None,
            "prev_action": self.prev_action.value if self.prev_action else None,
            "prev_called_player": (
                self.prev_called_player.player_idx if self.prev_called_player else None
            ),
            "latest_discard_tile_hand136_idx": (
                self.latest_discarded_tile.hand136_idx
                if self.latest_discarded_tile
                else None
            ),
            "latest_called_tile_hand136_idx": (
                self.latest_called_tile.hand136_idx if self.latest_called_tile else None
            ),
            "latest_draw_tile_hand136_idx": [],
            "calling_player": (
                self.calling_player.player_idx if self.calling_player else None
            ),
            "keep_direction": self.keep_direction,
        }

        for player in self.player_list:
            data["discards"].append(self.__map_tiles_data(player.discard_tiles))
            data["already_discards"].append(
                self.__map_tiles_data(player.get_all_discarded_tiles())
            )
            if player.can_call:
                data["can_call"].append(
                    list(map(lambda call: call.value, player.can_call))
                )
            else:
                data["can_call"].append([])
            full_callable_list = []
            for callable_list in player.callable_tiles_list:
                callable = self.__map_tiles_data(callable_list)
                full_callable_list.append(callable)
            data["callable_tiles_list"].append(full_callable_list)
            melds = []
            data["latest_draw_tile_hand136_idx"].append(
                player.get_draw_tile().hand136_idx
            )
            for call in player.call_list:

                data_meld: MeldData = {
                    "from_who": call.from_who,
                    "opened": call.is_opened,
                    "tiles": self.__map_tiles_data(call.tiles),
                    "called_tile": (
                        call.tiles.index(call.another_player_tiles)
                        if call.another_player_tiles
                        else None
                    ),
                    "type": call.type.value,
                    "who": call.who,
                    "kakan": call.is_kakan,
                }
                melds.append(data_meld)
            data["melds"].append(melds)
            data["hands"].append(self.__map_tiles_data(player.player_deck))
            data["points"].append(player.points)
            data["is_reaches"].append(True if player.is_riichi() >= 0 else False)
            data["is_riichi_furiten"].append(player.riichi_furiten)
            data["is_temporary_furiten"].append(player.temporary_furiten)
            data["is_discard_furiten"].append(player.discard_furiten)
            data["direction"].append(player.direction.value)

        # print(data)
        return data

    def __map_tiles_data(self, tiles_list: list[Tile]) -> list[TileData]:

        return list(
            map(
                lambda tile: {
                    "hand136_idx": tile.hand136_idx,
                    "riichi_discard": tile.is_discard_from_riichi(),
                    "from_death_wall": tile.from_death_wall,
                    "is_disabled": tile.is_disabled,
                    "string": str(tile),
                },
                tiles_list,
            )
        )

    def __to_str_list(self, iterable: list):
        return list(map(lambda thing: str(thing), iterable))
