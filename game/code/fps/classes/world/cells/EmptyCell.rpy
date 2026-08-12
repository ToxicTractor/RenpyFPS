init python:
    class EmptyCell(CellBase):
        def __init__(self, coord):
            super().__init__(coord)
            
            self.type = ECellType.Empty

        @property
        def is_npc_walkable(self):
            return True


        def get_texture(self, side):
            return None, 1.0


        def check_collision(self, x, y, radius):
            return False, None, None, None, None