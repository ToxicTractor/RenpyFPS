from enum import Enum

"""renpy
init -999 python:
"""

class ETriggerType(Enum):
    PlayerOnly  = 0
    NpcOnly     = 1
    Any         = 2
