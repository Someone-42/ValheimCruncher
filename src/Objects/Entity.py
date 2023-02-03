from Modifiers import *

class Entity:
    """ An entity is a game object that can percieve damage posses resistance and or armors """
    __slots__ = (
        "name",
        "hp",
        "dmg",
        "modifiers",
        "stagger",
        "stagger_limit"
    )
    def __init__(self, name, hp, dmg, stagger_limit, modifiers = Modifiers()):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.modifiers = modifiers
        self.stagger_limit = stagger_limit

    def get_damage(self):
        raise NotImplementedError()