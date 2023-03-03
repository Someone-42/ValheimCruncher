from Objects.ParryTool import ParryTool
from dataclasses import dataclass
from Objects.Modifiers import *

@dataclass
class WeaponAttack:
    damage_types : list[DamageType]
    listed_damages : list[float]
    stagger_bonus : float
    skill : str

class Weapon(ParryTool):
    __slots__ = (
        "name",
        "damage_types",
        "listed_damages",
        "chain_attack",     # A number describing how many hits in the chain with the last one being the bonus blow, if 1 then there is no chain attack
        "chain_attack_bonus",        # a multiplier for how much more damage the last hit of the chain does
        "secondary_attack_bonus",        # 1 if no secondary attack, otherwise just uses 
        "stagger_bonus",                # 1 if no stagger bonus on weapon
        "secondary_stagger_bonus",       # 1 if no secondary attack stagger bonus
        "back_stab_bonus",
        "stagger_multiplier",
        "skill_name",
        "level"
    )
    def __init__(self, name, damage_types, listed_damages, stagger_bonus, chain_attack, chain_attack_bonus, secondary_attack_bonus, secondary_stagger_bonus, back_stab_bonus, block_force, parry_bonus, block_armor, skill_name, level):
        self.damage_types = damage_types
        self.name = name
        self.listed_damages = listed_damages
        super().__init__(block_force, parry_bonus, block_armor)
        self.chain_attack = chain_attack
        self.chain_attack_bonus = chain_attack_bonus
        self.secondary_attack_bonus = secondary_attack_bonus
        self.stagger_bonus = stagger_bonus
        self.back_stab_bonus = back_stab_bonus
        self.secondary_stagger_bonus = secondary_stagger_bonus
        self.skill_name = skill_name
        self.level = level

    def get_weapon_attack(self, chain_hit_count, back_stab=False, secondary=False):
        mul = 1
        smul = self.stagger_bonus
        if secondary:
            mul *= self.secondary_attack_bonus
            smul = self.secondary_stagger_bonus
        elif self.chain_attack > 1 and chain_hit_count % self.chain_attack == 0:
            mul *= self.chain_attack_bonus

        if back_stab:
            mul *= self.back_stab_bonus

        ldmg = [i * mul for i in self.listed_damages]
        return WeaponAttack(self.damage_types, ldmg, smul, self.skill_name)

        
        
