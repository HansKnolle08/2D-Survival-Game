"""
MIT License
Copyright (c) 2026 [HansKnolle08]

Definition of the base Entity and Mob classes.

src/game/logic/entities/entity.py
"""

# Global imports
import math
import random
import pygame

# Local imports
from game.logic.core.config import TILE_SIZE
from game.logic.world.objects.tree import Tree

# Entity and Mob classes
class Entity:
    """Base entity for any game object with position and health."""
    def __init__(self, x: float, y: float, width: int, height: int, health: int = 10, speed: float = 0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.speed = speed
        self.is_alive = True

    # Collision rectangle for this entity
    def get_rect(self) -> tuple[int, int, int, int]:
        return (int(self.x), int(self.y), self.width, self.height)

    # Center point for distance calculations
    def get_center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

    # Distance to another entity
    def distance_to(self, other: "Entity") -> float:
        dx = self.get_center()[0] - other.get_center()[0]
        dy = self.get_center()[1] - other.get_center()[1]
        return math.hypot(dx, dy)

    # Apply damage to this entity
    def take_damage(self, amount: int, source=None) -> None:
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    # Move the entity, checking for collisions with world boundaries and trees
    def move(self, dx: float, dy: float, world) -> None:
        target_x = self.x + dx
        target_y = self.y + dy
        rect = pygame.Rect(int(target_x), int(target_y), self.width, self.height)

        if target_x < 0 or target_y < 0:
            return
        if target_x + self.width > world.width * TILE_SIZE:
            return
        if target_y + self.height > world.height * TILE_SIZE:
            return

        for tree in world.trees:
            tree_rect = pygame.Rect(*tree.get_collision_rect())
            if rect.colliderect(tree_rect):
                return

        self.x = target_x
        self.y = target_y

# Mob class with simple wandering and fleeing behavior
class Mob(Entity):
    """Generic mob entity with simple wandering AI."""
    def __init__(self, x: float, y: float, width: int, height: int, health: int, speed: float):
        super().__init__(x, y, width, height, health, speed)
        self.state = "idle"
        self.direction = (0.0, 0.0)
        self.wander_timer = 0.0
        self.wander_interval = random.uniform(1.5, 3.0)
        self.pause_timer = 0.0
        self.threat_timer = 0.0
        self.threat_source = None
        self.threat_duration = 4.0
        self.damage_flash_duration = 0.2
        self.damage_timer = 0.0

    # Update mob behavior each frame
    def update(self, delta: float, world, player) -> None:
        if not self.is_alive:
            return
        self.damage_timer = max(0.0, self.damage_timer - delta)
        self.update_ai(delta, world, player)

    # Simple AI: flee from player if recently attacked, otherwise wander
    def update_ai(self, delta: float, world) -> None:
        if self.threat_timer > 0 and self.threat_source is not None and self.threat_source.is_alive:
            self.flee_from(self.threat_source, delta, world)
            self.threat_timer -= delta
            if self.threat_timer <= 0:
                self.threat_source = None
                self.state = "idle"
        else:
            self.wander(delta, world)

    # Override take_damage to trigger fleeing behavior
    def take_damage(self, amount: int, source=None) -> None:
        super().take_damage(amount)
        if source is not None:
            self.threat_source = source
            self.threat_timer = self.threat_duration
            self.state = "flee"
        self.damage_timer = self.damage_flash_duration

    # Flee away from a source entity
    def flee_from(self, source, delta: float, world) -> None:
        px, py = source.get_center()
        cx, cy = self.get_center()
        dx = cx - px
        dy = cy - py
        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 1.0, 0.0
        else:
            dx /= length
            dy /= length
        self.move(dx * self.speed * delta, dy * self.speed * delta, world)

    # Wander randomly when not threatened
    def wander(self, delta: float, world) -> None:
        if self.state == "paused":
            self.pause_timer -= delta
            if self.pause_timer <= 0:
                self.state = "idle"
                self.wander_timer = 0
            return

        self.wander_timer -= delta
        if self.wander_timer <= 0:
            if random.random() < 0.4:
                self.state = "paused"
                self.pause_timer = random.uniform(0.8, 2.0)
            else:
                self.state = "moving"
                angle = random.uniform(0, math.pi * 2)
                self.direction = (math.cos(angle), math.sin(angle))
                self.wander_timer = random.uniform(1.0, 2.5)

        if self.state == "moving":
            self.move(self.direction[0] * self.speed * delta, self.direction[1] * self.speed * delta, world)

    # Return dropped loot when this mob dies
    def get_loot(self) -> list[tuple[str, int]]:
        """Return dropped loot when this mob dies."""
        return []
