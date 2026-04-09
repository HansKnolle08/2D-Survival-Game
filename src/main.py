# Global Imports
import pygame
import sys

# Local Imports
from game.logic.core.config import WIDTH, HEIGHT, FPS, TITLE, TILE_SIZE, COLORS
from game.logic.world.world import World
from game.logic.entities.player import Player


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Create Window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # Initialize Game Systems
    world = World(50, 50)
    player = Player(100, 100)

    # Game State
    running = True

    # Game Loop
    while running:
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # --- UPDATE ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.y -= player.speed
        if keys[pygame.K_s]:
            player.y += player.speed
        if keys[pygame.K_a]:
            player.x -= player.speed
        if keys[pygame.K_d]:
            player.x += player.speed

        camera_x = player.x - WIDTH // 2
        camera_y = player.y - HEIGHT // 2

        # --- RENDERER ---
        screen.fill((30, 30, 30))

        # Draw World
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

        # Draw Player
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

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Entry-Point
if __name__ == "__main__":
    main()