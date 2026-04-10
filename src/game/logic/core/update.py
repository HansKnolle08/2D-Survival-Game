import pygame

from game.logic.entities.player import *
from game.logic.world.world import World

def update(player: Player, world: World, clock: pygame.time.Clock, FPS: int, WIDTH: int, HEIGHT: int) -> tuple[float, float, float]:
    # Calculate time elapsed since last frame for smooth movement
    delta = clock.tick(FPS) / 1000
    old_x = player.x
    old_y = player.y

    # Handle player input for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= player.speed * delta
    if keys[pygame.K_s]:
        player.y += player.speed * delta
    if keys[pygame.K_a]:
        player.x -= player.speed * delta
    if keys[pygame.K_d]:
        player.x += player.speed * delta

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

    player.update(delta)

    # Center camera on player
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    return camera_x, camera_y, delta