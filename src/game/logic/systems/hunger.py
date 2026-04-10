"""
MIT License
Copyright (c) 2026 [HansKnolle08]

System for managing player hunger and its decay over time.

src/game/logic/systems/hunger.py
"""

# Local imports
from game.logic.core.gameplay_config import HUNGER_DECAY_IDLE, HUNGER_DECAY_RUN, HUNGER_DECAY_WALK
from game.logic.entities.player import Player

# Update player hunger based on movement state and time delta.
def update_hunger(player: Player, delta: float, is_moving: bool, is_running: bool) -> None:
    """Update player hunger based on movement state."""
    if is_running:
        decay_rate: float = HUNGER_DECAY_RUN
    elif is_moving:
        decay_rate: float = HUNGER_DECAY_WALK
    else:
        decay_rate: float = HUNGER_DECAY_IDLE

    player.hunger = max(0.0, player.hunger - decay_rate * delta)
