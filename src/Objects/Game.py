class Game:
    # Represents an approximation of a current time frame's game's state.
    # Used in the calculations of various scenarios
    __slots__ = (
        "player_count"
    )
    def __init__(self, player_count):
        self.player_count = player_count