from enum import Flag, auto, IntEnum
import math

class DamageType(IntEnum):
    # Using binary numbers : 3 first digits determine ID (y), 3 following digits determine category (x) : 0bxxxyyy
    # Pure damage is 0
    PURE = 0

    # Physical damage : 1
    BLUNT  = 0b001000
    PIERCE = 0b001001
    SLASH  = 0b001010

    # Elemental damage : 2
    FIRE      = 0b010000
    POISON    = 0b010001
    SPIRIT    = 0b010010
    LIGHTNING = 0b010011
    FROST     = 0b010100

    # Terrain damage : 3 (doesn't apply to player)
    CHOP    = 0b011000
    PICKAXE = 0b011001


class Tenacity(IntEnum):
    # Refering to tenacity from ingame wiki ('tenacity [0, 4]' then 'immune')
    VERY_WEAK = 0
    WEAK = 1
    NEUTRAL = 2
    RESISTANT = 3
    VERY_RESISTANT = 4
    IMMUNE = 5

# Lookup table for tenacity damage multipliers
TENACITY_MULTIPLIER_LOOKUP = [2, 1.5, 1, 0.5, 0.25, 0]

class Modifiers:
    __slots__ = ("modifiers")
    def __init__(self):
        self.modifiers = {}

    def add_modifier(self, damage_type : int, tenacity : int) -> None:
        self.modifiers[damage_type] = tenacity

    def get_tenacity_name(self, damage_type):
        tenacity = 2
        if damage_type in self.modifiers:
            tenacity = self.modifiers[damage_type]
        return Tenacity(tenacity).name

    def get_multiplier(self, damage_type : int):
        if damage_type in self.modifiers:
            return TENACITY_MULTIPLIER_LOOKUP[self.modifiers[damage_type]]
        return 1

__SQRT_5 = math.sqrt(5)

def get_elemental_tick_debuff(damage_type, damage, player_is_attacked=False):
    """ Returns a tuple with DPS and duration """
    # NOTE : 1 tick is one second
    if damage_type == DamageType.POISON:
        x = __SQRT_5 if player_is_attacked else 1
        duration = int(1 + (x * math.sqrt(damage)))
        return (damage/duration, duration)
    if damage_type == DamageType.FIRE:
        # Poison and fire tick is once per second
        return (damage/5, 5)
    if damage_type == DamageType.SPIRIT: # NOTE : Spirit debuff stacks
        # Spirit ticks every .5 seconds, which means it does 2x more damage than described
        return (damage/3, 3)
    else:
        raise Exception(f"Damage type {damage_type} does not exist or does not have a tick damage implementation yet")

def stack_elemental_tick_debuff(damage_type, dps_duration_tuple1, dd1_expired, dps_duration_tuple2):
    """ Returns a new DPS, Duration tuple obtained by stacking every elemental damages """
    if damage_type == DamageType.SPIRIT:    # Only spirit debuff stacks
        # From my own testing, duration is reset, and leftover tick damage is added in the total damage, therefore dmg/tick has to be recalculated
        # NOTE: Spirit tick is 1/2 a second
        dps1, d1 = dps_duration_tuple1
        dps2, d2 = dps_duration_tuple2
        dr = d1 / d2 # duration ratio -> There are 6 ticks, we get the remaining amount of ticks divided by total
        # This ratio is then used to calculate how much is left to be applied per tick to reach dps1 * d1 damage
        return (dps1 * dr + dps2, d2)
    dps1, d1 = dps_duration_tuple1
    dps2, d2 = dps_duration_tuple2
    return (max(dps1, dps2), max(d1, d2))