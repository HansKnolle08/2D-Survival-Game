class Food:
    """
    Represents a collectible food item that restores hunger.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16  # Half tile size
        self.hunger_restore = 20  # Amount of hunger restored