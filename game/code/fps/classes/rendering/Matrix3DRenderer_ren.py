import math
import renpy
from renpy.display.transform import Transform
from game.code.fps.classes.settings.Constants_ren import FpsConstants
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.enums.EGridAlignment_ren import EGridAlignment
from game.code.fps.other.named_tuples_ren import RaycastHitDDA

"""renpy
init python:
"""

class Matrix3DRenderer():
    def __init__(self, object_renderer):
        self.object_renderer = object_renderer
        self.game = object_renderer.game
        self.player = object_renderer.player

#region Public methods

    def draw(self, screen, offset, st):
        """
        Merges the matrix-rendered wall/door faces with sprite/shadow
        objects into a single depth-sorted draw pass. These used to be two
        entirely separate passes (all walls, then all sprites on top),
        which meant a sprite only got hidden if a raw raycast said it was
        FULLY occluded - a sprite partially behind a nearer wall face
        (e.g. at a corner) still drew whole, on top of the nearer wall
        pixels too. Sorting both kinds of item together by the same depth
        key fixes that, at whole-face/whole-sprite granularity.
        """
        wall_items = self._collect_matrix_draw_items()

        combined = [
            (depth, "wall", (cell, side, edge_override, plane_cell, tint))
            for depth, cell, side, edge_override, plane_cell, tint in wall_items
        ]
        combined.extend((p.near_depth, "object", p) for p in self.object_renderer.objects_to_render)

        combined.sort(key=lambda item: item[0], reverse=True)

        for depth, kind, payload in combined:
            if kind == "object":
                self.object_renderer.draw_object_item(screen, offset, st, payload)
                continue

            cell, side, edge_override, plane_cell, tint = payload
            if plane_cell is not None:
                self._draw_matrix_prototype_horizontal_plane(screen, offset, st, self.player, plane_cell)
            else:
                self._draw_matrix_prototype_face(screen, offset, st, self.player, cell, side, edge_override, tint)

#endregion

#region Internal methods

    def _collect_matrix_draw_items(self):
        """
        PROTOTYPE (temporary): collects every wall/button/door face
        currently on screen as a (depth, cell, side, edge_override,
        plane_cell, tint) item, to be rendered as its own single
        perspective matrix-transformed quad instead of per-column strips.
        Drawing is done by the caller so these items can be depth-sorted
        together with sprite/shadow objects. Tinted magenta and
        semi-transparent so it can be visually compared against the
        normal raycast rendering underneath it.
        """
        player = self.player

        raycast_results = self.object_renderer.raycast_hits

        ## collect every unique (cell, side) hit by any ray this frame, so
        ## adjacent faces (e.g. at a corner), and whatever's visible through
        ## a partially-open door, all get drawn - not just whatever's
        ## nearest. cast_rays_dda() already stops each ray's own hit list
        ## at the correct point (fully-blocking cells), so there's no need
        ## to break early here.
        seen = set()
        targets = []
        for hits in raycast_results:
            for hit in hits:
                key = (id(hit.cell), hit.side)
                if key not in seen:
                    seen.add(key)
                    targets.append(hit)

        ## rays are cast at fixed angular increments, so a wall cell that
        ## subtends a very small angle (far away and/or viewed at a
        ## grazing angle, looking along the wall run) can fall entirely
        ## between two ray samples and never get discovered at all - not
        ## drawn narrow, just silently missing. The classic per-column
        ## renderer doesn't have this problem since every screen column
        ## always draws whatever its own ray hit; this renderer only draws
        ## cells some ray actually found. Once any point on a wall run is
        ## found, walk outward along it (checking real neighbor cells, not
        ## more rays) to pick up whatever a ray sample skipped, including
        ## around corners onto a perpendicular run.
        for hit in list(targets):
            if hit.cell.type in (ECellType.Wall, ECellType.Button):
                for neighbor_cell, neighbor_side in self._expand_wall_run(hit.cell, hit.side, player, set()):
                    key = (id(neighbor_cell), neighbor_side)
                    if key not in seen:
                        seen.add(key)
                        targets.append(RaycastHitDDA(0, 0, neighbor_cell, 0, neighbor_side))

        ## a door with thickness < 1 sits recessed in a pocket; the
        ## neighboring wall face(s) bordering that pocket need to be split
        ## into segments aligned with the door's thickness span, since a
        ## single whole-face depth can't correctly order a face that's
        ## partially nearer and partially farther than the door across its
        ## own screen extent. Suppressed faces are rendered as split
        ## segments instead of their normal single whole-face quad.
        suppressed_faces = set()
        split_segments = [] ## (cell, side, min_edge, max_edge, crop_x_fraction)

        for target in targets:
            if target.cell.type in (ECellType.HorizontalDoor, ECellType.VerticalDoor):
                split_segments.extend(self._get_door_neighbor_splits(target.cell, suppressed_faces))

        ## painter's algorithm: draw farthest-first so nearer (opaque) quads
        ## correctly cover farther ones. near_depth comes from whichever
        ## single ray first discovered a face, which isn't representative
        ## of the whole face - e.g. a wide adjacent wall's discovering ray
        ## can land far from where it actually overlaps a nearby door on
        ## screen, sorting the wrong way. The face's own center-point depth
        ## (the same depth used to actually position its quad) is a more
        ## consistent, representative choice.
        ## DEBUG: color-code the split segments distinctly so it's clear
        ## which piece (before/middle/after the door's pocket) is which
        PIECE_TINTS = {"before": "#f00", "middle": "#0f0", "after": "#00f"}

        draw_items = []
        for target in targets:
            key = (id(target.cell), target.side)
            if key in suppressed_faces:
                continue
            center_x, center_y, _, _, _ = self._get_face_geometry(target.cell, target.side)
            dx = center_x - player.pos.x
            dy = center_y - player.pos.y
            center_depth = dx * math.cos(player.angle) + dy * math.sin(player.angle)
            draw_items.append((center_depth, target.cell, target.side, None, None, "#f0f"))

        for cell, side, seg_min, seg_max, crop_x_fraction, piece_label, door_cell in split_segments:
            if piece_label == "middle":
                ## the middle piece is the pocket's own reveal wall, flush against
                ## the door across its whole span - it has no single true depth of
                ## its own relative to the door. Anchor it directly to the depth of
                ## the door's OWN farthest face (not an estimate from the segment's
                ## own edges, which are offset from the door and can still land
                ## nearer than the door at some angles) so it's guaranteed to lose
                ## the painter's-algorithm tie against the door specifically,
                ## without being pushed behind unrelated objects in the scene.
                seg_depth = self._get_door_far_face_depth(door_cell, player)
            else:
                center_x, center_y, _, _, _ = self._get_face_geometry(cell, side)
                if side in (EDirection.Left, EDirection.Right):
                    center_y = (seg_min + seg_max) / 2
                else:
                    center_x = (seg_min + seg_max) / 2
                dx = center_x - player.pos.x
                dy = center_y - player.pos.y
                seg_depth = dx * math.cos(player.angle) + dy * math.sin(player.angle)

            draw_items.append((seg_depth, cell, side, (seg_min, seg_max, crop_x_fraction), None, PIECE_TINTS[piece_label]))

        ## the horizontal plane is per-cell (not per-face), so add one per
        ## unique vertical door among this frame's targets
        seen_vertical_doors = set()
        for target in targets:
            cell = target.cell
            if cell.type == ECellType.VerticalDoor and id(cell) not in seen_vertical_doors:
                seen_vertical_doors.add(id(cell))
                aabb = cell.get_aabb()
                dx = (aabb.min_x + aabb.max_x) / 2 - player.pos.x
                dy = (aabb.min_y + aabb.max_y) / 2 - player.pos.y
                plane_depth = dx * math.cos(player.angle) + dy * math.sin(player.angle)
                draw_items.append((plane_depth, None, None, None, cell, "#f0f"))

        return draw_items


    def _expand_wall_run(self, cell, side, player, visited):
        """
        Walks outward from a discovered wall/button face along its own
        tangent axis, in both directions, collecting any adjacent
        wall/button cells with a matching face - to recover cells a ray
        sample may have skipped entirely (see the call site). Bounded to
        keep cost proportional to the actual run length, not unbounded.

        At each end of the run, also checks a single step around the
        corner: a perpendicular face on the last matched cell (an
        outside-corner cell exposed on two sides) or on the cell just
        beyond the run, kept only if it's actually facing the player.
        This does NOT recurse any further around that corner - a single
        step only, since "facing the player" alone doesn't account for
        occlusion or FOV and cascading it was flooding across entire
        rooms. `visited` avoids reprocessing the same face twice.
        """
        key = (id(cell), side)
        if key in visited:
            return []
        visited.add(key)

        MAX_STEPS = 2

        if side in (EDirection.Left, EDirection.Right):
            step = (0, 1)
            perp_sides = (EDirection.Up, EDirection.Down)
        else:
            step = (1, 0)
            perp_sides = (EDirection.Left, EDirection.Right)

        cx, cy = cell.coord.x, cell.coord.y
        found = []

        for direction in (1, -1):
            x, y = cx, cy
            last_cell = cell

            for _ in range(MAX_STEPS):
                nx, ny = x + step[0] * direction, y + step[1] * direction
                neighbor = self.game.map.world_map.get((nx, ny))
                if neighbor is None or neighbor.type not in (ECellType.Wall, ECellType.Button):
                    break
                if not self._face_is_exposed(neighbor, side):
                    break
                found.append((neighbor, side))
                visited.add((id(neighbor), side))
                last_cell = neighbor
                x, y = nx, ny

            candidates = [last_cell]
            beyond = self.game.map.world_map.get((x + step[0] * direction, y + step[1] * direction))
            if beyond is not None and beyond.type in (ECellType.Wall, ECellType.Button):
                candidates.append(beyond)

            for candidate in candidates:
                for perp_side in perp_sides:
                    if (id(candidate), perp_side) in visited:
                        continue
                    if not self._face_is_exposed(candidate, perp_side):
                        continue
                    if self._face_faces_point(candidate, perp_side, player.pos):
                        found.append((candidate, perp_side))
                        visited.add((id(candidate), perp_side))

        return found


    def _face_is_exposed(self, cell, side):
        """
        True if there's open (non wall/button) space on this face's own
        side - i.e. it's a real, potentially-visible surface, not an
        interior face sandwiched between two solid cells. "Facing the
        player" alone doesn't check this: a wall's interior face can
        still point roughly toward the player's position.
        """
        if side == EDirection.Left:
            adjacent_coord = (cell.coord.x - 1, cell.coord.y)
        elif side == EDirection.Right:
            adjacent_coord = (cell.coord.x + 1, cell.coord.y)
        elif side == EDirection.Up:
            adjacent_coord = (cell.coord.x, cell.coord.y - 1)
        else: ## EDirection.Down
            adjacent_coord = (cell.coord.x, cell.coord.y + 1)

        adjacent_cell = self.game.map.world_map.get(adjacent_coord)

        return adjacent_cell is None or adjacent_cell.type not in (ECellType.Wall, ECellType.Button)


    def _face_faces_point(self, cell, side, point):
        """
        True if the given point is on the outward side of this cell face
        (i.e. the face could plausibly be visible from there).
        """
        center_x, center_y, _, _, normal_angle = self._get_face_geometry(cell, side)
        dx = point.x - center_x
        dy = point.y - center_y
        return dx * math.cos(normal_angle) + dy * math.sin(normal_angle) > 0


    def _get_door_far_face_depth(self, door_cell, player):
        """
        Depth of whichever of the door's two main faces is farther from the
        player - the door's front/back faces (Up/Down for an X-aligned door,
        Left/Right for Y-aligned) bound the depth range the door's pocket
        actually occupies, so anything meant to sit behind the door as a
        whole (e.g. the pocket's reveal wall) can anchor to this value.
        """
        main_faces = FpsConstants.VERTICAL_DIRECTIONS if door_cell.grid_alignment == EGridAlignment.X else FpsConstants.HORIZONTAL_DIRECTIONS

        depths = []
        for face in main_faces:
            center_x, center_y, _, _, _ = self._get_face_geometry(door_cell, face)
            dx = center_x - player.pos.x
            dy = center_y - player.pos.y
            depths.append(dx * math.cos(player.angle) + dy * math.sin(player.angle))

        ## nudged a hair farther than the actual far face so the reveal wall
        ## strictly loses the painter's-algorithm tie against it too (the sort
        ## is stable and the door faces are added to draw_items before the
        ## split segments, so an exact tie would otherwise draw the reveal
        ## wall - added later - on top of the door's own far face)
        return max(depths) + 0.0001


    def _get_door_neighbor_splits(self, cell, suppressed_faces):
        """
        For a door with thickness < 1, finds the wall/button cells
        bordering its recessed thickness pocket on either side, and splits
        each one's bordering face into up to 3 segments aligned with the
        pocket: before it, spanning it, and after it. Adds each affected
        (cell, side) to suppressed_faces so its normal whole-face render is
        skipped in favor of these segments.

        Horizontal doors shrink their footprint as they open, receding
        into one neighbor's side; that neighbor's middle segment is
        omitted since the door's own geometry already covers it there.
        Vertical doors never shrink this footprint, so both neighbors
        always get the full 3-way split.
        """
        if cell.thickness >= 1.0:
            return []

        cx, cy = cell.coord.x, cell.coord.y

        if cell.grid_alignment == EGridAlignment.X:
            axis_step = (1, 0)
            near_face, far_face = EDirection.Right, EDirection.Left
            pocket_min = cy + 0.5 + cell.offset - cell.thickness / 2
            pocket_max = cy + 0.5 + cell.offset + cell.thickness / 2
            cell_edge_min, cell_edge_max = cy, cy + 1
        else:
            axis_step = (0, 1)
            near_face, far_face = EDirection.Down, EDirection.Up
            pocket_min = cx + 0.5 + cell.offset - cell.thickness / 2
            pocket_max = cx + 0.5 + cell.offset + cell.thickness / 2
            cell_edge_min, cell_edge_max = cx, cx + 1

        ## which neighbor (by axis offset) the door recedes into as it
        ## opens; only horizontal doors shrink their footprint at all
        omit_middle_offset = None
        if cell.type == ECellType.HorizontalDoor:
            omit_middle_offset = -1 if cell.open_direction == EDirection.Right else 1

        segments = []

        for axis_offset, face in ((-1, near_face), (1, far_face)):
            neighbor_coord = (cx + axis_step[0] * axis_offset, cy + axis_step[1] * axis_offset)
            neighbor_cell = self.game.map.world_map.get(neighbor_coord)

            if neighbor_cell is None or neighbor_cell.type not in (ECellType.Wall, ECellType.Button):
                continue

            suppressed_faces.add((id(neighbor_cell), face))

            pieces = [(cell_edge_min, pocket_min, "before")]
            if axis_offset != omit_middle_offset:
                pieces.append((pocket_min, pocket_max, "middle"))
            pieces.append((pocket_max, cell_edge_max, "after"))

            for seg_min, seg_max, piece_label in pieces:
                if seg_max - seg_min > 0.001:
                    crop_x_fraction = (seg_min - cell_edge_min) % 1.0
                    segments.append((neighbor_cell, face, seg_min, seg_max, crop_x_fraction, piece_label, cell))

        return segments


    def _get_face_geometry(self, cell, side):
        """
        Returns (center_x, center_y, min_edge, max_edge, normal_angle) for
        a cell face. For walls/buttons this is always the full 1x1 cell;
        for doors it tracks the cell's current (possibly shrunk/offset)
        AABB, so a door slides/narrows correctly.
        """
        aabb = cell.get_aabb()

        if side == EDirection.Left:
            min_edge, max_edge = aabb.min_y, aabb.max_y
            center_x, center_y = aabb.min_x, (aabb.min_y + aabb.max_y) / 2
            normal_angle = math.pi
        elif side == EDirection.Right:
            min_edge, max_edge = aabb.min_y, aabb.max_y
            center_x, center_y = aabb.max_x, (aabb.min_y + aabb.max_y) / 2
            normal_angle = 0.0
        elif side == EDirection.Up:
            min_edge, max_edge = aabb.min_x, aabb.max_x
            center_x, center_y = (aabb.min_x + aabb.max_x) / 2, aabb.min_y
            normal_angle = -math.pi / 2
        else: ## EDirection.Down
            min_edge, max_edge = aabb.min_x, aabb.max_x
            center_x, center_y = (aabb.min_x + aabb.max_x) / 2, aabb.max_y
            normal_angle = math.pi / 2

        return center_x, center_y, min_edge, max_edge, normal_angle


    def _draw_matrix_prototype_face(self, screen, offset, st, player, cell, side, edge_override=None, tint="#f0f"):
        """
        edge_override, when given, is (min_edge, max_edge, crop_x_fraction)
        and renders just that sub-span of the face's tangent axis instead
        of the whole thing - used to split a wall face bordering a door's
        recessed thickness pocket into independently depth-sortable pieces.
        """
        offset_x, offset_y = offset

        center_x, center_y, min_edge, max_edge, normal_angle = self._get_face_geometry(cell, side)

        crop_x_fraction = None

        if edge_override is not None:
            min_edge, max_edge, crop_x_fraction = edge_override
            if side in (EDirection.Left, EDirection.Right):
                center_y = (min_edge + max_edge) / 2
            else:
                center_x = (min_edge + max_edge) / 2

        face_width = max_edge - min_edge

        if face_width <= 0.001:
            return

        texture, texture_size_ratio = cell.get_texture(side)

        if texture is None:
            return

        T = FpsSettings.TEXTURE_SIZE

        ## local +X points in world direction (normal_angle - 90 deg); on
        ## Right/Up faces that points opposite to how the tangent axis
        ## (min_edge -> max_edge) increases, so local-x=0 lands on max_edge
        ## instead of min_edge there and the crop must be mirrored to
        ## compensate. Left/Down faces already agree, no mirror needed.
        mirror = side in (EDirection.Right, EDirection.Up)

        if crop_x_fraction is None:
            ## default (walls, buttons, door end-caps): show the whole
            ## texture, spanning the face's full current width
            crop_x_fraction = 0.0

            if cell.type == ECellType.HorizontalDoor:
                is_main_face = (
                    (cell.grid_alignment == EGridAlignment.X and side in FpsConstants.VERTICAL_DIRECTIONS) or
                    (cell.grid_alignment == EGridAlignment.Y and side in FpsConstants.HORIZONTAL_DIRECTIONS)
                )

                if is_main_face:
                    ## same offset formula as BaseDoorCell.ray_intersect, evaluated
                    ## at this face's near/fixed edge, so the texture appears to
                    ## slide into its pocket rather than stretch as the door opens
                    coord_axis = cell.coord.x if cell.grid_alignment == EGridAlignment.X else cell.coord.y

                    if cell.open_direction == EDirection.Right:
                        crop_x_fraction = (min_edge - (coord_axis + 1 - cell.open_amount)) % 1.0
                    else:
                        crop_x_fraction = (min_edge - (coord_axis + cell.open_amount)) % 1.0

        logical_texture_width = T * texture_size_ratio
        crop_x = int(crop_x_fraction * logical_texture_width)

        if texture_size_ratio != 1.0:
            ## a non-1:1 ratio (e.g. a door's thin end-cap) means this
            ## texture is a single "whole edge profile" image meant to
            ## stretch across however wide the face currently is, not tile
            ## at a fixed per-world-unit density like the main texture -
            ## crop the whole thing rather than a sliver proportional to
            ## face_width (which produced a blown-up, stretched-looking result)
            crop_width = max(1, int(logical_texture_width))
        else:
            crop_width = max(1, int(face_width * logical_texture_width))

        ## default (walls, buttons, horizontal doors): full height, 0..1,
        ## full texture (crop_y=0)
        height_min, height_max = 0.0, 1.0
        crop_y = 0

        if cell.type == ECellType.VerticalDoor:
            ## the door slides up (into the ceiling) or down (into the
            ## floor); the remaining visible slice, and which portion of
            ## the texture it shows, depends on which direction. Applies to
            ## both the main face and its end-caps, since the whole cell's
            ## visible height shrinks together.
            if cell.open_direction == EDirection.Up:
                ## bottom rises as it slides up into the ceiling; texture
                ## crop slides down to keep pace (matches classic renderer)
                height_min, height_max = cell.open_amount, 1.0
                crop_y = int(cell.open_amount * T)
            elif cell.open_direction == EDirection.Down:
                ## top recedes as it slides down into the floor; texture
                ## crop stays anchored at the top
                height_min, height_max = 0.0, 1.0 - cell.open_amount

        crop_height = max(1, int((height_max - height_min) * T))

        ## the quad's own local size, in our world-unit-to-coordinate-unit
        ## scale (T pixels per world unit) - computed straight from the
        ## continuous face_width/height, NOT from crop_width/crop_height.
        ## Those are texel-truncated, and a door's face_width/height shrinks
        ## continuously as it opens; deriving the destination size from the
        ## truncated texel count would round it down by up to a texel,
        ## pulling both edges of the quad inward around its fixed center and
        ## opening a hairline gap against the neighboring wall on the door's
        ## non-moving edge until it lands back on a whole texel at
        ## open_amount 0 or 1. size=(quad_width, quad_height) below (always
        ## applied) resamples the truncated crop up to this exact size so
        ## geometry stays gapless even when the source texels don't evenly
        ## divide it.
        quad_width = face_width * T
        quad_height = (height_max - height_min) * T

        dx = center_x - player.pos.x
        dy = center_y - player.pos.y

        cos_a = math.cos(player.angle)
        sin_a = math.sin(player.angle)

        ## forward depth and left/right offset of the face's center, relative to the camera
        depth = dx * cos_a + dy * sin_a
        sideways = dy * cos_a - dx * sin_a

        ## depth is an affine function of world position, and the face is a
        ## straight line segment, so its two edges bound the depth range
        ## across the whole face (the center depth checked above is just
        ## their average). Culling on the center alone would drop a wide
        ## face standing close to the player whose center falls behind the
        ## camera even though an edge - and everything on screen near it -
        ## is still clearly in front. Only cull if neither edge reaches the
        ## near threshold either.
        if side in (EDirection.Left, EDirection.Right):
            edge1_x, edge1_y = center_x, min_edge
            edge2_x, edge2_y = center_x, max_edge
        else:
            edge1_x, edge1_y = min_edge, center_y
            edge2_x, edge2_y = max_edge, center_y

        edge1_depth = (edge1_x - player.pos.x) * cos_a + (edge1_y - player.pos.y) * sin_a
        edge2_depth = (edge2_x - player.pos.x) * cos_a + (edge2_y - player.pos.y) * sin_a

        if depth <= 0.05 and edge1_depth <= 0.05 and edge2_depth <= 0.05:
            return

        P = FpsSettings.PROJECTION_DISTANCE
        eye_height = 0.5
        face_height = (height_min + height_max) / 2 ## center of the visible slice, in world units

        ## degrees to rotate the (by default camera-facing) quad around the
        ## vertical axis so it matches the wall face's own orientation.
        ## Negated relative to the naive world-angle-difference: Ren'Py's
        ## yrotate handedness runs opposite to what that would suggest.
        rotation_deg = -math.degrees(normal_angle - player.angle - math.pi)

        ## Matrix.perspective's coordinate system has (0,0) at the screen's
        ## top-left (not centered), so the world offset must explicitly
        ## include the screen-center bias. matrixanchor is avoided because it
        ## composes unsafely with a non-affine (perspective) matrix; centering
        ## for rotation is done by hand instead, via the trailing offset below.
        quad_matrix = (
            Matrix.perspective(FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, P * 0.01, P, P * (FpsSettings.MAX_DEPTH + 10))
            * Matrix.offset(
                FpsSettings.HALF_SCREEN_WIDTH + sideways * T,
                FpsSettings.HALF_SCREEN_HEIGHT - (face_height - eye_height) * T,
                P - T * depth,
            )
            * Matrix.rotate(0, rotation_deg, 0)
            * Matrix.offset(-quad_width / 2, -quad_height / 2, 0)
        )

        ## crop/resize on the SAME Transform as matrixtransform breaks
        ## rendering entirely (even when the crop is a mathematical no-op),
        ## so the crop is done on an inner Transform, with matrixtransform
        ## applied on an outer one wrapping it.
        inner_kwargs = dict(crop=(crop_x, crop_y, crop_width, crop_height), size=(quad_width, quad_height))

        if mirror:
            inner_kwargs["xzoom"] = -1.0

        cropped = Transform(texture, **inner_kwargs)

        face_transform = Transform(
            cropped,
            matrixtransform=quad_matrix,
            matrixanchor=(0, 0),
            matrixcolor=TintMatrix(tint),
            alpha=1.0,
        )

        face_render = renpy.render(face_transform, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, 0)

        screen.blit(face_render, (0 + offset_x, 0 + offset_y))


    def _draw_matrix_prototype_horizontal_plane(self, screen, offset, st, player, cell):
        """
        PROTOTYPE: the horizontal surface exposed above/below a vertical
        door as it slides open (matching _draw_vertical_door_horizontal_side
        in the classic renderer). Unlike every other face so far, this quad
        lies flat rather than standing vertical, so on top of the usual
        yrotate (aiming it at the right compass direction) it also needs an
        xrotate to tilt it out of the vertical plane.
        """
        if cell.open_amount < 0.5:
            return

        offset_x, offset_y = offset

        aabb = cell.get_aabb()
        z = cell.get_horizontal_side_z()

        center_x = (aabb.min_x + aabb.max_x) / 2
        center_y = (aabb.min_y + aabb.max_y) / 2

        if cell.grid_alignment == EGridAlignment.X:
            long_extent = aabb.max_x - aabb.min_x
            short_extent = aabb.max_y - aabb.min_y
            long_axis_angle = 0.0
        else:
            long_extent = aabb.max_y - aabb.min_y
            short_extent = aabb.max_x - aabb.min_x
            long_axis_angle = math.pi / 2

        if long_extent <= 0.001 or short_extent <= 0.001:
            return

        texture = cell.plane_texture

        dx = center_x - player.pos.x
        dy = center_y - player.pos.y

        cos_a = math.cos(player.angle)
        sin_a = math.sin(player.angle)

        depth = dx * cos_a + dy * sin_a
        sideways = dy * cos_a - dx * sin_a

        ## same reasoning as _draw_matrix_prototype_face: this is a flat
        ## rectangle rather than a line, so check all four AABB corners
        ## rather than just the center before culling as fully behind.
        corner_depths = [
            (cx - player.pos.x) * cos_a + (cy - player.pos.y) * sin_a
            for cx, cy in ((aabb.min_x, aabb.min_y), (aabb.min_x, aabb.max_y), (aabb.max_x, aabb.min_y), (aabb.max_x, aabb.max_y))
        ]

        if depth <= 0.05 and max(corner_depths) <= 0.05:
            return

        T = FpsSettings.TEXTURE_SIZE
        P = FpsSettings.PROJECTION_DISTANCE
        eye_height = 0.5

        quad_width = long_extent * T
        quad_height = short_extent * T

        ## same yrotate formula as the vertical faces, but aiming the local
        ## +X axis at the footprint's long axis instead of a wall normal
        rotation_deg = -math.degrees(long_axis_angle - player.angle - math.pi / 2)

        quad_matrix = (
            Matrix.perspective(FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, P * 0.01, P, P * (FpsSettings.MAX_DEPTH + 10))
            * Matrix.offset(
                FpsSettings.HALF_SCREEN_WIDTH + sideways * T,
                FpsSettings.HALF_SCREEN_HEIGHT - (z - eye_height) * T,
                P - T * depth,
            )
            * Matrix.rotate(0, rotation_deg, 0)
            * Matrix.rotate(90, 0, 0)
            * Matrix.offset(-quad_width / 2, -quad_height / 2, 0)
        )

        resized = Transform(texture, size=(quad_width, quad_height))

        plane_transform = Transform(
            resized,
            matrixtransform=quad_matrix,
            matrixanchor=(0, 0),
            matrixcolor=TintMatrix("#f0f"),
            alpha=1.0,
        )

        plane_render = renpy.render(plane_transform, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, 0)

        screen.blit(plane_render, (0 + offset_x, 0 + offset_y))

#endregion
