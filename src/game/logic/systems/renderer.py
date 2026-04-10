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
    mx, my = mouse_pos
    if player.inventory.is_inventory_open():
        grid_rows = player.inventory.inventory_rows + 1
        row_gap = slot_size // 2
        grid_height = slot_size * grid_rows + row_gap
        grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
        grid_y_start = (HEIGHT - grid_height) // 2
        hotbar_y = grid_y_start + player.inventory.inventory_rows * slot_size + row_gap
        if not (grid_x_start <= mx < grid_x_start + slot_size * player.inventory.inventory_cols):
            return None
    else:
        hotbar_y = HEIGHT - slot_size - 10
        grid_x_start = (WIDTH - slot_size * player.inventory.hotbar_size) // 2
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
    row_gap = slot_size // 2
    grid_rows = player.inventory.inventory_rows + 1
    grid_height = slot_size * grid_rows + row_gap
    grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
    grid_y_start = (HEIGHT - grid_height) // 2
    mx, my = mouse_pos
    if mx < grid_x_start or mx >= grid_x_start + slot_size * player.inventory.inventory_cols:
        return None
    inventory_height = player.inventory.inventory_rows * slot_size
    if my < grid_y_start or my >= grid_y_start + grid_height:
        return None
    if my < grid_y_start + inventory_height:
        col = int((mx - grid_x_start) // slot_size)
        row = int((my - grid_y_start) // slot_size)
        return player.inventory.hotbar_size + row * player.inventory.inventory_cols + col
    if my < grid_y_start + inventory_height + row_gap:
        return None
    col = int((mx - grid_x_start) // slot_size)
    return col


def is_mouse_over_inventory(mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int) -> bool:
    """Check whether the mouse is over the open inventory UI."""
    return get_inventory_slot_at(mouse_pos, player, WIDTH, HEIGHT) is not None


def get_tree_under_cursor(world: World, camera_x: int, camera_y: int, mouse_pos: tuple[int, int]) -> Tree | None:
    """Return the tree under the cursor, if any."""
    mx, my = mouse_pos
    world_x = camera_x + mx
    world_y = camera_y + my
    tile_x = int(world_x // TILE_SIZE)
    tile_y = int(world_y // TILE_SIZE)
    if 0 <= tile_x < world.width and 0 <= tile_y < world.height:
        return world.get_tree_at(tile_x, tile_y)
    return None


def get_mob_under_cursor(mobs: list, camera_x: int, camera_y: int, mouse_pos: tuple[int, int]):
    """Return the mob under the cursor, if any."""
    mx, my = mouse_pos
    world_x = camera_x + mx
    world_y = camera_y + my
    for mob in mobs:
        if not getattr(mob, "is_alive", False):
            continue
        rect = mob.get_rect()
        if rect[0] <= world_x <= rect[0] + rect[2] and rect[1] <= world_y <= rect[1] + rect[3]:
            return mob
    return None


def render_world_selector(screen: pygame.Surface, world: World, camera_x: int, camera_y: int, mouse_pos: tuple[int, int], player: Player, WIDTH: int, HEIGHT: int, mobs: list | None = None):
    """Render a hovering selector over the world grid under the cursor."""
    if player.inventory.is_inventory_open() and is_mouse_over_inventory(mouse_pos, player, WIDTH, HEIGHT):
        return None

    hovered_tree = get_tree_under_cursor(world, camera_x, camera_y, mouse_pos)
    if hovered_tree is not None:
        collision_rect = hovered_tree.get_collision_rect()
        rect = pygame.Rect(
            collision_rect[0] - camera_x,
            collision_rect[1] - camera_y,
            collision_rect[2],
            collision_rect[3]
        )
        color = (255, 120, 0) if player.can_break_tree(hovered_tree) else (255, 220, 0)
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill((255, 120, 0, 40) if player.can_break_tree(hovered_tree) else (255, 220, 0, 40))
        screen.blit(overlay, (rect.x, rect.y))
        pygame.draw.rect(screen, color, rect, 4)
        return hovered_tree

    hovered_mob = None
    if mobs is not None:
        hovered_mob = get_mob_under_cursor(mobs, camera_x, camera_y, mouse_pos)
    if hovered_mob is not None:
        rect = pygame.Rect(
            hovered_mob.get_rect()[0] - camera_x,
            hovered_mob.get_rect()[1] - camera_y,
            hovered_mob.get_rect()[2],
            hovered_mob.get_rect()[3]
        )
        color = (255, 120, 0) if player.can_interact_with(hovered_mob) else (255, 220, 0)
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill((255, 120, 0, 40) if player.can_interact_with(hovered_mob) else (255, 220, 0, 40))
        screen.blit(overlay, (rect.x, rect.y))
        pygame.draw.rect(screen, color, rect, 4)
        return hovered_mob

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
    return None


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

    # Draw world objects like trees on top of tiles.
    for tree in world.trees:
        tree_rect = tree.get_draw_rect()
        screen_x = tree_rect[0] - camera_x
        screen_y = tree_rect[1] - camera_y
        canopy_center = (screen_x + tree_rect[2] // 2, screen_y + tree_rect[3] // 2)
        canopy_radius = TILE_SIZE

        pygame.draw.circle(screen, (30, 120, 30), canopy_center, canopy_radius)
        trunk_rect = pygame.Rect(
            screen_x + tree_rect[2] // 2 - 6,
            screen_y + tree_rect[3] - TILE_SIZE // 2,
            12,
            TILE_SIZE // 2,
        )
        pygame.draw.rect(screen, (100, 60, 20), trunk_rect)


def render_mobs(mobs: list, screen: pygame.Surface, TILE_SIZE: int, camera_x: int, camera_y: int) -> None:
    """Render all mobs on the screen."""
    for mob in mobs:
        if not mob.is_alive:
            continue
        mob_rect = mob.get_rect()
        screen_x = mob_rect[0] - camera_x
        screen_y = mob_rect[1] - camera_y
        pygame.draw.rect(screen, mob.color, (screen_x, screen_y, mob_rect[2], mob_rect[3]))
        if getattr(mob, "damage_timer", 0) > 0:
            flash_opacity = int(150 * min(mob.damage_timer / mob.damage_flash_duration, 1.0))
            overlay = pygame.Surface((mob_rect[2], mob_rect[3]), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, flash_opacity))
            screen.blit(overlay, (screen_x, screen_y))
        eye_radius = max(2, TILE_SIZE // 16)
        pygame.draw.circle(screen, mob.eye_color, (screen_x + mob_rect[2] // 3, screen_y + mob_rect[3] // 3), eye_radius)
        pygame.draw.circle(screen, mob.eye_color, (screen_x + 2 * mob_rect[2] // 3, screen_y + mob_rect[3] // 3), eye_radius)


def render_break_progress(player: Player, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
    if player.break_target is None or player.break_progress <= 0:
        return

    tree_rect = player.break_target.get_draw_rect()
    bar_width = tree_rect[2]
    bar_height = 10
    fill_ratio = min(player.break_progress / player.break_duration, 1.0)
    bar_x = tree_rect[0] - camera_x
    bar_y = tree_rect[1] - camera_y - bar_height - 5
    pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
    bar_color = (0, 180, 0) if player.inventory.can_add_item("wood", 4) else (180, 0, 0)
    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(bar_width * fill_ratio), bar_height))


def render_ui(player: Player, screen: pygame.Surface, WIDTH: int, HEIGHT: int, mouse_pos: tuple[int, int]) -> None:
    """
    Render health bar and hotbar/inventory UI.
    """
    bar_width = 200
    bar_height = 20
    margin = 10
    slot_size = get_slot_size(player, WIDTH, HEIGHT)
    font_size = max(20, slot_size // 2)
    font = pygame.font.SysFont(None, font_size)
    hovered_inventory_slot = get_inventory_slot_at(mouse_pos, player, WIDTH, HEIGHT) if player.inventory.is_inventory_open() else None

    # Health bar (red background, green fill)
    pygame.draw.rect(screen, (255, 0, 0), (margin, margin, bar_width, bar_height))
    health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, (0, 255, 0), (margin, margin, bar_width * health_ratio, bar_height))

    # Hunger bar (dark background, yellow fill)
    hunger_y = margin + bar_height + 6
    pygame.draw.rect(screen, (40, 40, 40), (margin, hunger_y, bar_width, bar_height))
    hunger_ratio = player.hunger / player.max_hunger
    pygame.draw.rect(screen, (220, 180, 40), (margin, hunger_y, bar_width * hunger_ratio, bar_height))

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
        row_gap = slot_size // 2
        grid_height = slot_size * grid_rows + row_gap
        grid_x_start = (WIDTH - slot_size * player.inventory.inventory_cols) // 2
        grid_y_start = (HEIGHT - grid_height) // 2
        for row in range(grid_rows):
            for col in range(player.inventory.inventory_cols):
                if row < player.inventory.inventory_rows:
                    slot_index = player.inventory.hotbar_size + row * player.inventory.inventory_cols + col
                else:
                    slot_index = col
                x = grid_x_start + col * slot_size
                y = grid_y_start + row * slot_size + (row_gap if row == player.inventory.inventory_rows else 0)
                selected = slot_index == player.inventory.selected_slot and row == player.inventory.inventory_rows
                hovered = slot_index == hovered_inventory_slot and row < player.inventory.inventory_rows
                if selected:
                    color = (120, 120, 120)
                elif hovered:
                    color = (140, 140, 180)
                else:
                    color = (50, 50, 50)
                pygame.draw.rect(screen, color, (x, y, slot_size, slot_size))
                pygame.draw.rect(screen, (200, 200, 200), (x, y, slot_size, slot_size), 2)
                slot = player.inventory.slots[slot_index]
                if slot:
                    text = f"{slot['item'][0].upper()}{slot['count']}"
                    text_surface = font.render(text, True, (255, 255, 255))
                    screen.blit(text_surface, (x + 5, y + 5))

    if player.inventory.held_item is not None:
        held_text = f"{player.inventory.held_item['item'][0].upper()}{player.inventory.held_item['count']}"
        text_surface = font.render(held_text, True, (255, 255, 255))
        mouse_x, mouse_y = mouse_pos
        screen.blit(text_surface, (mouse_x + 10, mouse_y + 10))
