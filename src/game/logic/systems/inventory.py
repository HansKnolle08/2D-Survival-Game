class Inventory:
    """
    Inventory system with hotbar and main inventory.
    """
    def __init__(self):
        self.hotbar_size = 9
        self.inventory_rows = 4
        self.inventory_cols = 9
        self.main_inventory_size = self.inventory_rows * self.inventory_cols  # 36
        self.total_slots = self.hotbar_size + self.main_inventory_size  # 45
        self.slots = [None] * self.total_slots  # Each slot: {'item': str, 'count': int} or None
        self.selected_slot = 0  # Hotbar slot 0-8
        self.inventory_open = False

    def toggle_inventory(self):
        """Toggle the inventory open/closed."""
        self.inventory_open = not self.inventory_open

    def add_item(self, item_name: str, amount: int = 1):
        """Add items to inventory, stacking if possible."""
        # First, try to stack in existing slots
        for i in range(self.total_slots):
            if self.slots[i] and self.slots[i]['item'] == item_name:
                self.slots[i]['count'] += amount
                return True
        # Then, find empty slot
        for i in range(self.total_slots):
            if self.slots[i] is None:
                self.slots[i] = {'item': item_name, 'count': amount}
                return True
        return False  # Inventory full

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