# Global Imports
import pygame
import sys
import random

# Local Imports
from game.logic.core.config import WIDTH, HEIGHT, FPS, TITLE, TILE_SIZE, COLORS
from game.logic.core.update import *
from game.logic.world.world import World
from game.logic.entities.player import Player
from game.logic.items.items import Food
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
    # Add some test items to inventory
    player.inventory.add_item("stone", 10)
    player.inventory.add_item("wood", 5)
    
    # Generate random food positions
    num_food = 10
    food_items = []
    for _ in range(num_food):
        x = random.randint(0, world.width * TILE_SIZE - TILE_SIZE)
        y = random.randint(0, world.height * TILE_SIZE - TILE_SIZE)
        food_items.append(Food(x, y))

    # Game State
    running = True

    # Game Loop
    while running:
        # Handle user input and system events
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player.inventory.toggle_inventory()
            
        # Update game state, including player movement and camera positioning
        # --- UPDATE ---
        camera_x, camera_y, delta = update(player, clock, FPS, WIDTH, HEIGHT, food_items)

        # Render the game world and entities to the screen
        # --- RENDERER ---
        screen.fill((30, 30, 30)) # Background will be removed when world is endless

        # Draw World
        render_world(world, screen, COLORS, TILE_SIZE, camera_x, camera_y)

        # Draw Food
        render_food(food_items, screen, camera_x, camera_y)

        # Draw Player
        render_player(player, screen, TILE_SIZE, camera_x, camera_y)

        # Draw UI
        render_ui(player, screen, WIDTH, HEIGHT)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Entry-Point
if __name__ == "__main__":
    main()
