init python:
    class EmptyCell(CellBase):
        def __init__(self, coord):
            super().__init__(coord)
            
            self.type = "empty"


        @property
        def is_npc_walkable(self):
            return True


        def check_collision(self, x, y, radius):
            return False, None, None, None, None