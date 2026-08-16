from abc import ABC
from dataclasses import dataclass

"""renpy
init python:
"""

@dataclass
class AmmoType(ABC):
    def __init__(self):
        self.name = None
        self.max = 999

@dataclass
class ShotgunAmmoType(AmmoType):
    def __init__(self):
        super().__init__()
        self.name = "shotgun"

@dataclass
class RevolverAmmoType(AmmoType):
    def __init__(self):
        super().__init__()
        self.name = ".44"
