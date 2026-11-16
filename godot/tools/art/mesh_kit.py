"""Low-poly modelling kit: builds meshes from lathes, tubes, spheres, boxes and sweeps.

Every primitive gets one flat vertex colour from the palette and, for characters, one
bone: all its vertices are weighted 1.0 to that bone, so the figure moves like a jointed
wooden toy. Blender axes: Z up, the figure faces -Y, its left hand is at +X.
"""

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

from palette import linear

TAU = math.pi * 2.0


def _ring_angles(segs, a0, a1):
    if a1 is None:
        return [TAU * i / segs for i in range(segs)], True
    return [a0 + (a1 - a0) * i / segs for i in range(segs + 1)], False


def lathe(profile, segs=12, sx=1.0, sy=1.0, a0=0.0, a1=None, cap0=True, cap1=True):
    """Surface of revolution around Z.

    profile: list of (z, r) or (z, r, "hard") going from the bottom up the outside;
    "hard" splits the shading at that ring. An angle of 0 points to the front (-Y),
    angles grow towards the left side (+X). With a1 given, only that arc is built and
    the surface stays open. Returns (verts, faces).
    """
    angles, closed = _ring_angles(segs, a0, a1)
    verts, faces = [], []
    starts, ends = [], []
    for p in profile:
        z, r = p[0], p[1]
        hard = len(p) > 2 and p[2] == "hard"
        if r <= 1e-6:
            verts.append((0.0, 0.0, z))
            idx = [len(verts) - 1]
            starts.append(idx)
            ends.append(idx)
            continue
        ring = []
        for a in angles:
            ring.append(len(verts))
            verts.append((r * sx * math.sin(a), -r * sy * math.cos(a), z))
        ends.append(ring)
        if hard:
            ring2 = []
            for a in angles:
                ring2.append(len(verts))
                verts.append((r * sx * math.sin(a), -r * sy * math.cos(a), z))
            starts.append(ring2)
        else:
            starts.append(ring)
    n = len(angles)
    steps = n if closed else n - 1
    for i in range(len(profile) - 1):
        lo, hi = starts[i], ends[i + 1]
        if len(lo) == 1 and len(hi) == 1:
            continue
        for j in range(steps):
            j2 = (j + 1) % n
            if len(lo) == 1:
                faces.append((lo[0], hi[j2], hi[j]))
            elif len(hi) == 1:
                faces.append((lo[j], lo[j2], hi[0]))
            else:
                faces.append((lo[j], lo[j2], hi[j2], hi[j]))
    if closed:
        first, last = ends[0], starts[-1]
        if cap0 and len(first) > 1:
            faces.append(tuple(reversed(first)))
        if cap1 and len(last) > 1:
            faces.append(tuple(last))
    return verts, faces


def ellipsoid_profile(rz, rings=7, z0=0.0, squash_bottom=1.0):
    """Profile of an ellipsoid with unit horizontal radius and half-height rz."""
    out = []
    for i in range(rings + 1):
        t = math.pi * i / rings
        z = -math.cos(t) * rz
        if z < 0:
            z *= squash_bottom
        out.append((z0 + z, math.sin(t)))
    return out


def box_geom(sx, sy, sz, taper=1.0):
    """Box centred at the origin; `taper` scales the top face."""
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    tx, ty = hx * taper, hy * taper
    verts = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
             (-tx, -ty, hz), (tx, -ty, hz), (tx, ty, hz), (-tx, ty, hz)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return verts, faces


def frame_along(p0, p1, roll_hint=None):
    """Matrix whose Z runs from p0 towards p1 (origin at p0)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    z = d.normalized()
    hint = Vector(roll_hint) if roll_hint else (Vector((0, -1, 0)) if abs(z.y) < 0.9 else Vector((0, 0, 1)))
    x = hint.cross(z)
    if x.length < 1e-6:
        x = Vector((1, 0, 0)).cross(z)
    x.normalize()
    y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4()
    m.translation = p0
    return m, d.length


def _transport_frames(points):
    pts = [Vector(p) for p in points]
    tangents = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        tangents.append((b - a).normalized())
    t0 = tangents[0]
    ref = Vector((0, 0, 1)) if abs(t0.z) < 0.9 else Vector((1, 0, 0))
    n = (ref - t0 * ref.dot(t0)).normalized()
    frames = []
    for t in tangents:
        n = (n - t * n.dot(t)).normalized()
        frames.append((t, n, t.cross(n)))
    return pts, frames


def sweep(points, radii, segs=6, cap=True, flat=1.0):
    """Tube along a polyline; `flat` squashes the cross-section along the binormal."""
    pts, frames = _transport_frames(points)
    verts, faces = [], []
    for p, (t, n, b), r in zip(pts, frames, radii):
        for j in range(segs):
            a = TAU * j / segs
            v = p + n * (math.cos(a) * r) + b * (math.sin(a) * r * flat)
            verts.append(tuple(v))
    for i in range(len(pts) - 1):
        for j in range(segs):
            j2 = (j + 1) % segs
            a, b2 = i * segs, (i + 1) * segs
            faces.append((a + j, a + j2, b2 + j2, b2 + j))
    if cap:
        faces.append(tuple(reversed(range(segs))))
        last = (len(pts) - 1) * segs
        faces.append(tuple(range(last, last + segs)))
    return verts, faces


def blade(points, widths, thick, up=(0, 0, 1)):
    """Flat blade along a polyline: diamond cross-section, width along `up`."""
    pts = [Vector(p) for p in points]
    upv = Vector(up)
    verts, faces = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        t = (b - a).normalized()
        w = (upv - t * upv.dot(t)).normalized()
        side = t.cross(w)
        hw = widths[i] / 2
        verts += [tuple(p + w * hw), tuple(p + side * thick / 2), tuple(p - w * hw), tuple(p - side * thick / 2)]
    for i in range(len(pts) - 1):
        a, b2 = i * 4, (i + 1) * 4
        for j in range(4):
            j2 = (j + 1) % 4
            faces.append((a + j, b2 + j, b2 + j2, a + j2))
    faces.append((0, 1, 2, 3))
    last = (len(pts) - 1) * 4
    faces.append((last + 3, last + 2, last + 1, last))
    return verts, faces


class MeshKit:
    """Collects primitives into one mesh with vertex colours and rigid bone weights."""

    def __init__(self, bones=None):
        self.bm = bmesh.new()
        self.color = self.bm.loops.layers.float_color.new("Col")
        self.bones = list(bones or [])
        self.index = {n: i for i, n in enumerate(self.bones)}
        self.deform = self.bm.verts.layers.deform.verify() if self.bones else None
        # colour names drawn as other ones (a figure with skin of another colour)
        self.remap = {}
        # a transform put over everything added while it is set (a smaller head, a broader chest)
        self.pre = None

    # -- low level -------------------------------------------------------------
    def add(self, geom, color, bone=None, matrix=None, smooth=True, shade=1.0):
        verts, faces = geom
        m = matrix if matrix is not None else Matrix.Identity(4)
        if self.pre is not None:
            m = self.pre @ m
        bv = [self.bm.verts.new(m @ Vector(v)) for v in verts]
        if bone is not None:
            gi = self.index[bone]
            for v in bv:
                v[self.deform][gi] = 1.0
        c = linear(self.remap.get(color, color), shade)
        made = []
        for f in faces:
            try:
                face = self.bm.faces.new([bv[i] for i in f])
            except ValueError:
                continue
            face.smooth = smooth
            for loop in face.loops:
                loop[self.color] = c
            made.append(face)
        return made

    def solidify(self, faces, thickness, color, bone=None, shade=1.0):
        """Give an open surface a thickness (inner side faces inwards)."""
        # the offset follows the normals, so they must be up to date first
        self.bm.normal_update()
        res = bmesh.ops.solidify(self.bm, geom=faces, thickness=thickness)
        c = linear(color, shade)
        gi = self.index[bone] if bone is not None else None
        for ele in res["geom"]:
            if isinstance(ele, bmesh.types.BMFace):
                for loop in ele.loops:
                    loop[self.color] = c
            elif isinstance(ele, bmesh.types.BMVert) and gi is not None:
                dv = ele[self.deform]
                dv.clear()
                dv[gi] = 1.0

    # -- primitives -------------------------------------------------------------
    def lathe(self, center, profile, color, bone=None, segs=12, sx=1.0, sy=1.0,
              a0=0.0, a1=None, smooth=True, thickness=0.0, rot=None, shade=1.0, cap0=True, cap1=True):
        m = Matrix.Translation(Vector(center))
        if rot is not None:
            m = m @ rot
        faces = self.add(lathe(profile, segs, sx, sy, a0, a1, cap0, cap1), color, bone, m, smooth, shade)
        if thickness > 0:
            self.solidify(faces, thickness, color, bone, shade)
        return faces

    def along(self, p0, p1, profile, color, bone=None, segs=10, sx=1.0, sy=1.0, smooth=True,
              roll_hint=None, shade=1.0):
        """Lathe whose axis runs from p0 to p1; profile z is a fraction 0..1 of the length."""
        m, length = frame_along(p0, p1, roll_hint)
        prof = [(p[0] * length,) + tuple(p[1:]) for p in profile]
        return self.add(lathe(prof, segs, sx, sy), color, bone, m, smooth, shade)

    def tube(self, p0, p1, r0, r1, color, bone=None, segs=10, sx=1.0, sy=1.0, smooth=True, shade=1.0):
        return self.along(p0, p1, [(0.0, r0), (1.0, r1)], color, bone, segs, sx, sy, smooth, shade=shade)

    def ball(self, center, radii, color, bone=None, segs=12, rings=7, smooth=True, rot=None, shade=1.0):
        rx, ry, rz = radii if isinstance(radii, (tuple, list)) else (radii, radii, radii)
        m = Matrix.Translation(Vector(center))
        if rot is not None:
            m = m @ rot
        geom = lathe(ellipsoid_profile(rz, rings), segs, rx, ry)
        return self.add(geom, color, bone, m, smooth, shade)

    def box(self, center, size, color, bone=None, rot=None, taper=1.0, smooth=False, shade=1.0):
        m = Matrix.Translation(Vector(center))
        if rot is not None:
            m = m @ rot
        return self.add(box_geom(*size, taper=taper), color, bone, m, smooth, shade)

    def beam(self, p0, p1, w, h, color, bone=None, roll_hint=None, shade=1.0, smooth=False):
        """Box running from p0 to p1 with cross-section w x h."""
        m, length = frame_along(p0, p1, roll_hint)
        m = m @ Matrix.Translation((0, 0, length / 2))
        return self.add(box_geom(w, h, length), color, bone, m, smooth, shade)

    def sweep(self, points, radii, color, bone=None, segs=6, cap=True, flat=1.0, smooth=True, shade=1.0):
        return self.add(sweep(points, radii, segs, cap, flat), color, bone, None, smooth, shade)

    def blade(self, points, widths, thick, color, bone=None, up=(0, 0, 1), shade=1.0):
        return self.add(blade(points, widths, thick, up), color, bone, None, False, shade)

    def transform(self, matrix):
        """Moves everything built so far."""
        bmesh.ops.transform(self.bm, matrix=matrix, verts=self.bm.verts[:])

    # -- output -----------------------------------------------------------------
    def to_object(self, name, armature=None, collection=None):
        bmesh.ops.remove_doubles(self.bm, verts=[], dist=0.0)
        me = bpy.data.meshes.new(name)
        self.bm.normal_update()
        self.bm.to_mesh(me)
        self.bm.free()
        me.color_attributes.active_color_name = "Col"
        me.attributes.default_color_name = "Col"
        obj = bpy.data.objects.new(name, me)
        (collection or bpy.context.scene.collection).objects.link(obj)
        if armature is not None:
            for b in self.bones:
                obj.vertex_groups.new(name=b)
            obj.parent = armature
            mod = obj.modifiers.new("Armature", "ARMATURE")
            mod.object = armature
        mat = bpy.data.materials.get("painted") or bpy.data.materials.new("painted")
        me.materials.append(mat)
        return obj


def triangles(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)
