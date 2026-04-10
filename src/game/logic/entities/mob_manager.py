import random

from game.logic.core.config import TILE_SIZE
from game.logic.core.gameplay_config import MOB_SPAWN_SETTINGS
from game.logic.entities.mobs.sheep import Sheep

class MobManager:
    """Manage a collection of mobs and update their behavior."""
    MOB_CLASSES = {
        "sheep": Sheep,
    }

    def __init__(self, world, player):
        self.world = world
        self.player = player
        self.mobs = []
        self.spawn_timers = {
            species: settings["spawn_interval"]
            for species, settings in MOB_SPAWN_SETTINGS.items()
        }
        self.spawn_initial_mobs()

    def spawn_initial_mobs(self) -> None:
        for species, settings in MOB_SPAWN_SETTINGS.items():
            for _ in range(settings["max_count"]):
                self.try_spawn_species(species)

    def spawn_mobs(self, species: str) -> bool:
        settings = MOB_SPAWN_SETTINGS[species]
        current = self.count_species(species)
        if current >= settings["max_count"]:
            return False
        return self.try_spawn_species(species)

    def try_spawn_species(self, species: str) -> bool:
        mob_class = self.MOB_CLASSES.get(species)
        if mob_class is None:
            return False

        settings = MOB_SPAWN_SETTINGS[species]
        tries = 0
        while tries < settings["spawn_attempts"]:
            tile_x = random.randrange(self.world.width)
            tile_y = random.randrange(self.world.height)
            if self.can_spawn_at(tile_x, tile_y):
                self.mobs.append(mob_class(tile_x * TILE_SIZE, tile_y * TILE_SIZE))
                return True
            tries += 1
        return False

    def count_species(self, species: str) -> int:
        return sum(1 for mob in self.mobs if getattr(mob, "species", None) == species)

    def can_spawn_at(self, tile_x: int, tile_y: int) -> bool:
        if self.world.is_in_spawn_protection(tile_x, tile_y):
            return False
        if self.world.get_tree_at(tile_x, tile_y) is not None:
            return False

        entity_rect = (tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        for mob in self.mobs:
            if self.rects_overlap(mob.get_rect(), entity_rect):
                return False

        player_rect = self.player.get_rect()
        if self.rects_overlap(player_rect, entity_rect):
            return False

        return True

    def rects_overlap(self, a, b) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def update(self, delta: float) -> None:
        self.spawn_timers = {
            species: timer - delta
            for species, timer in self.spawn_timers.items()
        }

        for species, timer in list(self.spawn_timers.items()):
            if timer <= 0:
                if self.spawn_mobs(species):
                    self.spawn_timers[species] = MOB_SPAWN_SETTINGS[species]["spawn_interval"]
                else:
                    self.spawn_timers[species] = MOB_SPAWN_SETTINGS[species]["spawn_interval"]

        for mob in self.mobs:
            mob.update(delta, self.world, self.player)

        self.mobs = [mob for mob in self.mobs if mob.is_alive]

    def get_mobs(self):
        return self.mobs
