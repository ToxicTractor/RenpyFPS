from copy import deepcopy
from game.code.fps.enums.EAvailability_ren import EAvailability

"""renpy
init python:
"""

class ObjectPool():
    def __init__(self, obj, pool_size, dynamic=True):

        self._obj = obj
        self._pool = {}
        self._dynamic = dynamic

        for i in range(pool_size):
            self._pool[deepcopy(self._obj)] = EAvailability.Available


    def get(self):

        for key, value in self._pool.items():
            if (value == EAvailability.Available):
                self._pool[key] = EAvailability.Unavailable
                return key

        if (self._dynamic):
            new_entry = deepcopy(self._obj)
            self._pool[new_entry] = EAvailability.Unavailable
            return new_entry

        return None


    def release(self, obj):

        if (obj in self._pool.keys()):
            obj.reset()
            self._pool[obj] = EAvailability.Available
