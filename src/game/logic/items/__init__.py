"""
MIT License
Copyright (c) 2026 [HansKnolle08]

Definition of the items package.

src/game/logic/items/__init__.py
"""

# Local import
from game.logic.items.items import FoodItem, Item, ITEM_REGISTRY, get_item_definition

# Define the public API of the items package
__all__ = ["Item", "FoodItem", "ITEM_REGISTRY", "get_item_definition"]
