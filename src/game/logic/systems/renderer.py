import pygame

def render_player(player, screen, TILE_SIZE, camera_x, camera_y):
    pygame.draw.rect(
        screen,
        (200, 50, 50),
        (
            player.x - camera_x,
            player.y - camera_y,
            TILE_SIZE // 2,
            TILE_SIZE // 2
        )
    )

def render_world(world, screen, COLORS, TILE_SIZE, camera_x, camera_y):
    for y in range(world.height):
        for x in range(world.width):
            tile = world.get_tile(x, y)
            color = COLORS[tile]

            screen_x = x * TILE_SIZE - camera_x
            screen_y = y * TILE_SIZE - camera_y

            rect = (
                screen_x,
                screen_y,
                TILE_SIZE,
                TILE_SIZE
            )

            pygame.draw.rect(screen, color, rect)