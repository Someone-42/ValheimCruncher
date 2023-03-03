from Objects.Entity import Entity
from Objects.Modifiers import *
from Objects.Game import Roll


class Player(Entity):
    __slots__=("skills")
    def __init__(self, name, hp, dmg, stagger_limit, modifiers = Modifiers(), skills = {}):
        self.skills = skills
        # dmg stands for unarmed damage
        super().__init__(name, hp, dmg, stagger_limit, modifiers)

    def get_skill_level(self, skill_name):
        return self.skills[skill_name] if skill_name in self.skills else 0
    
    def get_damage_skill_factor(self, skill_name, roll = Roll.AVERAGE):
        """ Returns the associated """
        # We get current skill level associated to `skill_name`
        level = self.get_skill_level(skill_name)
        if roll == Roll.AVERAGE:
            # We get both highest and lowest rolls for damage and determine average
            return (self.get_max_skill_factor(level) + self.get_min_skill_factor(level)) / 2
        elif roll == Roll.MAX:
            return self.get_max_skill_factor(level)
        else:
            return self.get_min_skill_factor(level)

    def get_max_skill_factor(self, skill_level):
        # Highest roll is 0.55
        return min(0.55 + 0.006 * skill_level, 1)

    def get_min_skill_factor(self, skill_level):
        # Highest roll is 0.25
        return min(0.25 + 0.006 * skill_level, 1)
        