import pygame

from game.logic.entities.player import *

def update(player: Player, clock: pygame.time.Clock, FPS: int, WIDTH: int, HEIGHT: int) -> tuple[float, float]:
    # Calculate time elapsed since last frame for smooth movement
    delta = clock.tick(FPS) / 1000

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

    # Center camera on player
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    return camera_x, camera_y, delta