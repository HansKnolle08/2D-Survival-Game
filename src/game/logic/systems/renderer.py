import pygame

from game.logic.core.config import TILE_SIZE
from game.logic.entities.player import *
from game.logic.world.world import *

def get_slot_size(player: Player, WIDTH: int, HEIGHT: int) -> int:
    """Calculate slot size depending on whether the inventory is open."""
    if player.inventory.is_inventory_open():
        rows = player.inventory.inventory_rows + 1
        max_width = WIDTH * 0.8
        max_height = HEIGHT * 0.7
        size = int(min(max_width / player.inventory.inventory_cols, max_height / rows))
        return max(40, min(size, 80))
    return 40


def get_hotbar_slot_at(mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int) -> int | None:
    """Return the hotbar slot index at the mouse position, if any."""
    slot_size = get_slot_size(player, WIDTH, HEIGHT)
    if player.inventory.is_inventory_open():
        grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
        grid_y_start = (HEIGHT - slot_size * (player.inventory.inventory_rows + 1)) // 2
        hotbar_y = grid_y_start + player.inventory.inventory_rows * slot_size
    else:
        hotbar_y = HEIGHT - slot_size - 10
        grid_x_start = (WIDTH - slot_size * player.inventory.hotbar_size) // 2
    mx, my = mouse_pos
    if hotbar_y <= my < hotbar_y + slot_size:
        for i in range(player.inventory.hotbar_size):
            x = grid_x_start + i * slot_size
            if x <= mx < x + slot_size:
                return i
    return None


def get_inventory_slot_at(mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int) -> int | None:
    """Return the inventory slot index under the mouse when inventory is open."""
    if not player.inventory.is_inventory_open():
        return None
    slot_size = get_slot_size(player, WIDTH, HEIGHT)
    grid_rows = player.inventory.inventory_rows + 1
    grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
    grid_y_start = (HEIGHT - slot_size * grid_rows) // 2
    mx, my = mouse_pos
    if not (grid_x_start <= mx < grid_x_start + slot_size * player.inventory.inventory_cols and
            grid_y_start <= my < grid_y_start + slot_size * grid_rows):
        return None
    col = (mx - grid_x_start) // slot_size
    row = (my - grid_y_start) // slot_size
    if row < player.inventory.inventory_rows:
        return player.inventory.hotbar_size + int(row) * player.inventory.inventory_cols + int(col)
    return int(col)


def is_mouse_over_inventory(mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int) -> bool:
    """Check whether the mouse is over the open inventory UI."""
    return get_inventory_slot_at(mouse_pos, player, WIDTH, HEIGHT) is not None


def render_world_selector(screen: pygame.Surface, world: World, camera_x: int, camera_y: int, mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int) -> None:
    """Render a hovering selector over the world grid under the cursor."""
    if player.inventory.is_inventory_open() and is_mouse_over_inventory(mouse_pos, player, WIDTH, HEIGHT):
        return
    mx, my = mouse_pos
    world_x = camera_x + mx
    world_y = camera_y + my
    tile_x = int(world_x // TILE_SIZE)
    tile_y = int(world_y // TILE_SIZE)
    if 0 <= tile_x < world.width and 0 <= tile_y < world.height:
        rect = (
            tile_x * TILE_SIZE - camera_x,
            tile_y * TILE_SIZE - camera_y,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)


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

def render_ui(player: Player, screen: pygame.Surface, WIDTH: int, HEIGHT: int) -> None:
    """
    Render health bar and hotbar/inventory UI.
    """
    bar_width = 200
    bar_height = 20
    margin = 10
    slot_size = get_slot_size(player, WIDTH, HEIGHT)
    font_size = max(20, slot_size // 2)
    font = pygame.font.SysFont(None, font_size)

    # Health bar (red background, green fill)
    pygame.draw.rect(screen, (255, 0, 0), (margin, margin, bar_width, bar_height))
    health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, (0, 255, 0), (margin, margin, bar_width * health_ratio, bar_height))

    # Hotbar only when inventory is closed
    if not player.inventory.is_inventory_open():
        hotbar_y = HEIGHT - slot_size - 10
        hotbar_x_start = (WIDTH - slot_size * player.inventory.hotbar_size) // 2
        for i in range(player.inventory.hotbar_size):
            x = hotbar_x_start + i * slot_size
            y = hotbar_y
            color = (100, 100, 100) if i == player.inventory.selected_slot else (50, 50, 50)
            pygame.draw.rect(screen, color, (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, (200, 200, 200), (x, y, slot_size, slot_size), 2)
            slot = player.inventory.slots[i]
            if slot:
                text = f"{slot['item'][0].upper()}{slot['count']}"
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
                    slot_index = col
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
