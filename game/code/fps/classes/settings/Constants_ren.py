from abc import ABC
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.enums.EEmotion_ren import EFaceEmote

"""renpy
init -99 python:
"""

class FpsConstants(ABC):
    ## Common
    DIRECTIONS = (EDirection.Up, EDirection.Right, EDirection.Down, EDirection.Left)
    HORIZONTAL_DIRECTIONS = (EDirection.Right, EDirection.Left)
    VERTICAL_DIRECTIONS = (EDirection.Up, EDirection.Down)

    ## Doors
    LOCKED_DOOR_NOTIFICATION = "It wont budge."

    ## Buttons
    LOCKED_BUTTON_NOTIFICATION = "It doesn't work."

    ## Notifications
    DEFAULT_NOTIFICATION_DURATION = 2.5

    ## Face
    NEUTRAL_EMOTES = (EFaceEmote.Neutral, EFaceEmote.LookLeft, EFaceEmote.LookRight)
    LOOK_EMOTES = (EFaceEmote.LookLeft, EFaceEmote.LookRight)
