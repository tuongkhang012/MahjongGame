from pygame import Surface, Rect


class Field:
    """
    Base class for all fields.
    :cvar is_hovered: Whether the field is being hovered over.
    :cvar is_clicked: Whether the field is being clicked.
    :cvar surface: The surface of the field.
    :cvar _relative_position: The relative position of the field.
    :cvar _absolute_position: The absolute position of the field.
    :cvar player_idx: The index of the player owning the field.
    """
    is_hovered: bool
    is_clicked: bool
    surface: Surface
    _relative_position: Rect = None
    _absolute_position: Rect = None
    player_idx: int

    def __init__(self):
        self.is_hovered = False
        self.is_clicked = False

    def check_collide(self, position: tuple[float, float]):
        return (
            self._absolute_position.collidepoint(position[0], position[1])
            if self._absolute_position is not None
            else False
        )

    def build_local_mouse(self, mouse_pos: tuple[float, float]) -> tuple[float, float]:
        """
        Build local mouse position relative to the field.
        :param mouse_pos: The mouse position.
        :return: The local mouse position.
        """
        return (
            mouse_pos[0] - self._absolute_position.x,
            mouse_pos[1] - self._absolute_position.y,
        )

    def get_relative_position(self):
        return self._relative_position

    def get_absolute_position(self):
        return self._absolute_position

    def update_relative_position(self, position: Rect):
        self._relative_position = position

    def update_absolute_position(self, position: Rect):
        self._absolute_position = position
