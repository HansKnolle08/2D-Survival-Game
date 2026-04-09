# Global Imports
import pygame
import sys

# Local Imports
from game.logic.core.config import WIDTH, HEIGHT, FPS, TITLE, TILE_SIZE, COLORS
from game.logic.world.world import World
from game.logic.entities.player import Player
from game.logic.systems.renderer import *

# Main Function
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
    dt = clock.tick(FPS) / 1000

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
            player.y -= player.speed * dt
        if keys[pygame.K_s]:
            player.y += player.speed * dt
        if keys[pygame.K_a]:
            player.x -= player.speed * dt
        if keys[pygame.K_d]:
            player.x += player.speed * dt

        camera_x = player.x - WIDTH // 2
        camera_y = player.y - HEIGHT // 2

        # --- RENDERER ---
        screen.fill((30, 30, 30)) # Background will be removed when world is endless

        # Draw World
        render_world(world, screen, COLORS, TILE_SIZE, camera_x, camera_y)

        # Draw Player
        render_player(player, screen, TILE_SIZE, camera_x, camera_y)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Entry-Point
if __name__ == "__main__":
    main()
