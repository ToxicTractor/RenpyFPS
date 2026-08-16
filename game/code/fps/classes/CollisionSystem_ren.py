import math
from abc import ABC
from game.code.fps.other.helper_functions_ren import clamp, sqr_dist
from game.code.fps.other.named_tuples_ren import Vector2

"""renpy
init -100 python:
"""

class CollisionSystem(ABC):
    COLLISION_PASS_COUNT = 3

    @staticmethod
    def collision_pass(game, actor, override_pass_count=None):
        collision_pass_count = override_pass_count if override_pass_count else CollisionSystem.COLLISION_PASS_COUNT
        x, y = actor.pos
        radius = actor.radius

        ## run correction passes
        for _ in range(collision_pass_count):

            object_correction, x, y = CollisionSystem._resolve_object_collisions(game, x, y, actor)
            cell_correction, x, y = CollisionSystem._resolve_cell_collisions(game, x, y, radius)

            ## if neither had any corrections, we are at a valid position
            if (not (object_correction or cell_correction)):
                break

        ## return corrected values
        return Vector2(x, y)


    @staticmethod
    def _resolve_object_collisions(game, x, y, actor):
        changed = False
        radius = actor.radius

        for sprite_object in (game.npcs + game.sprite_objects):

            ## we don't collide with ourselves
            if sprite_object == actor:
                continue

            ## we only collide with solid objects
            if (not sprite_object.is_solid):
                continue

            check_distance = radius + sprite_object.radius

            dx = x - sprite_object.pos.x
            dy = y - sprite_object.pos.y

            distance_sqrd = sqr_dist(sprite_object.pos, (x, y))
            ## if distance is larger than check distance, no correction is needed
            if (distance_sqrd >= check_distance ** 2):
                continue

            ## correct x and y
            distance = math.sqrt(distance_sqrd)

            if (distance == 0):
                dx = 1
                dy = 0
                distance = 1

            penetration = check_distance - distance

            x += dx / distance * penetration
            y += dy / distance * penetration

            changed = True

        return changed, x, y


    @staticmethod
    def _resolve_cell_collisions(game, x, y, radius):
        changed = False
        world_map = game.map.world_map
        max_x = game.map.width - 1
        max_y = game.map.height - 1

        ## find the cells we need to check collisions for
        min_coord_x = clamp(int(x - radius - 1), 0, max_x)
        max_coord_x = clamp(int(x + radius + 1), 0, max_x)
        min_coord_y = clamp(int(y - radius - 1), 0, max_y)
        max_coord_y = clamp(int(y + radius + 1), 0, max_y)

        for cell_y in range(min_coord_y, max_coord_y + 1):
            for cell_x in range(min_coord_x, max_coord_x + 1):
                cell = world_map[(cell_x, cell_y)]

                ## check if we collide with the cell                    
                collides, dx, dy, distance, penetration = cell.check_collision(x, y, radius)

                ## if we dont collide, just continue to the next cell
                if (not collides):
                    continue

                ## correct x and y
                if (distance == 0):
                    cell_min_x, cell_min_y, cell_max_x, cell_max_y = cell.get_aabb()

                    left = x - cell_min_x
                    right = cell_max_x - x
                    top = y - cell_min_y
                    bottom = cell_max_y - y

                    minimum = min(left, right, top, bottom)

                    if minimum == left:
                        x -= radius + left
                    elif minimum == right:
                        x += radius + right
                    elif minimum == top:
                        y -= radius + top
                    else:
                        y += radius + bottom

                else:
                    x += dx / distance * penetration
                    y += dy / distance * penetration

                changed = True

        return changed, x, y
