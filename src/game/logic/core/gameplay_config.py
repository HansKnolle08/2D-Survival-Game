# Gameplay tuning values and defaults

# Spawn protection zone around the player
SPAWN_PROTECTION_RANGE = 3

# Breaking properties
BREAK_DURATION = 1.0
BREAK_RANGE = 3

# Tree properties
TREE_SIZE = 3
TREE_HEALTH = 5
TREE_REWARD_ITEM = "wood"
TREE_REWARD_AMOUNT = 4

# Inventory layout and stacking
HOTBAR_SIZE = 9
INVENTORY_ROWS = 3
INVENTORY_COLS = 9
STACK_LIMIT = 64

# Interaction ranges
INTERACTION_RANGE = 3
BREAK_RANGE: int = INTERACTION_RANGE

# Movement and hunger
PLAYER_BASE_SPEED = 200
RUN_MULTIPLIER = 1.6
MAX_HUNGER = 20
HUNGER_DECAY_IDLE = 0.005
HUNGER_DECAY_WALK = 0.05
HUNGER_DECAY_RUN = 0.15

# Food values
HAM_HUNGER_RESTORE = 8
HAM_HEALTH_RESTORE = 0

# Attack properties
ATTACK_DAMAGE = 7
ATTACK_COOLDOWN = 0.3

# Loot properties
SHEEP_LOOT_ITEM = "ham"
SHEEP_LOOT_AMOUNT_MIN = 1
SHEEP_LOOT_AMOUNT_MAX = 3

# Mob spawn configuration per species
MOB_SPAWN_SETTINGS = {
    "sheep": {
        "max_count": 4,
        "spawn_interval": 8.0,
        "spawn_attempts": 20,
    },
    # Add future mob settings here, e.g.:
    # "cow": {"max_count": 6, "spawn_interval": 6.0, "spawn_attempts": 25},
}
