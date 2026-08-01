init python:
    class EmptyCell(CellBase):
        def __init__(self, coord):
            super().__init__(coord)
            
            self.type = "empty"

        def check_collision(self, x, y, radius):
            return False, None, None, None, None