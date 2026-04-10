from game.logic.core.gameplay_config import HAM_HEALTH_RESTORE, HAM_HUNGER_RESTORE, STACK_LIMIT

class Item:
    """Base item definition for inventory-only objects."""
    def __init__(self, name: str, display_name: str, stack_limit: int = STACK_LIMIT, can_place: bool = False) -> None:
        self.name: str = name
        self.display_name: str = display_name
        self.stack_limit: int = stack_limit
        self.can_place: bool = can_place
        self.is_food = False

    def __repr__(self) -> str:
        return f"Item(name={self.name}, display_name={self.display_name})"

class FoodItem(Item):
    """A consumable food item that restores hunger and optionally health."""
    def __init__(self, name: str, display_name: str, hunger_restore: int, health_restore: int = 0, stack_limit: int = STACK_LIMIT) -> None:
        super().__init__(name, display_name, stack_limit=stack_limit, can_place=False)
        self.hunger_restore: int = hunger_restore
        self.health_restore: int = health_restore
        self.is_food = True

    def __repr__(self) -> str:
        return f"FoodItem(name={self.name}, display_name={self.display_name}, hunger_restore={self.hunger_restore})"

# Define available inventory items here.
HAM = FoodItem("ham", "Ham", hunger_restore=HAM_HUNGER_RESTORE, health_restore=HAM_HEALTH_RESTORE)
WOOD = Item("wood", "Wood", can_place=True)
STONE = Item("stone", "Stone", can_place=True)
COPPER = Item("copper", "Copper", can_place=True)

ITEM_REGISTRY = {
    HAM.name: HAM,
    WOOD.name: WOOD,
    STONE.name: STONE,
    COPPER.name: COPPER,
}


def get_item_definition(item_name: str):
    return ITEM_REGISTRY.get(item_name)
