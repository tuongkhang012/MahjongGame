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
HISTORY_PATH = ".history/"

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
BETTER_VCR_FONT = "public/fonts/BetterVCR 25.09.ttf"

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

INSTRUCTION_TITLE_COLOR = (237, 171, 64)

HAND_CONFIG_OPTIONS = OptionalRules(
    has_aka_dora=True, has_open_tanyao=True, has_double_yakuman=True
)

# Instruction image assets
INSTRUCTION_ASSETS = {
    "INSTRUCTION_AKADORA": "public\\images\\intro\\akadora.png",
    "INSTRUCTION_ANKAN": "public\\images\\intro\\ankan.png",
    "INSTRUCTION_BAKAZE": "public\\images\\intro\\bakaze.png",
    "INSTRUCTION_CHANKAN": "public\\images\\intro\\chankan.png",
    "INSTRUCTION_CHANTA": "public\\images\\intro\\chanta.png",
    "INSTRUCTION_CHII": "public\\images\\intro\\chii.png",
    "INSTRUCTION_CHIITOITSU": "public\\images\\intro\\chiitoitsu.png",
    "INSTRUCTION_CHINITSU": "public\\images\\intro\\chinitsu.png",
    "INSTRUCTION_CHINROUTOU": "public\\images\\intro\\chinroutou.png",
    "INSTRUCTION_CHUURENPOUTOU": "public\\images\\intro\\chuurenpoutou.png",
    "INSTRUCTION_DAISANGEN": "public\\images\\intro\\daisangen.png",
    "INSTRUCTION_DAISUUSHI": "public\\images\\intro\\daisuushi.png",
    "INSTRUCTION_DORA": "public\\images\\intro\\dora.png",
    "INSTRUCTION_DRAGON": "public\\images\\intro\\dragon.png",
    "INSTRUCTION_HAND": "public\\images\\intro\\hand.png",
    "INSTRUCTION_HONITSU": "public\\images\\intro\\honitsu.png",
    "INSTRUCTION_HONROUTOU": "public\\images\\intro\\honroutou.png",
    "INSTRUCTION_HOURA": "public\\images\\intro\\houra.png",
    "INSTRUCTION_IIPEIKOU": "public\\images\\intro\\iipeikou.png",
    "INSTRUCTION_ITTSU": "public\\images\\intro\\ittsu.png",
    "INSTRUCTION_JIKAZE": "public\\images\\intro\\jikaze.png",
    "INSTRUCTION_JUNCHAN": "public\\images\\intro\\junchan.png",
    "INSTRUCTION_JUNSEICHUURENPOUTOU": "public\\images\\intro\\junseichuurenpoutou.png",
    "INSTRUCTION_KAKAN": "public\\images\\intro\\kakan.png",
    "INSTRUCTION_KOKUSHIMUSOU": "public\\images\\intro\\kokushimusou.png",
    "INSTRUCTION_KOKUSHIMUSOU13MENMACHI": "public\\images\\intro\\kokushimusou13menmachi.png",
    "INSTRUCTION_KYOTAKU": "public\\images\\intro\\kyotaku.png",
    "INSTRUCTION_MAN": "public\\images\\intro\\man.png",
    "INSTRUCTION_MENZENTSUMO": "public\\images\\intro\\menzentsumo.png",
    "INSTRUCTION_MINKAN": "public\\images\\intro\\minkan.png",
    "INSTRUCTION_PAIR": "public\\images\\intro\\pair.png",
    "INSTRUCTION_PIN": "public\\images\\intro\\pin.png",
    "INSTRUCTION_PINFU": "public\\images\\intro\\pinfu.png",
    "INSTRUCTION_PON": "public\\images\\intro\\pon.png",
    "INSTRUCTION_RIICHI": "public\\images\\intro\\riichi.png",
    "INSTRUCTION_RIICHI_YAKU": "public\\images\\intro\\riichi_yaku.png",
    "INSTRUCTION_RYANPEIKOU": "public\\images\\intro\\ryanpeikou.png",
    "INSTRUCTION_RYUUIISOU": "public\\images\\intro\\ryuuiisou.png",
    "INSTRUCTION_SANANKOU": "public\\images\\intro\\sanankou.png",
    "INSTRUCTION_SANGENPAI": "public\\images\\intro\\sangenpai.png",
    "INSTRUCTION_SANKANTSU": "public\\images\\intro\\sankantsu.png",
    "INSTRUCTION_SANSHOKUDOUJUN": "public\\images\\intro\\sanshokudoujun.png",
    "INSTRUCTION_SANSHOKUDOUKOU": "public\\images\\intro\\sanshokudoukou.png",
    "INSTRUCTION_SEQUENCE": "public\\images\\intro\\sequence.png",
    "INSTRUCTION_SHOUSANGEN": "public\\images\\intro\\shousangen.png",
    "INSTRUCTION_SHOUSUUSHI": "public\\images\\intro\\shousuushi.png",
    "INSTRUCTION_SOU": "public\\images\\intro\\sou.png",
    "INSTRUCTION_SUUANKOU": "public\\images\\intro\\suuankou.png",
    "INSTRUCTION_SUUKANTSU": "public\\images\\intro\\suukantsu.png",
    "INSTRUCTION_TANYAO": "public\\images\\intro\\tanyao.png",
    "INSTRUCTION_TANYAO_YAKU": "public\\images\\intro\\tanyao_yaku.png",
    "INSTRUCTION_TENPAI": "public\\images\\intro\\tenpai.png",
    "INSTRUCTION_TERMINAL": "public\\images\\intro\\terminal.png",
    "INSTRUCTION_TOITOI": "public\\images\\intro\\toitoi.png",
    "INSTRUCTION_TRIPLET": "public\\images\\intro\\triplet.png",
    "INSTRUCTION_TSUUIISOU": "public\\images\\intro\\tsuuiisou.png",
    "INSTRUCTION_WIND": "public\\images\\intro\\wind.png",
    "INSTRUCTION_YAKUHAI": "public\\images\\intro\\yakuhai.png",
}
