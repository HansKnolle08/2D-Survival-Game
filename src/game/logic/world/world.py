class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 2D Grid
        self.tiles = [
            ["grass" for _ in range(width)]
            for _ in range(height)
        ]

    def get_tile(self, x, y):
        return self.tiles[y][x]