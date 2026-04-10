from game.logic.systems.inventory import Inventory
from game.logic.core.config import TILE_SIZE
from game.logic.core.gameplay_config import BREAK_DURATION, BREAK_RANGE
from game.logic.world.objects.tree import Tree

class Player:
    """
    Represents the player entity with position, movement speed, health, and inventory.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # Pixels per second
        self.health = 100  # Max health
        self.max_health = 100
        self.inventory = Inventory()
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        self.break_target: Tree | None = None
        self.break_progress = 0.0
        self.break_duration = BREAK_DURATION
        self.break_range = BREAK_RANGE
        self.is_breaking = False

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    def get_center_tile(self) -> tuple[int, int]:
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        return int(center_x // TILE_SIZE), int(center_y // TILE_SIZE)

    def reset_break(self):
        self.break_target = None
        self.break_progress = 0.0
        self.is_breaking = False

    def can_break_tree(self, tree: Tree | None) -> bool:
        if tree is None:
            return False
        px, py = self.get_center_tile()
        tx, ty = tree.get_center_tile()
        distance = ((px - tx) ** 2 + (py - ty) ** 2) ** 0.5
        return distance <= self.break_range