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
    # Add some test items to inventory
    player.inventory.add_item("stone", 10)
    player.inventory.add_item("wood", 5)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.inventory.is_inventory_open():
                        slot_index = get_inventory_slot_at(event.pos, player, WIDTH, HEIGHT)
                        if slot_index is not None:
                            if slot_index < player.inventory.hotbar_size:
                                player.inventory.select_slot(slot_index)
                            elif player.inventory.slots[slot_index]:
                                target_slot = player.inventory.selected_slot
                                target = player.inventory.slots[target_slot]
                                source = player.inventory.slots[slot_index]
                                if target is None:
                                    player.inventory.slots[target_slot] = source
                                    player.inventory.slots[slot_index] = None
                                elif target['item'] == source['item']:
                                    target['count'] += source['count']
                                    player.inventory.slots[slot_index] = None
                    else:
                        hotbar_index = get_hotbar_slot_at(event.pos, player, WIDTH, HEIGHT)
                        if hotbar_index is not None:
                            player.inventory.select_slot(hotbar_index)
            
        # Update game state, including player movement and camera positioning
        # --- UPDATE ---
        camera_x, camera_y, delta = update(player, clock, FPS, WIDTH, HEIGHT)

        mouse_pos = pygame.mouse.get_pos()

        # Render the game world and entities to the screen
        # --- RENDERER ---
        screen.fill((30, 30, 30)) # Background will be removed when world is endless

        # Draw World
        render_world(world, screen, COLORS, TILE_SIZE, camera_x, camera_y)

        # Draw world hover selector
        render_world_selector(screen, world, camera_x, camera_y, mouse_pos, player, WIDTH, HEIGHT)

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
