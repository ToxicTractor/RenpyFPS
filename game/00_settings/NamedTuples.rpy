init -100 python:
    from collections import namedtuple

    ## axis aligned bounding box used for collisions
    AABB = namedtuple("AABB", ["min_x", "min_y", "max_x", "max_y"])