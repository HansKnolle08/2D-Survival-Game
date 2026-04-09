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

def render_food(food_items: list, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
    """
    Render food items as yellow squares.
    """
    for food in food_items:
        pygame.draw.rect(
            screen,
            (255, 255, 0),  # Yellow
            (
                food.x - camera_x,
                food.y - camera_y,
                food.size,
                food.size
            )
        )

def render_ui(player: Player, screen: pygame.Surface, WIDTH: int, HEIGHT: int) -> None:
    """
    Render health and hunger bars and hotbar at the bottom.
    """
    bar_width = 200
    bar_height = 20
    margin = 10
    font = pygame.font.SysFont(None, 24)

    # Health bar (red background, green fill)
    pygame.draw.rect(screen, (255, 0, 0), (margin, margin, bar_width, bar_height))
    health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, (0, 255, 0), (margin, margin, bar_width * health_ratio, bar_height))

    # Hunger bar (blue background, yellow fill)
    pygame.draw.rect(screen, (0, 0, 255), (margin, margin + bar_height + 5, bar_width, bar_height))
    hunger_ratio = player.hunger / player.max_hunger
    pygame.draw.rect(screen, (255, 255, 0), (margin, margin + bar_height + 5, bar_width * hunger_ratio, bar_height))

    # Hotbar and inventory grid sizing
    default_slot_size = 40
    if player.inventory.is_inventory_open():
        grid_rows = player.inventory.inventory_rows + 1
        max_width = WIDTH * 0.8
        max_height = HEIGHT * 0.7
        slot_size = int(min(max_width / player.inventory.inventory_cols, max_height / grid_rows))
        slot_size = max(40, min(slot_size, 80))
    else:
        slot_size = default_slot_size

    hotbar_y = HEIGHT - slot_size - 10
    hotbar_x_start = (WIDTH - slot_size * 9) // 2
    if not player.inventory.is_inventory_open():
        for i in range(9):
            x = hotbar_x_start + i * slot_size
            y = hotbar_y
            # Slot background
            color = (100, 100, 100) if i == player.inventory.selected_slot else (50, 50, 50)
            pygame.draw.rect(screen, color, (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, (200, 200, 200), (x, y, slot_size, slot_size), 2)  # Border
            # Item
            slot = player.inventory.slots[i]
            if slot:
                # For now, just text; later can add images
                text = f"{slot['item'][0].upper()}{slot['count']}"  # e.g., F5 for food 5
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (x + 5, y + 5))

    # Full inventory grid if open
    if player.inventory.is_inventory_open():
        grid_rows = player.inventory.inventory_rows + 1
        grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
        grid_y_start = (HEIGHT - slot_size * grid_rows) // 2
        for row in range(grid_rows):
            for col in range(player.inventory.inventory_cols):
                if row < player.inventory.inventory_rows:
                    slot_index = player.inventory.hotbar_size + row * player.inventory.inventory_cols + col
                else:
                    slot_index = col  # Hotbar in last row
                x = grid_x_start + col * slot_size
                y = grid_y_start + row * slot_size
                selected = slot_index == player.inventory.selected_slot and row == player.inventory.inventory_rows
                color = (100, 100, 100) if selected else (50, 50, 50)
                pygame.draw.rect(screen, color, (x, y, slot_size, slot_size))
                pygame.draw.rect(screen, (200, 200, 200), (x, y, slot_size, slot_size), 2)
                slot = player.inventory.slots[slot_index]
                if slot:
                    text = f"{slot['item'][0].upper()}{slot['count']}"
                    text_surface = font.render(text, True, (255, 255, 255))
                    screen.blit(text_surface, (x + 5, y + 5))
