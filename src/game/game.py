# Global Imports
import pygame
import sys

# Local Imports
from game.logic.core.config import WIDTH, HEIGHT, FPS, TITLE, TILE_SIZE, COLORS
from game.logic.core.gameplay_config import TREE_REWARD_ITEM, TREE_REWARD_AMOUNT, SPAWN_PROTECTION_RANGE
from game.logic.core.update import *
from game.logic.entities.player import Player
from game.logic.entities.mob_manager import MobManager
from game.logic.world.world import World
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
    world_width, world_height = 50, 50
    spawn_tile_x = world_width // 2
    spawn_tile_y = world_height // 2
    world = World(world_width, world_height, spawn_protection_center=(spawn_tile_x, spawn_tile_y), spawn_protection_range=SPAWN_PROTECTION_RANGE)
    player = Player(spawn_tile_x * TILE_SIZE, spawn_tile_y * TILE_SIZE)
    mob_manager = MobManager(world, player)

    # Add some test items to inventory
    player.inventory.add_item("stone", 10)
    player.inventory.add_item("wood", 5)
    player.inventory.add_item("copper", 3)

    # Game State
    running = True
    mouse_down = False
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

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
                if event.button == 3:
                    if player.inventory.is_inventory_open():
                        inventory_slot = get_inventory_slot_at(event.pos, player, WIDTH, HEIGHT)
                        if inventory_slot is not None:
                            player.eat_slot(inventory_slot)
                        else:
                            player.eat_selected()
                    else:
                        player.eat_selected()
                elif event.button == 1:
                    if player.inventory.is_inventory_open():
                        slot_index = get_inventory_slot_at(event.pos, player, WIDTH, HEIGHT)
                        if slot_index is not None:
                            if player.inventory.held_item is None:
                                player.inventory.pick_up(slot_index)
                            else:
                                player.inventory.place_item(slot_index)
                    else:
                        hotbar_index = get_hotbar_slot_at(event.pos, player, WIDTH, HEIGHT)
                        if hotbar_index is not None:
                            player.inventory.select_slot(hotbar_index)
                        else:
                            hover_mob = get_mob_under_cursor(mob_manager.get_mobs(), camera_x, camera_y, event.pos)
                            if hover_mob and player.can_attack(hover_mob):
                                player.attack(hover_mob)
                            else:
                                hover_tree = get_tree_under_cursor(world, camera_x, camera_y, event.pos)
                                if hover_tree and player.can_break_tree(hover_tree) and player.inventory.can_add_item(TREE_REWARD_ITEM, TREE_REWARD_AMOUNT):
                                    player.break_target = hover_tree
                                    player.is_breaking = True
                                else:
                                    player.reset_break()
                    mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.reset_break()
                    mouse_down = False

        # Update game state, including player movement and camera positioning
        # --- UPDATE ---
        camera_x, camera_y, delta = update(player, world, clock, FPS, WIDTH, HEIGHT)
        mob_manager.update(delta)

        mouse_pos = pygame.mouse.get_pos()
        hovered_tree = get_tree_under_cursor(world, camera_x, camera_y, mouse_pos)

        if player.is_breaking and player.break_target is not None:
            if not mouse_down or hovered_tree != player.break_target or not player.can_break_tree(player.break_target) or not player.inventory.can_add_item(TREE_REWARD_ITEM, TREE_REWARD_AMOUNT):
                player.reset_break()
            else:
                player.break_progress += delta
                if player.break_progress >= player.break_duration:
                    if player.inventory.add_item(TREE_REWARD_ITEM, TREE_REWARD_AMOUNT):
                        world.remove_tree(player.break_target)
                    player.reset_break()

        # Render the game world and entities to the screen
        # --- RENDERER ---
        screen.fill((30, 30, 30)) # Background will be removed when world is endless

        # Draw World
        render_world(world, screen, COLORS, TILE_SIZE, camera_x, camera_y)

        # Draw world hover selector
        hovered_tree = render_world_selector(screen, world, camera_x, camera_y, mouse_pos, player, WIDTH, HEIGHT, mob_manager.get_mobs())

        # Draw mobs
        render_mobs(mob_manager.get_mobs(), screen, TILE_SIZE, camera_x, camera_y)

        # Draw Player
        render_player(player, screen, TILE_SIZE, camera_x, camera_y)

        # Draw tree breaking progress
        render_break_progress(player, screen, camera_x, camera_y)

        # Draw UI
        render_ui(player, screen, WIDTH, HEIGHT, mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
