init -1 python:
    class FpsConstants(ABC):
        DIRECTIONS = (EDirection.Up, EDirection.Right, EDirection.Down, EDirection.Left)
        HORIZONTAL_DIRECTIONS = (EDirection.Right, EDirection.Left)
        VERTICAL_DIRECTIONS = (EDirection.Up, EDirection.Down)