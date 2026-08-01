init -1000 python:
    import heapq ## used for A* pathfinding
    import math
    import pygame ## used for input detection
    import struct ## used for isqrt approximation

    from abc import ABC, abstractmethod
    from copy import deepcopy ## used for ObjectPool
    from collections import namedtuple
