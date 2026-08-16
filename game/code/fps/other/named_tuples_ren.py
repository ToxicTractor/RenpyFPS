from collections import namedtuple

"""renpy
init -100 python:
"""

## common
Vector2 = namedtuple("Vector2", ["x", "y"])
Rect = namedtuple("Rect", ["x", "y", "width", "height"])

## axis aligned bounding box used for collisions
AABB = namedtuple("AABB", ["min_x", "min_y", "max_x", "max_y"])

## used by the raycaster
CellTraceEntry = namedtuple("CellTraceEntry", ["cell", "depth", "cell_side"])
RaycastHitDDA = namedtuple("RaycastHitDDA", ["near_depth", "far_depth","cell", "offset", "side"])

## rendering
ProjectionResult = namedtuple ("ProjectionResult", ["near_depth", "far_depth", "texture", "crop", "size", "position", "at", "cell", "cell_side"])

## notification
NotificationEntry = namedtuple("NotificationEntry", ["text", "duration", "type"])

## inventory and items
InventoryItem = namedtuple("InventoryItem", ["id", "name", "icon"])