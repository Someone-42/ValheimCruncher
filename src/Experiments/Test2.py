from Objects.Mob import Mob
from Objects.Modifiers import *
from Objects.Player import Player
from Objects.Weapon import Weapon
from Objects.Game import Roll

def run():
    p1 = Player("suu", 25, 5, 42, Modifiers(), { "knives" : 100 })
    skoll_and_hati = Weapon("skoll_and_hati", (DamageType.SLASH, DamageType.PIERCE), (45, 45), 1, 3, 2, 3, 1, 6, 10, 4, 24, "knives", 4)

    troll_mods = Modifiers()
    troll_mods.add_modifier(DamageType.PIERCE, Tenacity.WEAK)
    troll_mods.add_modifier(DamageType.BLUNT, Tenacity.RESISTANT)
    troll_mods.add_modifier(DamageType.SPIRIT, Tenacity.IMMUNE)
    troll = Mob("Troll", 600, 60, 0.3, troll_mods, 3)

    print(f"A sneak attack on `{troll.name}` (level: {troll.level}) using `{skoll_and_hati.name}` if rolling min will  do : {troll.get_percieved_damage(skoll_and_hati.get_weapon_attack(0, True, True), p1, roll_chance=Roll.MAX)} | (dmg, [...debuff dps...])") 