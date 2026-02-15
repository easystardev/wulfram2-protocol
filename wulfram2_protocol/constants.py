"""
Physics and protocol constants shared between server and client.

Sources:
- Decomp Physics.c / Vehicles.c (confirmed values marked)
- Server empirical tuning (marked where decomp disagrees)
"""

# ============ Tick / Timing ============

TICK_RATE_HZ = 30
TICK_DT = 1.0 / TICK_RATE_HZ  # ~0.0333s

# Physics substep limits (from decomp Physics.c)
SUBSTEP_DT_MAX = 0.04          # Physics substep ceiling
SUBSTEP_SPLIT_THRESHOLD = 0.08  # Split to half-step above this


# ============ Damping / Friction ============

# Angular velocity damping (from Physics_substep_integrate damped mode)
# entity->0xbc->+4->+0x7c  (DAT_005730cc+0x1C)
ANGULAR_DAMP_COEFF = 2.0

# Linear velocity damping
COASTING_DAMP = 2.0            # 0x40000000 at Vehicles.c:932 — no throttle
DRIVING_DAMP = 0.8             # empirical match — with throttle
# NOTE: Decomp shows DRIVING_FRICTION = 0.1 (0x3dcccccd at +0x74)
# but server uses 0.8 which matches actual client behavior.
# These may reference different things (friction vs damp).

# Softbody damping multiplier (TankController_update)
DAMPING_MULTIPLIER = 1.4137167  # entity+0x98


# ============ Position / Velocity Limits ============

VEC_POS_MAX = 8192.0           # Position quantizer max (±8192 world units)
STEADY_STATE_SPEED = 64.8      # u/s at full throttle with driving_damp=0.8


# ============ Gravity ============

GRAVITY_ACCEL = -50.0          # units/s² (server default)
GROUND_LEVEL = 5.0             # Default ground Z (before terrain heightmap)
TERRAIN_HEIGHT_OFFSET = 5.0    # Added to heightmap Z for entity position


# ============ Behavior Defaults ============
# From BEHAVIOR packet Section 6 (Active Vehicle Physics)

TANK_TURN_ADJUST = 4.25        # Calibrated: 0.00° heading error over 3s
TANK_MOVE_ADJUST = 85.0
TANK_STRAFE_ADJUST = 69.7
TANK_MAX_VELOCITY = 80.0
TANK_LOW_FUEL_LEVEL = 2000.0
TANK_MAX_ALTITUDE = 3.25
TANK_GRAVITY_PCT = 1.0
