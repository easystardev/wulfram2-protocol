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
    # NOTE: Slot 4 is NOT control-quantized in network packets.
    # Decompile (`Game/Session/Network/Protocol.c` GUESS5_Proto_write_quantized_behavior)
    # shows slot 4 takes the non-quantized/raw path.
    WEAPON_SELECT = 4
    UPWARD_THRUST = 5    # Q/Z relative axis (encoded with zoom quantizer)
    SLOT6 = 6            # Unknown (control quantizer)
    SLOT7 = 7            # Unknown (control quantizer)
    FIRE = 8             # Primary fire trigger (binary)
    # Slots 9-21 are various other controls


# Shared slot classification for ACTION_DUMP/ACTION_UPDATE encoding.
# Keep these authoritative to avoid client/server bitstream drift.
ACTION_ANALOG_SLOTS = frozenset({
    BehaviorSlot.UNUSED0,
    BehaviorSlot.TURNING,
    BehaviorSlot.MOVING_FORWARD,
    BehaviorSlot.MOVING_SIDEWAYS,
    BehaviorSlot.UPWARD_THRUST,
    BehaviorSlot.SLOT6,
    BehaviorSlot.SLOT7,
})

# ACTION_DUMP writes UPWARD_THRUST with the zoom quantizer; this set is only
# the slots written with the control quantizer.
ACTION_DUMP_CONTROL_SLOTS = frozenset({
    BehaviorSlot.UNUSED0,
    BehaviorSlot.TURNING,
    BehaviorSlot.MOVING_FORWARD,
    BehaviorSlot.MOVING_SIDEWAYS,
    BehaviorSlot.SLOT6,
    BehaviorSlot.SLOT7,
})


def is_action_analog_slot(slot_idx: int) -> bool:
    """Return True when ACTION_UPDATE should encode this slot as analog."""
    return slot_idx in ACTION_ANALOG_SLOTS


def is_action_dump_control_slot(slot_idx: int) -> bool:
    """Return True when ACTION_DUMP should encode this slot with control quantizer."""
    return slot_idx in ACTION_DUMP_CONTROL_SLOTS


class EntityType(IntEnum):
    """Entity type IDs from decompile (Registry.c EntityType_savechar_to_internal).

    Types 0-4: Vehicles (player-controllable)
    Types 5-18: Projectiles/ordnance
    Types 19-21: Special items
    Types 22: Torpedo
    Types 25-37: Buildings/structures (map objects)
    Sentinel 0x27 (39) = ILLEGAL
    """
    # Vehicles
    TANK = 0               # save: 't'
    SCOUT = 1              # save: (vehicle, not in save func) — also called Medic
    ASSAULT_PLATFORM = 2
    BOMBER = 3
    TRANSPORT = 4

    # Projectiles
    FLAK_SHELL = 5         # save: 'A' — uses g_entity_physics_config_projectile
    PULSE_SHELL = 6        # save: 'U'
    SHORT_MISSILE = 7      # save: 'O'
    HUNTER = 8             # save: 'm' — uses g_entity_physics_config_projectile
    HEAVY_MISSILE = 9      # save: 'M'
    MINE = 10              # save: 'i'
    PIERCER = 11           # save: 'P'
    THUMPER = 12           # save: 'H'
    CALTROP = 13           # save: 'k'
    ORBITAL_BOMB = 14
    CRUISE_MISSILE = 15
    MORTAR_SHELL = 16
    FLARE = 17
    AERIAL_BOMB = 18

    # Special items
    CARGO_BOX = 19         # save: 'c'
    UPLINK = 20            # save: 'u'
    SUPPLY_SHIP = 21       # save: 'h'

    # Torpedo — uses g_entity_physics_config_torpedo
    TORPEDO = 22           # save: 'T' (0x16)

    # Types 23-24 unused/unknown

    # Buildings / structures
    ENERGY_BUILDING = 25   # save: 'e' (0x19)
    FUEL_BUILDING = 26     # save: 'f' (0x1a)
    REPAIR_BUILDING = 27   # save: 'r' (0x1b) — spawn points use this type
    SPECIAL_STRUCTURE = 28 # save: 'S' (0x1c)
    SENSOR_BUILDING = 29   # save: 's' (0x1d)
    GUN_TURRET = 30        # save: 'g' (0x1e)
    ENERGY_STRUCTURE = 31  # save: 'E' (0x1f)
    LAUNCHER = 32          # save: 'L' (0x20)
    PAD = 33               # save: 'p' (0x21)
    ORBITAL_BUILDING = 34  # save: 'o' (0x22)
    DARK_LIGHT = 35        # save: 'd' (0x23)
    BUILDING = 36          # save: 'b' (0x24)
    STRUCTURE = 37         # save: '*' (0x25)


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

# UPDATE_ARRAY / PLAYER_INFO local-state turret flags are keyed by the
# local-state weapon/entity type value, not by the currently selected ammo slot.
# `azurefishy-src` Replication.c reads:
# - primary turret angle when weapon type 0 has weapon_def+0x170 set
# - secondary turret angle when weapon type 1 has weapon_def+0x68 set
# Keep this shared so server builders and client decoders stay aligned.
LOCAL_STATE_PRIMARY_TURRET_WEAPON_TYPES = frozenset({0})
LOCAL_STATE_SECONDARY_TURRET_WEAPON_TYPES = frozenset({1})


@dataclass
class VehiclePhysicsConfig:
    """Per-vehicle-type physics constants from decompile (VehiclePhysics_init_*).

    Offsets reference the VehiclePhysicsConfig struct in the original binary.
    Static values are set in VehiclePhysics_init_tank / _init_medic etc.
    Runtime values (damping, mass) come from PhysicsConfig type_data, set
    during entity creation — NOT from the static init (which zeroes +0x54-0x78).
    """
    # Static config from VehiclePhysics_init_* (hex-confirmed)
    turn_adjust: float      # +0x10 — angular acceleration multiplier
    move_adjust: float      # +0x18 — forward acceleration multiplier
    strafe_adjust: float    # +0x20 — strafe acceleration multiplier
    max_velocity: float     # +0x28 — velocity clamp
    low_fuel_level: float   # +0x30 — fuel warning threshold
    max_altitude: float     # +0x38 — max hover height
    gravity_pct: float      # +0x40 — gravity multiplier (1.0 = normal)

    # Runtime physics (from PhysicsConfig type_data, NOT static init)
    # Accessed via entity+0xBC → PhysicsState → +4 → type_data → offset
    linear_damping_driving: float = 0.8   # ground_friction * terrain_scale (flat ground)
    linear_damping_coasting: float = 2.0  # hardcoded at Vehicles.c:932
    angular_damping: float = 2.0          # type_data+0x7C (set at runtime, zeroed in static init)
    mass: float = 1.0                     # type_data+0x80


def tank_low_speed_mobility_factor(current_speed: float, speed_threshold: float) -> float:
    """Return the decompile-backed tank forward-mobility cap from current speed.

    `azurefishy-src` `Tank_compute_mobility_factors` applies:
      factor = (current_speed / speed_threshold) * 0.6 + 0.4
    when speed is below the threshold, otherwise 1.0.

    The original field is still named `low_fuel_level` in recovered debug vars,
    but the controller uses it as a speed-domain mobility cap.
    """
    if speed_threshold <= 0.0:
        return 1.0
    if current_speed < 0.0:
        current_speed = 0.0
    if current_speed < speed_threshold:
        factor = (current_speed / speed_threshold) * 0.6 + 0.4
        if factor < 0.4:
            return 0.4
        if factor > 1.0:
            return 1.0
        return factor
    return 1.0


# Per-vehicle-type configs from decompile hex literals (Registry.c)
VEHICLE_PHYSICS_CONFIGS = {
    EntityType.TANK: VehiclePhysicsConfig(
        turn_adjust=4.5,        # +0x10
        move_adjust=85.0,       # +0x18
        strafe_adjust=69.7,     # +0x20
        max_velocity=80.0,      # +0x28
        low_fuel_level=2000.0,  # +0x30
        max_altitude=3.25,      # +0x38
        gravity_pct=1.0,        # +0x40
    ),
    EntityType.SCOUT: VehiclePhysicsConfig(
        turn_adjust=4.5,        # +0x10 — same as tank
        move_adjust=85.0,       # +0x18 — same as tank
        strafe_adjust=38.0,     # +0x20 — lower than tank (69.7)
        max_velocity=72.0,      # +0x28 — different semantics
        low_fuel_level=2000.0,  # +0x38 — offset shifted in medic struct
        max_altitude=4.9,       # +0x40 — higher than tank (3.25)
        gravity_pct=1.0,        # +0x50
    ),
}


class EntityPhysicsMode(IntEnum):
    """Physics config modes from decompile globals.

    Three global configs exist: default (most entities), projectile (FlakShell,
    Hunter), torpedo. The mode determines integration behavior, damping flags,
    and collision response.
    """
    DEFAULT = 0       # g_entity_physics_config_default — standard entities
    PROJECTILE = 1    # g_entity_physics_config_projectile — types 5 (FlakShell), 8 (Hunter)
    TORPEDO = 2       # g_entity_physics_config_torpedo — type 22 (Torpedo)


# Map entity types to their physics mode
ENTITY_PHYSICS_MODES = {
    EntityType.FLAK_SHELL: EntityPhysicsMode.PROJECTILE,
    EntityType.HUNTER: EntityPhysicsMode.PROJECTILE,
    EntityType.TORPEDO: EntityPhysicsMode.TORPEDO,
    # All other entity types use DEFAULT
}


def get_entity_physics_mode(entity_type: int) -> EntityPhysicsMode:
    """Get the physics mode for an entity type."""
    return ENTITY_PHYSICS_MODES.get(entity_type, EntityPhysicsMode.DEFAULT)


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
