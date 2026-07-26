init python:
    class EmptyCell(CellBase):
        def __init__(self, coord):
            super().__init__(coord)
            
            self.type = "empty"

        def blocks_movement(self, x, y, radius):
            return False