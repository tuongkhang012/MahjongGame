from pygame import Surface


def calculate_center_range(
    screen: Surface, player_idx: int, deck_size: int
) -> tuple[int, int]:
    middle_height = screen.get_height() * 1 / 2
    middle_width = screen.get_width() * 1 / 2
    quarter_height = screen.get_height() * 1 / 3
    quarter_width = screen.get_width() * 1 / 3
    CUSTOM_WIDTH_OFFSET = 16
    CUSTOM_HEIGTH_OFFSET = 32
    match player_idx:
        case 1:
            return (
                middle_width - (deck_size * 16 / 2),
                middle_height + quarter_height,
            )
        case 2:
            return (
                middle_width - quarter_width - CUSTOM_WIDTH_OFFSET,
                middle_height - (deck_size * 16 / 2),
            )
        case 3:
            return (
                middle_width - (deck_size * 16 / 2),
                middle_height - quarter_height - CUSTOM_HEIGTH_OFFSET,
            )
        case 4:
            return (
                middle_width + quarter_width,
                middle_height - (deck_size * 16 / 2),
            )
