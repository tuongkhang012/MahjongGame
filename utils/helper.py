from pygame import Surface, Rect, Color
import pygame
import sys
from utils.enums import CallType, ActionType, TileType
import typing
from mahjong.meld import Meld
from utils.setting_config import SettingConfig

if typing.TYPE_CHECKING:
    from components.entities.buttons.tile import Tile


def build_center_rect(screen: Surface, image: Surface) -> Rect:
    """
    Build a centered rectangle for the given image on the screen.
    :param screen: The surface to center on.
    :param image: The image surface to center.
    :return: A Rect object representing the centered position.
    :rtype: Rect
    """
    return image.get_rect(center=screen.get_rect().center)


def draw_hitbox(surface: Surface, color: Color = (255, 0, 0)) -> None:
    """
    Draw the hitbox of the given surface if debug mode is enabled.
    :param surface: The surface to draw the hitbox for.
    :param color: The color of the hitbox outline.
    :return: None
    """
    if len(sys.argv) > 1 and "debug" in sys.argv:
        pygame.draw.rect(surface, color, surface.get_rect(), 2)


def map_call_to_action(call_type: CallType) -> ActionType:
    return ActionType(call_type.value)


def map_action_to_call(action: ActionType) -> CallType | None:
    try:
        return CallType(action.value)
    except:
        return None


def map_call_type_to_meld_type(call_type: CallType) -> Meld | None:
    match call_type:
        case CallType.CHII:
            return Meld.CHI
        case CallType.PON:
            return Meld.PON
        case CallType.KAN:
            return Meld.KAN
        case _:
            return None


def convert_tiles_list_to_hand34(tiles: list["Tile"]) -> list[int]:
    """
    Convert a list of Tile objects to a 34-array hand representation.
    34-array representation counts the number of each tile type in the hand.

    :param tiles: List of Tile objects to convert.
    :return: A list of integers representing the 34-array hand.
    :rtype: list[int]
    """
    from mahjong.tile import TilesConverter

    mans = ""
    sous = ""
    pins = ""
    honors = ""
    for tile in tiles:
        match tile.type:
            case TileType.MAN:
                mans += str(tile.number)
            case TileType.SOU:
                sous += str(tile.number)
            case TileType.PIN:
                pins += str(tile.number)
            case TileType.WIND:
                honors += str(tile.number)
            case TileType.DRAGON:
                honors += str(tile.number + 4)

    return TilesConverter.string_to_34_array(
        man=mans, sou=sous, pin=pins, honors=honors
    )


def convert_tiles_list_to_hand136(tiles: list["Tile"]) -> list[int]:
    """
    Convert a list of Tile objects to a 136-array hand representation.
    136-array representation uses one index per tile.

    :param tiles: List of Tile objects to convert.
    :return: A list of integers representing the 136-array hand.
    :rtype: list[int]
    """
    from mahjong.tile import TilesConverter

    mans = ""
    sous = ""
    pins = ""
    honors = ""
    has_aka = False
    for tile in tiles:
        match tile.type:
            case TileType.MAN:
                if tile.aka:
                    mans += "r"
                    has_aka = True
                else:
                    mans += str(tile.number)
            case TileType.SOU:
                if tile.aka:
                    sous += "r"
                    has_aka = True
                else:
                    sous += str(tile.number)
            case TileType.PIN:
                if tile.aka:
                    pins += "r"
                    has_aka = True
                else:
                    pins += str(tile.number)
            case TileType.WIND:
                honors += str(tile.number)
            case TileType.DRAGON:
                honors += str(tile.number + 4)

    return TilesConverter.string_to_136_array(
        man=mans, sou=sous, pin=pins, honors=honors, has_aka_dora=has_aka
    )


def convert_tile_to_hand34_index(tile: "Tile") -> int:
    """
    Convert a single Tile object to its corresponding index in a 34-array hand representation.

    :param tile: Tile object to convert.
    :return: An integer representing the index in the 34-array hand.
    :rtype: int
    """
    from mahjong.tile import TilesConverter

    mans = ""
    sous = ""
    pins = ""
    honors = ""
    match tile.type:
        case TileType.MAN:
            mans += str(tile.number)
        case TileType.SOU:
            sous += str(tile.number)
        case TileType.PIN:
            pins += str(tile.number)
        case TileType.WIND:
            honors += str(tile.number)
        case TileType.DRAGON:
            honors += str(tile.number + 4)

    return TilesConverter.string_to_34_array(
        man=mans, sou=sous, pin=pins, honors=honors
    ).index(1)


def parse_string_tile(tile: str) -> "Tile":
    """
    Parse a string representation of a tile into its components.
    The string format is expected to be:

    - First character: tile number (1-9 or 'r' for aka dora)
    - Second character: tile type ('m', 'p', 's', 'z')
    :param tile: String representation of the tile.
    :return: Tile object.
    :rtype: Tile
    """
    if len(tile) > 2:
        raise ValueError(f"Wrong string length! Current length: {len(tile)}")

    if not (tile[-1] == "z" or tile[-1] == "m" or tile[-1] == "s" or tile[-1] == "p"):
        raise ValueError(f"Wrong tile format! No type found! Current type: {tile[-1]}")

    tile_type = None
    tile_number = int(tile[0] if tile[0] != "r" else 5)
    tile_aka = False if tile[0] != "r" else True
    if tile_number == "r":
        tile_number = 5
        tile_aka = True
    match tile[-1]:
        case "z":
            if tile_number > 4:
                tile_type = TileType.DRAGON
                tile_number = tile_number - 4
            else:
                tile_type = TileType.WIND

        case "p":
            tile_type = TileType.PIN
        case "s":
            tile_type = TileType.SOU
        case "m":
            tile_type = TileType.MAN
    return (tile_type, tile_number, tile_aka)


def get_config() -> SettingConfig:
    """
    Get the setting configuration from the JSON file.
    :return: SettingConfig object containing the configuration.
    :rtype: SettingConfig
    """
    import json
    from pathlib import Path
    from utils.constants import SETTING_CONFIG_PATH

    with open(Path(SETTING_CONFIG_PATH)) as file:
        config = json.load(file)
    return config


def get_data_from_file(file_name: str) -> dict:
    """
    Get data from a JSON file located in the data directory.
    :param file_name: Name of the JSON file.
    :return: A dictionary containing the data from the JSON file.
    :rtype: dict
    """
    import json

    data = None
    with open(f"data/{file_name}") as json_data:
        data = json.load(json_data)
        json_data.close()

    return data


def split_every_n_chars(text, n) -> list[str]:
    """
    Split a string into chunks of n characters.
    :param text: The string to split.
    :param n: The number of characters per chunk.
    :return: A list of string chunks.
    :rtype: list[str]
    """
    return [text[i: i + n] for i in range(0, len(text), n)]


def find_suitable_tile_in_list(
        tile_number: int,
        tile_type: TileType,
        tile_aka: bool,
        tiles_list: list["Tile"],
) -> "Tile":
    """
    Find a tile in the given list that matches the specified number, type, and aka status.
    :param tile_number: The number of the tile to find.
    :param tile_type: The type of the tile to find.
    :param tile_aka: Whether the tile is an aka dora.
    :param tiles_list: The list of Tile objects to search in.
    :return: The matching Tile object.
    :rtype: Tile
    """
    try:
        return list(
            filter(
                lambda tmp_tile:
                tmp_tile.type == tile_type
                and tmp_tile.number == tile_number
                and tmp_tile.aka == tile_aka,
                tiles_list,
            )
        )[0] # Return the first matching tile
    except IndexError as e:
        raise IndexError(
            f"Can not get tile from list {tile_number}, {tile_type}, {tile_aka}! Error: {e}"
        )


def count_shanten_points(tiles: list["Tile"]) -> int:
    """
    Count the shanten points of the given tiles.
    :param tiles: List of Tile objects to evaluate.
    :return: An integer representing the shanten points.
    :rtype: int
    """
    from mahjong.shanten import Shanten

    shanten_calculator = Shanten()
    points = shanten_calculator.calculate_shanten(
        convert_tiles_list_to_hand34(tiles),
    )
    return points
