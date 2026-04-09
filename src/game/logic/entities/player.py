class Player:
    """
    Represents the player entity with position and movement speed.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # Pixels per second