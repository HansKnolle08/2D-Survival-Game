from game.logic.systems.inventory import Inventory
from game.logic.core.config import TILE_SIZE
from game.logic.core.gameplay_config import BREAK_DURATION, INTERACTION_RANGE, ATTACK_COOLDOWN, ATTACK_DAMAGE
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
        self.is_alive = True
        self.inventory = Inventory()
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE // 2
        self.break_target: Tree | None = None
        self.break_progress = 0.0
        self.break_duration = BREAK_DURATION
        self.interaction_range = INTERACTION_RANGE
        self.attack_cooldown = ATTACK_COOLDOWN
        self.attack_timer = 0.0
        self.is_breaking = False

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    def get_center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

    def get_center_tile(self) -> tuple[int, int]:
        center_x, center_y = self.get_center()
        return int(center_x // TILE_SIZE), int(center_y // TILE_SIZE)

    def reset_break(self):
        self.break_target = None
        self.break_progress = 0.0
        self.is_breaking = False

    def distance_in_tiles_to(self, target) -> float:
        tx, ty = target.get_center()
        px, py = self.get_center()
        return ((px - tx) ** 2 + (py - ty) ** 2) ** 0.5 / TILE_SIZE

    def can_interact_with(self, target) -> bool:
        if target is None:
            return False
        return self.distance_in_tiles_to(target) <= self.interaction_range

    def can_break_tree(self, tree: Tree | None) -> bool:
        return self.can_interact_with(tree)

    def can_attack(self, target) -> bool:
        return self.can_interact_with(target) and self.attack_timer <= 0 and target is not None and getattr(target, "is_alive", False)

    def attack(self, target) -> bool:
        if not self.can_attack(target):
            return False

        target.take_damage(ATTACK_DAMAGE, source=self)
        self.attack_timer = self.attack_cooldown
        if not target.is_alive:
            self._collect_loot_from(target)
        return True

    def _collect_loot_from(self, target) -> None:
        if not hasattr(target, "get_loot"):
            return
        for item_name, amount in target.get_loot():
            self.inventory.add_item(item_name, amount)

    def update(self, delta: float) -> None:
        if self.attack_timer > 0:
            self.attack_timer = max(0.0, self.attack_timer - delta)
