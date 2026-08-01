init -100 python:
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
            return x, y
        

        @staticmethod
        def _resolve_object_collisions(game, x, y, actor):
            changed = False
            radius = actor.radius

            ## TODO: implement collisions for all SpriteObjects, currently only NPCs have collisions
            for npc in game.npcs:
                
                ## we don't collide with ourselves
                if npc == actor:
                    continue

                ## if the npc is dead just skip it
                if not npc.is_alive:
                    continue

                npc_check_distance = radius + npc.radius
                
                dx = x - npc.pos_x
                dy = y - npc.pos_y

                distance_sqrd = sqr_dist(npc.pos, (x, y))
                ## if distance is larger than check distance, no correction is needed
                if (distance_sqrd >= npc_check_distance ** 2):
                    continue

                ## correct x and y
                distance = math.sqrt(distance_sqrd)
                
                if (distance == 0):
                    dx = 1
                    dy = 0
                    distance = 1
                
                penetration = npc_check_distance - distance
                
                x += dx / distance * penetration
                y += dy / distance * penetration

                changed = True

            return changed, x, y
        

        @staticmethod
        def _resolve_cell_collisions(game, x, y, radius):
            changed = False
            world_map = game.map.world_map

            ## find the cells we need to check collisions for
            min_coord_x = int(x - radius - 1)
            max_coord_x = int(x + radius + 1)
            min_coord_y = int(y - radius - 1)
            max_coord_y = int(y + radius + 1)

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
        