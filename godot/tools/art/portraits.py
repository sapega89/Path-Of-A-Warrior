"""The portraits of the game: busts of the people as wooden figures of the new art.

Each of the 42 portraits (the numbers the game's data use: generals, colonels, the master's
people, the hero's four classes) gets its own recipe in the words of characters.py (a hat,
hair, a face, a coat), most of them a variation of a figure that fights on the maps, so a
colonel looks on his portrait as he looks in the mission. `side` picks the colour of the
portrait's backdrop; `look` turns the head (degrees, + to the viewer's right).

`build_story_people()` exports the people only the story pictures have (characters/<name>.glb,
rigged as the people of the maps; the Godot tool godot/client/tools/story_pictures.tscn poses
them). `build_busts()` builds every bust in the idle pose without legs, bakes the pose and writes
them as static meshes into one file, portraits/busts.glb (bust_<number>), with
portraits/busts.json (each one's side and turn of the head); the Godot tool
godot/client/tools/portraits.tscn paints each with the game's shaders into
portraits/<number>.png.
"""

import json
import os

import characters

R = characters.RECIPES


def like(base, **changes):
    r = dict(R[base])
    r.update(changes)
    return r


GOLD_SASH = characters.FACTIONS["hetman"]

## The girl of the story (Oksana, Marusia): a wreath of flowers, a braid, coral beads, a red
## vest over a long white shirt, red boots.
OKSANA = {"hat": "vinok", "hair": "hair_blond", "hair_cap": True, "braid": True, "face": "none",
          "lips": True, "nose": 0.75, "namysto": True, "coat": "whitewash", "coat_trim": "cinnabar",
          "coat_len": "long", "vest": "cinnabar", "sash": "cinnabar", "trousers": "whitewash",
          "boots": "cinnabar"}

## People who are only in the story pictures, not on the maps: characters/<name>.glb as the
## people of characters.py, without weapons.
STORY_PEOPLE = {"divchyna": OKSANA}

PORTRAITS = {
    # anyone without a face of his own: a messenger, a Cossack of the ranks
    0: (like("kozak_rival", sash=GOLD_SASH, hair="hair_brown", coat="stone_dark"), "plain"),
    1: (like("kozak_camp", hair="hair", face="long_mustache", earring=True, coat="blue_dark",
             coat_trim="blue", coat_len="knee", sash=GOLD_SASH), "cossack"),            # Osaul Zalizo
    2: (like("kozak_camp", hair="hair_brown", coat="wood_dark", coat_trim="fur", coat_len="knee",
             collar="fur", sash=GOLD_SASH), "cossack"),                                    # Hrebinka
    3: (like("rotmistr", hat_cloth="blue_dark", hair="hair_blond", face="short_mustache",
             coat="blue", undercoat="whitewash"), "crown"),                                  # Wilczek
    4: (like("polkovnyk", hat="kuchma", hat_fur="fur", hair="hair", coat="crimson",
             undercoat="gold"), "cossack"),                                                  # Zaderykhvist
    5: (like("kozak", hat_cloth="oak", hair="hair_red", coat="canvas", coat_trim="canvas_dark"), "cossack"),
    6: (like("rotmistr", hat=None, hair="hair", hair_cap=True, earring=True, collar="fur_grey"), "crown"),  # Zaremba
    7: (like("polkovnyk", hat="shlyk", hat_cloth="oak", hair="hair_blond", coat="oak_dark", undercoat="gold"), "cossack"),
    8: (like("rotmistr", hair="hair_white", beard=True, collar="fur"), "crown"),            # Grabowski
    9: (like("kozak_svyta", hat_fur="fur_grey", hair="hair_grey", beard="long", coat="stone_dark"), "cossack"),
    10: (like("kozak_camp", hair="hair_brown", face="long_mustache", scar=True, coat="cinnabar_dark",
              coat_trim="cinnabar", coat_len="knee", sash=GOLD_SASH), "cossack"),         # Shram
    11: (like("luchnyk", hat_cloth="blue", hair="hair", coat="blue_light", coat_trim="blue",
              sash=GOLD_SASH, quiver=False), "cossack"),                                    # Tymish
    12: (like("murza", hat="tatar", hat_cloth="crimson", hair="hair"), "horde"),            # Kara-murza
    13: (like("serdiuk", hair="hair_brown"), "cossack"),
    14: (like("haidamaka", hat=None, hair="hair_brown", hair_cap=True, beard=True, vest="fur_grey",
              belly=1.15), "cossack"),                                                      # Kozhumiaka
    15: (like("haidamaka", hat_cloth="blue", hair="hair", scar=True, coat="stone",
              coat_trim="stone_dark", vest=None), "cossack"),                               # Chupryna
    16: (like("serdiuk", hair="hair_grey", face="long_mustache", coat="cinnabar_dark"), "cossack"),
    17: (like("zholner", hair="hair_red", face="mustache", sash=GOLD_SASH), "cossack"),    # Sukhovii
    18: (like("kozak_rival", hair="hair", face="short_mustache", coat="blue", sash=GOLD_SASH), "cossack"),
    19: (like("tatar", hat_cloth="oak_dark", hair="hair_red"), "horde"),                   # Sefer-aga
    20: (like("serdiuk", hair="hair_brown", beard=True, coat="blue_dark"), "cossack"),     # Ruban
    21: (like("zholner", hair="hair"), "crown"),
    22: (like("rotmistr", hat_cloth="blue", hair="hair_brown", coat="blue_dark"), "crown"),
    23: (like("luchnyk", hair="hair_brown", face="mustache", quiver=False), "crown"),
    24: (like("kozak_svyta", hat_fur="fur_grey", hair="hair_grey", face="long_mustache", beard=True,
              coat="blue"), "cossack"),                                                     # Tykhyi
    25: (like("polkovnyk", hat_cloth="blue", hair="hair_white", coat="cinnabar", undercoat="blue"), "cossack"),
    26: (like("haidamaka", hat_cloth="oak", hair="hair", coat="canvas", vest=None), "cossack"),
    27: (like("murza", hair="hair", coat="oak_dark"), "horde"),                             # Aslan-murza
    28: (like("kozak_camp", hair="hair_grey", scar=True, coat="stone", coat_trim="stone_dark",
              coat_len="knee", sash=GOLD_SASH), "cossack"),
    29: (like("kozak", hat_cloth="blue", hair="hair", coat="blue_dark", coat_trim="blue"), "cossack"),
    30: (like("luchnyk", hat_cloth="wood_dark", hair="hair_brown", face="mustache", beard=True,
              coat="leather", coat_trim="wood_dark", sash=GOLD_SASH, quiver=False), "cossack"),
    31: (like("polkovnyk", hat_cloth="oak", hair="hair_grey", beard=True, coat="oak_dark"), "cossack"),  # Kosach
    32: (like("polkovnyk", hat_cloth="chernozem", hair="hair", coat="dusk", undercoat="cinnabar"), "cossack"),  # Voron
    33: (dict(R["polkovnyk"]), "cossack"),                                                   # Bairak
    34: (like("polkovnyk", hat="kuchma", hat_fur="fur", hair="hair", beard=True, coat="blue_dark",
              undercoat="gold"), "cossack"),                                                # Chornohuz
    35: (like("polkovnyk", hat="kuchma", hat_fur="fur_grey", hair="hair_white", coat="crimson",
              undercoat="gold"), "cossack"),                                                # Bilous
    36: (like("kozak", hat_cloth="cinnabar_dark", hair="hair_red", face="long_mustache", earring=True,
              coat="wood_dark", coat_trim="fur"), "cossack"),                               # Rudyi
    37: (dict(OKSANA), "cossack"),
    # the hero's classes (Profile.HERO_CLASSES), as he is on the map
    38: (dict(R["kozak"]), "hero"),
    39: (dict(R["serdiuk"]), "hero"),
    40: (dict(R["kharakternyk"]), "hero"),
    41: (dict(R["haidamaka"]), "hero"),
}

## How far each bust turns from the viewer (degrees, + to the viewer's right, towards the hero
## on the right of a talk); the hero looks the other way, to the one he talks to.
LOOK = {pid: (-24 if PORTRAITS[pid][1] == "hero" else 24) for pid in PORTRAITS}


def build_story_people(arm, bones, deform, out, export):
    """The story pictures' own people, rigged as the others, into <out>/characters/."""
    import bpy

    report = []
    for name, recipe in STORY_PEOPLE.items():
        body = characters.Figure(bones, deform).build(recipe).to_object(name, arm)
        export(f"{out}/characters/{name}.glb", [arm, body])
        report.append((name, len(body.data.polygons)))
        bpy.data.objects.remove(body, do_unlink=True)
    return report


def build_busts(arm, bones, deform, out, export, pose="idle", frame=8):
    """Every portrait's bust, posed and baked, into <out>/portraits/busts.glb."""
    import bpy

    act = bpy.data.actions[pose]
    ad = arm.animation_data or arm.animation_data_create()
    ad.action = act
    if act.slots:
        ad.action_slot = act.slots[0]
    bpy.context.scene.frame_set(frame)
    made = []
    for pid, (recipe, _) in PORTRAITS.items():
        fig = characters.Figure(bones, deform)
        posed = fig.build(recipe, legs=False).to_object(f"posed_{pid}", arm)
        dg = bpy.context.evaluated_depsgraph_get()
        mesh = bpy.data.meshes.new_from_object(posed.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        bpy.data.objects.remove(posed, do_unlink=True)
        mesh.name = f"bust_{pid}"
        mesh.color_attributes.active_color_name = "Col"
        bust = bpy.data.objects.new(f"bust_{pid}", mesh)
        bpy.context.scene.collection.objects.link(bust)
        made.append(bust)
    ad.action = None
    export(f"{out}/portraits/busts.glb", made)
    with open(os.path.join(out, "portraits", "busts.json"), "w") as f:
        json.dump({str(pid): {"side": side, "look": LOOK[pid]} for pid, (_, side) in PORTRAITS.items()},
                  f, indent=1, sort_keys=True)
    report = [(o.name, len(o.data.polygons)) for o in made]
    for o in made:
        bpy.data.objects.remove(o, do_unlink=True)
    return report
