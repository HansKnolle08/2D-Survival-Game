import pygame

from game.logic.entities.player import *
from game.logic.core.config import TILE_SIZE

def update(player: Player, clock: pygame.time.Clock, FPS: int, WIDTH: int, HEIGHT: int, food_items: list) -> tuple[float, float]:
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

    # Handle hotbar selection
    for i in range(9):
        if keys[pygame.K_1 + i]:
            player.inventory.select_slot(i)

    # Check collision with food items
    for food in food_items[:]:  # Copy list to allow removal
        if (player.x < food.x + food.size and
            player.x + TILE_SIZE // 2 > food.x and
            player.y < food.y + food.size and
            player.y + TILE_SIZE // 2 > food.y):
            player.hunger += food.hunger_restore
            if player.hunger > player.max_hunger:
                player.hunger = player.max_hunger
            food_items.remove(food)

    # Update hunger and health
    player.hunger -= 5 * delta  # Decrease hunger over time
    if player.hunger <= 0:
        player.hunger = 0
        player.health -= 2 * delta  # Decrease health if hunger is 0
        if player.health < 0:
            player.health = 0

    # Center camera on player
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    return camera_x, camera_y, delta