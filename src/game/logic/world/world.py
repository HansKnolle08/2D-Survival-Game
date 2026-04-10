import random

from game.logic.core.gameplay_config import SPAWN_PROTECTION_RANGE
from game.logic.world.objects.tree import Tree

class World:
    """
    Represents the game world as a 2D grid of tiles.
    """
    def __init__(self, width, height, spawn_protection_center: tuple[int, int] | None = None,
                 spawn_protection_range: int = SPAWN_PROTECTION_RANGE):
        self.width = width
        self.height = height
        self.spawn_protection_center = spawn_protection_center
        self.spawn_protection_range = spawn_protection_range

        # Initialize 2D grid with default tile type
        self.tiles = [
            ["grass" for _ in range(width)]
            for _ in range(height)
        ]

        # World objects such as trees
        self.trees: list[Tree] = []
        self.spawn_trees()

    def spawn_trees(self, count: int | None = None):
        """Spawn a set of trees randomly during world creation."""
        if count is None:
            count = max(8, min(40, (self.width * self.height) // 40))

        tries = 0
        while len(self.trees) < count and tries < count * 10:
            x = random.randrange(0, self.width - Tree.size + 1)
            y = random.randrange(0, self.height - Tree.size + 1)
            if self.can_place_tree(x, y):
                self.trees.append(Tree(x, y))
            tries += 1

    def is_in_spawn_protection(self, x: int, y: int) -> bool:
        """Return whether a tile is inside the spawn protection zone."""
        if self.spawn_protection_center is None:
            return False

        center_x, center_y = self.spawn_protection_center
        half_range = self.spawn_protection_range // 2
        return (
            center_x - half_range <= x <= center_x + half_range and
            center_y - half_range <= y <= center_y + half_range
        )

    def can_place_tree(self, x: int, y: int) -> bool:
        """Return whether a tree can be placed at the requested location."""
        if x < 0 or y < 0 or x + Tree.size > self.width or y + Tree.size > self.height:
            return False

        for tile_x, tile_y in [(x + dx, y + dy) for dy in range(Tree.size) for dx in range(Tree.size)]:
            if self.get_tile(tile_x, tile_y) != "grass" or self.get_tree_at(tile_x, tile_y) is not None:
                return False
            if self.is_in_spawn_protection(tile_x, tile_y):
                return False
        return True

    def remove_tree(self, tree: Tree) -> None:
        """Remove a tree from the world."""
        if tree in self.trees:
            self.trees.remove(tree)

    def get_tree_at(self, x: int, y: int) -> Tree | None:
        """Return the tree at the given grid position, or None if there is no tree."""
        for tree in self.trees:
            if tree.is_at(x, y):
                return tree
        return None

    def get_tile(self, x, y):
        """
        Get the tile type at the specified coordinates.
        
        Args:
            x (int): X-coordinate
            y (int): Y-coordinate
            
        Returns:
            str: Tile type
        """
        return self.tiles[y][x]