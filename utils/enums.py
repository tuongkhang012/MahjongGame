from enum import Enum


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __str__(self):
        match self.value:
            case 0:
                return f"East"
            case 1:
                return f"South"
            case 2:
                return f"West"
            case 3:
                return f"North"


class TileType(Enum):
    MAN = 0
    PIN = 1
    SOU = 2
    WIND = 3
    DRAGON = 4


class TileSource(Enum):
    DRAW = 0
    PLAYER = 1


class CallType(Enum):
    """
    Type of call (naki)

    - TSUMO: self-draw
    - RON: win by discard
    - RIICHI: riichi declaration
    - KAN: kan call
    - PON: pon call
    - CHII: chii call
    - RYUUKYOKU: draw game
    - SKIP: no call
    """
    TSUMO = 0
    RON = 1
    RIICHI = 2
    KAN = 3
    PON = 4
    CHII = 5
    RYUUKYOKU = 6
    SKIP = 7


class CallName(Enum):
    """
    Name of call (naki) for easier definition

    - CHII: chii
    - PON: pon
    - DAMINKAN: Daminkan
    - ANKAN: ankan
    - KAKAN: kakan (shouminkan)
    - AGARI: agari
    - RON: ron
    """

    CHII = "chii"
    PON = "pon"
    DAIMINKAN = "daiminkan"
    ANKAN = "ankan"
    KAKAN = "kakan"
    AGARI = "agari"
    RON = "ron"


class ActionType(Enum):
    TSUMO = 0
    RON = 1
    RIICHI = 2
    KAN = 3
    PON = 4
    CHII = 5
    RYUUKYOKU = 6
    SKIP = 7
    DRAW = 8
    DISCARD = 9
    DORA = 10
    TENPAI = 11
    NO_TEN = 12


class BasePoints(Enum):
    MANGAN = 2000
    HANEMAN = 3000
    BAIMAN = 4000
    SANBAIMAN = 6000
    YAKUMAN = 8000
    DOUBLE_YAKUMAN = 16000


class GameScene(Enum):
    START = 0
    GAME = 1


class GamePopup(Enum):
    AFTER_MATCH = 0
    INSTRUCTION = 1
    SETTING = 2


class InstructionSection(Enum):
    TUTORIAL = 0
    YAKU_OVERVIEW = 1
