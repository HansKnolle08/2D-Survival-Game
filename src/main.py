# Global Imports
import pygame
import sys

# Local Imports
from game.logic.core.config import WIDTH, HEIGHT, FPS, TITLE, TILE_SIZE, COLORS
from game.logic.core.update import *
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

    # Game State
    running = True

    # Game Loop
    while running:
        # Handle user input and system events
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Update game state, including player movement and camera positioning
        # --- UPDATE ---
        camera_x, camera_y, delta = update(player, clock, FPS, WIDTH, HEIGHT)

        # Render the game world and entities to the screen
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
