from game.logic.systems.inventory import Inventory

class Player:
    """
    Represents the player entity with position, movement speed, health, and inventory.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # Pixels per second
        self.health = 100  # Max health
        self.max_health = 100
        self.inventory = Inventory()