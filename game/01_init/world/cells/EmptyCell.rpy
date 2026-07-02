init python:
    class EmptyCell(CellBase):
        def __init__(self, coordinate):
            super().__init__(coordinate)
            
            self.type = "empty"

        def blocks_movement(self, x, y, radius):
            return False