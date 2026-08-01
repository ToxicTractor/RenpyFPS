init -100 python:

    ## axis aligned bounding box used for collisions
    AABB = namedtuple("AABB", ["min_x", "min_y", "max_x", "max_y"])
    
    ## used by the raycaster
    CellTraceEntry = namedtuple("CellTraceEntry", ["cell", "depth", "cell_side"])