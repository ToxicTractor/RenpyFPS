init -100 python:
    ## widely used
    Vector2 = namedtuple("Position", ["x", "y"])
    Rect = namedtuple("Rect", ["x", "y", "width", "height"])

    ## axis aligned bounding box used for collisions
    AABB = namedtuple("AABB", ["min_x", "min_y", "max_x", "max_y"])
    
    ## used by the raycaster
    CellTraceEntry = namedtuple("CellTraceEntry", ["cell", "depth", "cell_side"])
    RaycastHitDDA = namedtuple("RaycastHitDDA", ["near_depth", "far_depth","cell", "offset", "side"])
    
    ## notification
    NotificationEntry = namedtuple("NotificationEntry", ["text", "duration", "type"])

    ## inventory and items
    InventoryItem = namedtuple("InventoryItem", ["id", "name", "icon"])
