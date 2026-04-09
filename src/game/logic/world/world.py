class World:
    """
    Represents the game world as a 2D grid of tiles.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialize 2D grid with default tile type
        self.tiles = [
            ["grass" for _ in range(width)]
            for _ in range(height)
        ]

    def get_tile(self, x, y):
        """
        Get the tile type at the specified coordinates.
        
        Args:
            x (int): X-coordinate
            y (int): Y-coordinate
            
        Returns:
            str: Tile type
        """
        return self.tiles[y][x]