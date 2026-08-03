init -1 python:
    class FpsConstants(ABC):
        DIRECTIONS = (EDirection.North, EDirection.East, EDirection.South, EDirection.West)
        HORIZONTAL_DIRECTIONS = (EDirection.East, EDirection.West)
        VERTICAL_DIRECTIONS = (EDirection.North, EDirection.South)