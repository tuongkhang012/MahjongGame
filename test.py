from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

calculator = HandCalculator()

# 1. FIXED HAND
# I replaced the last '52' with '55' (The 4th unique 5-pin tile)
hands = [2, 0, 43, 40, 42, 54, 53, 126, 125, 124, 52, 104, 105, 106, 107]
win_tile = 52

# 2. Define the Kan
meld_kan = Meld(meld_type=Meld.KAN, tiles=[104, 105, 106, 107], opened=True)

# 3. Configure
config = HandConfig(is_tsumo=True)

# 4. Calculate
result = calculator.estimate_hand_value(
    hands, win_tile, melds=[meld_kan], config=config
)

if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Result: {result.han} Han, {result.fu} Fu")
    print(f"Yaku: {[y.name for y in result.yaku]}")
    # Output: Yakuhai (White Dragon), Toitoi (All Triplets)
