from utils.enums import TilesType


class Tile:
    def __init__(self, type: TilesType, number: int):
        self.type = type
        self.number = number
        self.hidden = True

    def click(self):
        if self.hidden:
            return

        print(self.type, self.numbder)
