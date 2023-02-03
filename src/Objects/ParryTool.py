
class ParryTool:
    """ Describes an object capable of parrying and blocking """
    __slots__ = (
        "parry_force",
        "parry_armor",
        "parry_bonus"
    )
    def __init__(self, parry_force, parry_bonus, parry_armor):
        self.parry_armor = parry_armor
        self.parry_bonus = parry_bonus
        self.parry_force = parry_force
