from game.logic.core.gameplay_config import HOTBAR_SIZE, INVENTORY_ROWS, INVENTORY_COLS, STACK_LIMIT

class Inventory:
    """
    Inventory system with hotbar and main inventory.
    """
    def __init__(self):
        self.hotbar_size = HOTBAR_SIZE
        self.inventory_rows = INVENTORY_ROWS
        self.inventory_cols = INVENTORY_COLS
        self.main_inventory_size = self.inventory_rows * self.inventory_cols
        self.total_slots = self.hotbar_size + self.main_inventory_size
        self.slots = [None] * self.total_slots  # Each slot: {'item': str, 'count': int} or None
        self.selected_slot = 0  # Hotbar slot 0-8
        self.inventory_open = False
        self.held_item = None

    def toggle_inventory(self):
        """Toggle the inventory open/closed."""
        self.inventory_open = not self.inventory_open

    def add_item(self, item_name: str, amount: int = 1):
        """Add items to inventory, preferring hotbar first."""
        if not self.can_add_item(item_name, amount):
            return False

        amount_remaining = amount
        for i in range(self.hotbar_size):
            slot = self.slots[i]
            if slot and slot['item'] == item_name:
                capacity = STACK_LIMIT - slot['count']
                to_add = min(capacity, amount_remaining)
                if to_add > 0:
                    slot['count'] += to_add
                    amount_remaining -= to_add
                    if amount_remaining == 0:
                        return True
        for i in range(self.hotbar_size):
            if self.slots[i] is None:
                to_add = min(STACK_LIMIT, amount_remaining)
                self.slots[i] = {'item': item_name, 'count': to_add}
                amount_remaining -= to_add
                if amount_remaining == 0:
                    return True
        for i in range(self.hotbar_size, self.total_slots):
            slot = self.slots[i]
            if slot and slot['item'] == item_name:
                capacity = STACK_LIMIT - slot['count']
                to_add = min(capacity, amount_remaining)
                if to_add > 0:
                    slot['count'] += to_add
                    amount_remaining -= to_add
                    if amount_remaining == 0:
                        return True
        for i in range(self.hotbar_size, self.total_slots):
            if self.slots[i] is None:
                to_add = min(STACK_LIMIT, amount_remaining)
                self.slots[i] = {'item': item_name, 'count': to_add}
                amount_remaining -= to_add
                if amount_remaining == 0:
                    return True
        return False

    def _stack_item(self, item_name: str, amount: int, slot_range):
        """Stack items into existing matching slots."""
        for i in slot_range:
            slot = self.slots[i]
            if slot and slot['item'] == item_name:
                capacity = STACK_LIMIT - slot['count']
                if capacity >= amount:
                    slot['count'] += amount
                    return True
        return False

    def _empty_slot(self, item_name: str, amount: int, slot_range):
        """Place items into the first empty slot in a range."""
        for i in slot_range:
            if self.slots[i] is None:
                self.slots[i] = {'item': item_name, 'count': amount}
                return True
        return False

    def can_add_item(self, item_name: str, amount: int = 1):
        """Return True if the inventory can accept this item amount."""
        capacity = 0
        for i in range(self.hotbar_size):
            slot = self.slots[i]
            if slot is None:
                capacity += STACK_LIMIT
            elif slot['item'] == item_name:
                capacity += STACK_LIMIT - slot['count']
        for i in range(self.hotbar_size, self.total_slots):
            slot = self.slots[i]
            if slot is None:
                capacity += STACK_LIMIT
            elif slot['item'] == item_name:
                capacity += STACK_LIMIT - slot['count']
        return capacity >= amount

    def _can_stack(self, item_name: str, slot_range):
        for i in slot_range:
            slot = self.slots[i]
            if slot and slot['item'] == item_name:
                return slot['count'] < STACK_LIMIT
        return False

    def _can_empty(self, slot_range):
        for i in slot_range:
            if self.slots[i] is None:
                return True
        return False

    def pick_up(self, slot_index: int) -> bool:
        """Pick up an item stack from the given slot into the cursor."""
        if 0 <= slot_index < self.total_slots and self.slots[slot_index]:
            self.held_item = self.slots[slot_index]
            self.slots[slot_index] = None
            return True
        return False

    def place_item(self, slot_index: int) -> bool:
        """Place held item into the given slot, swapping or merging when needed."""
        if self.held_item is None or not (0 <= slot_index < self.total_slots):
            return False

        target = self.slots[slot_index]
        if target is None:
            self.slots[slot_index] = self.held_item
            self.held_item = None
            return True

        if target['item'] == self.held_item['item']:
            target['count'] += self.held_item['count']
            self.held_item = None
            return True

        self.slots[slot_index], self.held_item = self.held_item, self.slots[slot_index]
        return True

    def remove_item(self, slot_index: int, amount: int = 1):
        """Remove items from a specific slot."""
        if 0 <= slot_index < self.total_slots and self.slots[slot_index]:
            if self.slots[slot_index]['count'] > amount:
                self.slots[slot_index]['count'] -= amount
            else:
                self.slots[slot_index] = None
            return True
        return False

    def get_selected_item(self):
        """Get the item in the selected hotbar slot."""
        return self.slots[self.selected_slot]

    def select_slot(self, slot: int):
        """Select a hotbar slot (0-8)."""
        if 0 <= slot < self.hotbar_size:
            self.selected_slot = slot

    def is_inventory_open(self):
        """Check if inventory is open."""
        return self.inventory_open