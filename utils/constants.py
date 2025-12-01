from mahjong.hand_calculating.hand_config import OptionalRules

FPS_LIMIT = 60
WINDOW_SIZE = (1280, 720)
GAME_TITLE = "Riichi for the Win"

TILES_IMAGE_LINK = "public/images/tiles/sheet.png"
TILE_SCALE_BY = 2.0
TILE_ANIMATION_DURATION = 0.5
TILE_POPUP_DURATION = 1
TILE_WIDTH = 32
TILE_HEIGHT = 32

DIRECTION_IMAGE_LINK = "public/images/directions/direction.png"
DIRECTION_WIDTH = 32
DIRECTION_HEIGHT = 32

SMOKE_PARTICLE_IMAGE_LINK = "public/images/particles/smoke/"
DISCARD_MODEL = "public/model/mahjong_cnn_discard_best.pth"
CHI_MODEL = "public/model/mahjong_cnn_chi_best.pth"
PON_MODEL = "public/model/mahjong_cnn_pon_best.pth"
RIICHI_MODEL = "public/model/mahjong_cnn_riichi_best.pth"
COMBINED_MODEL = "public/model/mahjong_cnn_discard_chi_pon_riichi_best.pth"

MAIN_MENU_BACKGROUND = "public/images/main_menu_bg.png"

TURN_BAR_HEIGHT = 10

CENTER_BOARD_FIELD_SIZE = (540, 540)
DIRECTION_TURN_SIZE = (180, 180)
DISCARD_FIELD_SIZE = (180, 180)

# --- BUTTONS ---
CHI_PON_KAN_FONT_SIZE = 20

MADOU_FUTO_FONT = "public/fonts/MadouFutoMaruGothic-d9Xo7.ttf"
ANMOTALES_FONT = "public/fonts/AncientModernTales-a7Po.ttf"
MINTSODA_FONT = "public/fonts/MintsodaLimeGreen13X16Regular-KVvzA.ttf"
PIXELARI_FONT = "public/fonts/Pixellari.ttf"
ANCIENT_MODERN_FONT = "public/fonts/AncientModernTales-a7Po.ttf"

CALL_BUTTON_COLORS = {
    # --- Winning Actions ---
    "Ron": (214, 69, 75),  # The bright Red from "Ron"
    "Tsumo": (34, 139, 34),  # (Using my previous suggestion, as it's not in the image)
    # --- Meld Actions ---
    "Chii": (0, 138, 135),  # The Teal color from "Chii"
    "Pon": (70, 184, 132),  # The Mint Green color from "Pon"
    "Kan": (91, 56, 138),  # The Dark Purple color from "Kan"
    # --- Special/Neutral Actions ---
    "Riichi": (255, 215, 0),  # (Using my previous suggestion, as it's not in the image)
    "Skip": (112, 112, 112),  # The Medium Gray color from "Skip"
    # --- Ryuukyoku ---
    "Ryuukyoku": (217, 119, 6),
}

COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 166, 181)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (59, 122, 87)
COLOR_GREY = (128, 128, 128)
COLOR_BLACK = (0, 0, 0)
CALL_BUTTON_SIZE = (100, 40)
CALL_TEXT_COLOR = COLOR_WHITE

UI_BUTTON_SIZE = (200, 60)
UI_TEXT_COLOR = COLOR_WHITE
UI_BUTTON_COLOR = (0, 0, 0, int(255 * 0))
UI_FONT_SIZE = 25

HAND_CONFIG_OPTIONS = OptionalRules(
    has_aka_dora=True, has_open_tanyao=True, has_double_yakuman=True
)
