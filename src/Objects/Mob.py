from Objects.Modifiers import *
from Objects.Entity import Entity
from Objects.Game import Roll
class Mob(Entity):
    __slots__ = (
        "level"     # the amount of stars + 1 decorating the enemy, level 1 is 0 star, and so on
    )
    def __init__(self, name, hp, dmg, stagger_limit, modifiers = Modifiers(), level = 1):
        # Calculating multipliers from level
        dmg_m = ((level - 1) / 2 + 1)
        hp_m = level

        super().__init__(name, hp * hp_m, dmg * dmg_m, stagger_limit, modifiers)
        self.level = level

    def get_damage(self):
        return self.dmg

    def get_damage_per_tick(self, damage, damage_type):
        pass

    def get_percieved_damage(self, weapon_attack, player, attack_bonus = 1, targets = 1, roll_chance = Roll.AVERAGE):
        """ Returns damage taken by the enemy from a weapon attack by the player """
        # calculate stagger (When the enemy is staggered, we cannot add more stagger)
        staggered = self.stagger >= self.stagger_limit    # supposing the enemy doesn't take double damage on first stagger hit
        stagger_bonus = 2 if staggered else 1

        multitarget_penalty = 1 if targets == 1 else (4/(3 * targets))

        mul = stagger_bonus * attack_bonus * multitarget_penalty * player.get_damage_skill_factor(weapon_attack.skill, roll_chance) # Backstab is missing because calculated in the weapon_attack step

        tick_damage = []
        dmg = 0
        cdmg = 0
        for i in range(len(weapon_attack.listed_damages)):
            ld = weapon_attack.listed_damages[i]
            dmt = weapon_attack.listed_damages[i]
            cdmg = self.modifiers.get_multiplier(dmt) * ld
            if dmt != DamageType.LIGHTNING and dmt != DamageType.FROST and dmt & 0b111000 == 0b010000: # If damage type is per tick (elemental or pure)
                tick_damage.append(get_elemental_tick_debuff(dmt, cdmg))
                continue
            dmg += cdmg

        dmg *= mul

        # Calculate added stagger
        #if not staggered:
        #    self.stagger = max(self.stagger_limit, self.stagger + )
        
        return dmg, tick_damage