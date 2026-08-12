init -1000 python:
    import heapq ## used for A* pathfinding
    import math
    import pygame ## used for input detection
    import struct ## used for isqrt approximation
    import random

    from abc import ABC, abstractmethod
    from copy import deepcopy ## used for ObjectPool
    from collections import namedtuple
    from dataclasses import dataclass ## used for AmmoTypes
    from enum import Enum