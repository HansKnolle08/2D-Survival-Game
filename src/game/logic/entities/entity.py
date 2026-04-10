import math
import random
import pygame

from game.logic.core.config import TILE_SIZE
from game.logic.world.objects.tree import Tree

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

    def get_rect(self) -> tuple[int, int, int, int]:
        return (int(self.x), int(self.y), self.width, self.height)

    def get_center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

    def distance_to(self, other: "Entity") -> float:
        dx = self.get_center()[0] - other.get_center()[0]
        dy = self.get_center()[1] - other.get_center()[1]
        return math.hypot(dx, dy)

    def take_damage(self, amount: int, source=None) -> None:
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

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

    def update(self, delta: float, world, player) -> None:
        if not self.is_alive:
            return
        self.update_ai(delta, world, player)

    def update_ai(self, delta: float, world, player) -> None:
        if self.threat_timer > 0 and self.threat_source is not None and self.threat_source.is_alive:
            self.flee_from(self.threat_source, delta, world)
            self.threat_timer -= delta
            if self.threat_timer <= 0:
                self.threat_source = None
                self.state = "idle"
        else:
            self.wander(delta, world)

    def take_damage(self, amount: int, source=None) -> None:
        super().take_damage(amount)
        if source is not None:
            self.threat_source = source
            self.threat_timer = self.threat_duration
            self.state = "flee"

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

    def get_loot(self) -> list[tuple[str, int]]:
        """Return dropped loot when this mob dies."""
        return []
