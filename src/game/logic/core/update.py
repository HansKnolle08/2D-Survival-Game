"""
MIT License
Copyright (c) 2026 [HansKnolle08]

Update function that processes player input, updates the player's position, handles collisions,
and updates the player's hunger status. This function is called every frame in the main game loop.

src/game/logic/core/update.py
"""

# Global imports
import pygame

# Local imports
from game.logic.core.gameplay_config import RUN_MULTIPLIER
from game.logic.entities.player import *
from game.logic.systems.hunger import update_hunger
from game.logic.world.world import World

# Main update function
def update(player: Player, world: World, clock: pygame.time.Clock, FPS: int, WIDTH: int, HEIGHT: int) -> tuple[float, float, float]:
    # Calculate time elapsed since last frame for smooth movement
    delta = clock.tick(FPS) / 1000
    old_x = player.x
    old_y = player.y

    # Handle player input for movement
    keys = pygame.key.get_pressed()
    player.is_running = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
    player.speed = player.base_speed * (RUN_MULTIPLIER if player.is_running else 1.0)

    is_moving = False
    
    # Use WASD for movement, allowing diagonal movement when multiple keys are pressed
    if keys[pygame.K_w]:
        player.y -= player.speed * delta
        is_moving = True
    if keys[pygame.K_s]:
        player.y += player.speed * delta
        is_moving = True
    if keys[pygame.K_a]:
        player.x -= player.speed * delta
        is_moving = True
    if keys[pygame.K_d]:
        player.x += player.speed * delta
        is_moving = True

    # Handle hotbar selection
    for i in range(9):
        if keys[pygame.K_1 + i]:
            player.inventory.select_slot(i)

    # Collision with tree objects
    player_rect = pygame.Rect(*player.get_rect())
    for tree in world.trees:
        tree_rect = pygame.Rect(*tree.get_collision_rect())
        if player_rect.colliderect(tree_rect):
            player.x = old_x
            player.y = old_y
            break

    # Update player state and hunger
    player.update(delta)
    update_hunger(player, delta, is_moving, player.is_running)

    # Center camera on player
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    return camera_x, camera_y, delta