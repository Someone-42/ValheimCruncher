from enum import IntEnum

class Roll(IntEnum):
    MIN = 0
    AVERAGE = 1
    MAX = 2

class Game:
    # Represents an approximation of a current time frame's game's state.
    # Used in the calculations of various scenarios
    __slots__ = (
        "player_count"
    )
    def __init__(self, player_count):
        self.player_count = player_count