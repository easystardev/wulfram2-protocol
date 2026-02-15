"""
Entity type definitions, weapon enums, and behavior slot indices.
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Tuple


class BehaviorSlot(IntEnum):
    """Behavior slot indices for input axes.

    These are INPUT behavior slots (0-21), not weapon/ammo slots.
    Used in ACTION_DUMP (0x09) and ACTION_UPDATE (0x0A) packets.
    """
    UNUSED0 = 0
    TURNING = 1          # yaw (left/right)
    MOVING_FORWARD = 2   # W/S
    MOVING_SIDEWAYS = 3  # A/D
    WEAPON_SELECT = 4    # Current weapon slot (5-bit quantized)
    UPWARD_THRUST = 5    # Q/Z relative axis (encoded with zoom quantizer)
    SLOT6 = 6            # Unknown (control quantizer)
    SLOT7 = 7            # Unknown (control quantizer)
    FIRE = 8             # Primary fire trigger (binary)
    # Slots 9-21 are various other controls


class EntityType(IntEnum):
    """Entity type IDs from entity_info.c"""
    TANK = 0
    SCOUT = 1
    ASSAULT_PLATFORM = 2
    BOMBER = 3
    TRANSPORT = 4
    FLAK_SHELL = 5
    PULSE_SHELL = 6
    SHORT_MISSILE = 7
    HUNTER = 8
    HEAVY_MISSILE = 9
    MINE = 10
    PIERCER = 11
    THUMPER = 12
    CALTROP = 13
    ORBITAL_BOMB = 14
    CRUISE_MISSILE = 15
    MORTAR_SHELL = 16
    FLARE = 17
    AEREAL_BOMB = 18
    CARGO_BOX = 19
    UPLINK = 20
    SUPPLY_SHIP = 21


class WeaponType(IntEnum):
    """Weapon types (ammo slot indices from decompilation).

    Tank weapon slots from GUESS4_WeaponDef_init_by_entity_type:
    - Slot 0: Chain gun (instant hit)
    - Slot 4: Pulse cannon (projectile)
    - Slot 5: Flak
    - Slot 6: Guided missile
    - Slot 7: Hunter seeker
    - Slot 8: Mine
    - Slot 9: Thumper
    - Slot 10: Mortar
    - Slot 11: Piercer
    """
    CHAIN_GUN = 0       # Instant hit
    PULSE_CANNON = 4    # Energy projectile
    FLAK = 5            # Anti-air
    GUIDED_MISSILE = 6  # Lock-on missile
    HUNTER_SEEKER = 7   # Autonomous missile
    MINE = 8            # Deployable mine
    THUMPER = 9         # Heavy artillery
    MORTAR = 10         # Arc projectile
    PIERCER = 11        # Long-range sniper


# Weapon names for UI/logging
WEAPON_NAMES = {
    0: "Chain Gun",
    4: "Pulse Cannon",
    5: "Flak",
    6: "Guided Missile",
    7: "Hunter Seeker",
    8: "Mine",
    9: "Thumper",
    10: "Mortar",
    11: "Piercer",
}

# Valid Tank weapon slots
TANK_WEAPON_SLOTS = {0, 4, 5, 6, 7, 8, 9, 10, 11}


@dataclass
class Projectile:
    """Represents an in-flight projectile."""
    entity_id: int
    entity_type: EntityType
    owner_id: int
    team: int
    pos: Tuple[float, float, float]
    vel: Tuple[float, float, float]
    spawn_time: float
    lifetime: float = 5.0  # seconds before despawn
    debug_context: Optional[dict] = None
