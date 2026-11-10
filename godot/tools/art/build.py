"""Builds the game's 3D art: people, weapons and the shared animation clips.

    pip install bpy==5.*            # Blender as a Python module
    git clone https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0 kaykit
    python godot/tools/art/build.py --kaykit kaykit --out godot/client/assets/art

Outputs (glTF binary, Y up):
    characters/<name>.glb   skinned body + default weapons, no clips
    characters/humanoid_clips.glb   skeleton with every clip (one library for all people)
    characters/weapons.glb  every weapon on its hand bone
    props/<name>.glb        environment pieces (see props.py)
    portraits/busts.glb     with --portraits: the busts of the portraits (see portraits.py)
    characters/divchyna.glb with --story: the people only the story pictures have (portraits.py)
--only NAMES builds just those people (characters/<name>.glb), e.g. --only upyr.
--props NAMES builds just those environment pieces (props/<name>.glb), e.g. --props brama,vorota;
    it needs no --kaykit.
--preview FILE renders a line-up of everyone with Cycles for a quick look.
"""

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import characters  # noqa: E402
import hero  # noqa: E402
import mesh_kit  # noqa: E402
import portraits  # noqa: E402
import props  # noqa: E402
import rig  # noqa: E402
import weapons  # noqa: E402

LOADOUT = {
    "kozak": ["sabre"],
    "kozak_hero": ["sabre"],
    "kozak_camp": [],
    "kozak_svyta": [],
    "zholner": ["sabre", "shield"],
    "luchnyk": ["bow"],
    "polkovnyk": ["bulava"],
    # the hero's classes take their blade in the game (sabre or palash)
    "serdiuk": [],
    "kharakternyk": [],
    "haidamaka": [],
    "kozak_rival": ["sabre"],
    "kozak_rival_luk": ["bow"],
    "tatar": ["sabre", "kalkan"],
    "tatar_luk": ["bow"],
    "rotmistr": ["sabre_gold"],
    "murza": ["sabre_gold"],
    "upyr": ["bulava"],
}


PEOPLE = list(characters.RECIPES) + list(hero.RECIPES)


def build_person(name, bones, arm):
    """The body of a person: the hero's Cossack from hero.py, everyone else from characters.py."""
    return (hero if name in hero.RECIPES else characters).build(name, bones, rig.DEFORM, arm)


def _select(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]


def export(path, objs, clips=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _select(objs)
    bpy.ops.export_scene.gltf(
        filepath=path, export_format="GLB", use_selection=True, export_yup=True,
        export_apply=False, export_animations=clips, export_animation_mode="ACTIONS",
        export_vertex_color="ACTIVE", export_all_vertex_colors=False, export_normals=True,
        export_texcoords=False, export_materials="EXPORT", export_image_format="NONE",
        export_skins=True, export_def_bones=False, export_force_sampling=True,
        export_optimize_animation_size=True, export_reset_pose_bones=True,
        export_rest_position_armature=True, export_extras=False)


def painted_material():
    mat = bpy.data.materials.get("painted") or bpy.data.materials.new("painted")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    attr = nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "Col"
    nt.links.new(attr.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.9
    return mat


def build_people(arm, bones, out, names=None):
    report = []
    for name in names or PEOPLE:
        body = build_person(name, bones, arm)
        held = [weapons.build(w, bones, arm) for w in LOADOUT[name]]
        export(f"{out}/characters/{name}.glb", [arm, body] + held)
        tris = mesh_kit.triangles(body) + sum(mesh_kit.triangles(h) for h in held)
        report.append((name, tris))
        for o in [body] + held:
            bpy.data.objects.remove(o, do_unlink=True)
    if names:
        return report
    held = [weapons.build(w, bones, arm) for w in weapons.SLOTS]
    export(f"{out}/characters/weapons.glb", [arm] + held)
    for o in held:
        report.append((o.name, mesh_kit.triangles(o)))
        bpy.data.objects.remove(o, do_unlink=True)
    rig.strip_for_export(arm, with_clips=False)
    export(f"{out}/characters/humanoid_clips.glb", [arm], clips=True)
    return report


def preview(arm, bones, path, pose="idle", frame=8, spacing=1.45):
    painted_material()
    scene = bpy.context.scene
    names = PEOPLE
    for i, name in enumerate(names):
        a = arm.copy()
        a.data = arm.data
        scene.collection.objects.link(a)
        a.location = Vector(((i - (len(names) - 1) / 2) * spacing, 0, 0))
        act = bpy.data.actions[pose]
        a.animation_data_create()
        a.animation_data.action = act
        if act.slots:
            a.animation_data.action_slot = act.slots[0]
        body = build_person(name, bones, a)
        for w in LOADOUT[name]:
            weapons.build(w, bones, a)
    for p in props.preview_set():
        pass
    scene.frame_set(frame)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    scene.collection.objects.link(cam)
    cam.data.lens = 50
    dist = 11.5
    pitch = math.radians(28)
    yaw = math.radians(12)
    cam.location = (dist * math.cos(pitch) * math.sin(yaw), -dist * math.cos(pitch) * math.cos(yaw), 1.0 + dist * math.sin(pitch))
    cam.rotation_euler = (math.radians(90) - pitch, 0, yaw)
    scene.camera = cam
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.5
    sun.data.color = (1.0, 0.93, 0.82)
    sun.rotation_euler = (math.radians(50), math.radians(-25), math.radians(-35))
    scene.collection.objects.link(sun)
    world = bpy.data.worlds.new("w")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.62, 0.75, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    scene.world = world
    ground = bpy.data.meshes.new("ground")
    ground.from_pydata([(-8, -8, 0), (8, -8, 0), (8, 8, 0), (-8, 8, 0)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("ground", ground)
    gm = bpy.data.materials.new("g")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.58, 0.45, 0.22, 1)
    ground.materials.append(gm)
    scene.collection.objects.link(g)
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.cycles.device = "CPU"
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 760
    scene.render.filepath = path
    scene.view_settings.view_transform = "Standard"
    bpy.ops.render.render(write_still=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaykit")
    ap.add_argument("--out", default="godot/client/assets/art")
    ap.add_argument("--preview")
    ap.add_argument("--pose", default="idle")
    ap.add_argument("--frame", type=int, default=8)
    ap.add_argument("--skip-export", action="store_true")
    ap.add_argument("--portraits", action="store_true")
    ap.add_argument("--story", action="store_true")
    ap.add_argument("--only", help="build only these people (comma-separated), nothing else")
    ap.add_argument("--props", help="build only these environment pieces (comma-separated), nothing else")
    args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
    if args.props:
        painted_material()
        for name in args.props.split(","):
            obj = props.build_one(name)
            export(f"{args.out}/props/{name}.glb", [obj])
            print(f"{name:16s} {mesh_kit.triangles(obj):6d} tris")
            bpy.data.objects.remove(obj, do_unlink=True)
        return
    if not args.kaykit:
        ap.error("--kaykit is needed for the people")
    arm = rig.load(args.kaykit)
    bones = rig.bones(arm)
    painted_material()
    if args.story:
        for name, faces in portraits.build_story_people(arm, bones, rig.DEFORM, args.out, export):
            print(f"{name:16s} {faces:6d} faces")
    if args.portraits:
        for name, faces in portraits.build_busts(arm, bones, rig.DEFORM, args.out, export):
            print(f"{name:16s} {faces:6d} faces")
    if args.only:
        for name, tris in build_people(arm, bones, args.out, args.only.split(",")):
            print(f"{name:16s} {tris:6d} tris")
    elif not args.skip_export:
        for name, tris in build_people(arm, bones, args.out):
            print(f"{name:16s} {tris:6d} tris")
        for name, tris in props.build_all(args.out, export):
            print(f"{name:16s} {tris:6d} tris")
    if args.preview:
        preview(arm, bones, args.preview, args.pose, args.frame)


if __name__ == "__main__":
    main()
