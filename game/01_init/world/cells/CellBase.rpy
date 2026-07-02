init python:
    class CellBase(ABC):
        def __init__(self, coordinate):
            self.type = None
            self.coordinate = coordinate
        
        @property
        def coord_x(self):
            return self.coordinate[0]

        @property
        def coord_y(self):
            return self.coordinate[1]

        @property
        def interactable(self):
            return False
        
        @abstractmethod
        def blocks_movement(self, x, y, radius):
            pass

