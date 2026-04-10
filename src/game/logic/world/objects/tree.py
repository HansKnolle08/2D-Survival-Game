from game.logic.core.config import TILE_SIZE
from game.logic.core.gameplay_config import TREE_HEALTH, TREE_SIZE

class Tree:
    """
    Represents a large tree object occupying multiple tiles.
    """
    size = TREE_SIZE

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = TREE_HEALTH
        self.max_health = TREE_HEALTH
        self.type = "tree"

    def occupied_tiles(self) -> list[tuple[int, int]]:
        """Return all tile coordinates covered by this tree."""
        return [
            (self.x + dx, self.y + dy)
            for dy in range(self.size)
            for dx in range(self.size)
        ]

    def is_at(self, x: int, y: int) -> bool:
        """Check whether this tree occupies the specified tile."""
        return self.x <= x < self.x + self.size and self.y <= y < self.y + self.size

    def get_draw_rect(self) -> tuple[int, int, int, int]:
        """Return the full tile-area rectangle used for rendering the tree."""
        return (
            self.x * TILE_SIZE,
            self.y * TILE_SIZE,
            self.size * TILE_SIZE,
            self.size * TILE_SIZE,
        )

    def get_collision_rect(self) -> tuple[int, int, int, int]:
        """Return a tighter collision rectangle around the visible tree canopy."""
        offset = TILE_SIZE // 2
        return (
            self.x * TILE_SIZE + offset,
            self.y * TILE_SIZE + offset,
            TILE_SIZE * 2,
            TILE_SIZE * 2,
        )

    def get_center(self) -> tuple[float, float]:
        rect = self.get_draw_rect()
        return (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)

    def get_center_tile(self) -> tuple[float, float]:
        """Return the floating center tile coordinates for range checks."""
        return self.x + self.size / 2.0, self.y + self.size / 2.0

    def hit(self, damage: int = 1) -> bool:
        """Deal damage to the tree and return True if it is destroyed."""
        self.health -= damage
        return self.health <= 0

    def get_position(self) -> tuple[int, int]:
        """Return the tree position as (x, y)."""
        return self.x, self.y
