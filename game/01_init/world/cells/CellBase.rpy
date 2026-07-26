init -1 python:
    class CellBase(ABC):
        def __init__(self, coord):
            self.type = None
            self.coord = coord
        
        @property
        def coord_x(self):
            return self.coord[0]

        @property
        def coord_y(self):
            return self.coord[1]

        def is_interactable(self, side):
            return False
        
        @abstractmethod
        def blocks_movement(self, x, y, radius):
            pass

