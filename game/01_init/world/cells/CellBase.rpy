init python:
    class CellBase(ABC):
        def __init__(self, coordinate):
            self.type = None
            self.coordinate = coordinate
