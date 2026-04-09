import pygame

from game.logic.entities.player import *
from game.logic.world.world import *

def render_player(player: Player, screen: pygame.Surface, TILE_SIZE: int, camera_x: int, camera_y: int) -> None:
    """
    Render the player as a red rectangle on the screen, adjusted for camera position.
    """
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

def render_world(world: World, screen: pygame.Surface, COLORS: dict, TILE_SIZE: int, camera_x: int, camera_y: int) -> None:
    """
    Render the world tiles on the screen, adjusted for camera position.
    """
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
