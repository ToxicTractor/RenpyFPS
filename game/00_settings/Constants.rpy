init -99 python:
    class FpsConstants(ABC):
        DIRECTIONS = (EDirection.Up, EDirection.Right, EDirection.Down, EDirection.Left)
        HORIZONTAL_DIRECTIONS = (EDirection.Right, EDirection.Left)
        VERTICAL_DIRECTIONS = (EDirection.Up, EDirection.Down)

        ## Doors
        LOCKED_DOOR_NOTIFICATION = "It wont budge."

        ## Buttons
        LOCKED_BUTTON_NOTIFICATION = "It doesn't work."

        ## Notifications
        DEFAULT_NOTIFICATION_DURATION = 2.5