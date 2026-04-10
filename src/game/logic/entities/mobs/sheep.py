import random

from game.logic.entities.entity import Mob
from game.logic.core.config import TILE_SIZE
from game.logic.core.gameplay_config import SHEEP_LOOT_ITEM, SHEEP_LOOT_AMOUNT_MIN, SHEEP_LOOT_AMOUNT_MAX

class Sheep(Mob):
    """Simple sheep mob with a small health pool and light movement."""
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, TILE_SIZE // 2, TILE_SIZE // 2, health=20, speed=80.0)
        self.species = "sheep"
        self.color = (240, 240, 240)
        self.eye_color = (40, 40, 40)

    def get_loot(self) -> list[tuple[str, int]]:
        return [(SHEEP_LOOT_ITEM, random.randint(SHEEP_LOOT_AMOUNT_MIN, SHEEP_LOOT_AMOUNT_MAX))]
