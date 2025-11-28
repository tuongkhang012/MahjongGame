import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

TILES = [
    *(f"{n}m" for n in range(1, 10)),
    *(f"{n}p" for n in range(1, 10)),
    *(f"{n}s" for n in range(1, 10)),
    "E", "S", "W", "N", "P", "F", "C"
]
TILE_IDX = {tile: idx for idx, tile in enumerate(TILES)}
AKA_DORA_TILES = ["5mr", "5pr", "5sr"]
TILE_IDX.update({"5mr": 4, "5pr": 13, "5sr": 22})

def fill_row_by_count(plane: np.ndarray, row: int, count: int):
    """ Fill a row of the plane with count number of 1s from left to right."""
    c = min(4, count)
    if c > 0:
        plane[row, 0:c] = 1.0

def fill_row(plane: np.ndarray, row: int):
    """ Fill a row of the plane with count number of 1s from left to right."""
    plane[row, :] = 1.0

def fill_plane(plane: np.ndarray):
    """ Fill multiple rows of the plane with 1s."""
    for row in range(np.size(plane, 0)):
        fill_row(plane, row)