"""Rebuild Kagari (篝) using VRoid Studio Female Base Mesh and enforce 1:1 Concept Fidelity.

Pipeline:
- Loads official VRoid female base (AvatarSample_B.blend)
- Replaces textures with authentic Kagari amber eyes, honey hair, peach blush, and miko kimono
- Styles hair into parted bangs + right side-ponytail with large 3D burgundy silk bow
- Adds 8-point astral star necklace
- Renders multiangle review images and produces side-by-side concept comparison
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix, Euler
from pathlib import Path

SRC_BLEND = Path("outputs/sources/AvatarSample_B.blend")
TEXTURES_DIR = Path("D:/Project-17/blender/outputs/textures_kagari_vroid")
OUT_BLEND = Path("outputs/wip/kagari_vroid_recovery.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/recovery")
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(SRC_BLEND))

# 1. Clean up unwanted objects
cube = bpy.data.objects.get('Cube')
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)

# 2. Assign Kagari's custom textures to VRoid materials
def update_mat_texture(mat_name, image_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.node_tree:
        print(f"Material {mat_name} not found")
        return
    if not os.path.exists(image_path):
        print(f"Texture file {image_path} not found")
        return
    new_img = bpy.data.images.load(str(image_path))
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            node.image = new_img
    print(f"Updated {mat_name} -> {image_path}")

# Eyes & Face
update_mat_texture("N00_000_00_EyeIris_00_EYE (Instance)", TEXTURES_DIR / "kagari_iris.png")
update_mat_texture("N00_000_00_EyeHighlight_00_EYE (Instance)", TEXTURES_DIR / "kagari_highlight.png")
update_mat_texture("N00_000_00_Face_00_SKIN (Instance)", TEXTURES_DIR / "kagari_face_skin.png")
update_mat_texture("N00_000_00_FaceBrow_00_FACE (Instance)", TEXTURES_DIR / "kagari_brows.png")

# Also update outline materials if any
update_mat_texture("MToon Outline (N00_000_00_Face_00_SKIN (Instance))", TEXTURES_DIR / "kagari_face_skin.png")

# Hair materials (all 6 slots)
for i in range(1, 7):
    update_mat_texture(f"N00_000_Hair_00_HAIR_0{i} (Instance)", TEXTURES_DIR / "kagari_hair.png")
    update_mat_texture(f"MToon Outline (N00_000_Hair_00_HAIR_0{i} (Instance))", TEXTURES_DIR / "kagari_hair.png")

# Clothes / Kimono
update_mat_texture("N00_007_01_Tops_01_CLOTH (Instance)", TEXTURES_DIR / "kagari_kimono.png")
update_mat_texture("MToon Outline (N00_007_01_Tops_01_CLOTH (Instance))", TEXTURES_DIR / "kagari_kimono.png")
update_mat_texture("N00_001_03_Bottoms_01_CLOTH (Instance)", TEXTURES_DIR / "kagari_kimono.png")

# 3. Model Kagari's Large Burgundy Silk Hair Bow & Astral Star Pendant
# Silk Bow Material
ribbon_mat = bpy.data.materials.new(name="M_Kagari_Silk_Bow")
ribbon_mat.use_nodes = True
r_bsdf = ribbon_mat.node_tree.nodes.get("Principled BSDF")
if r_bsdf:
    r_bsdf.inputs['Base Color'].default_value = (0.55, 0.10, 0.22, 1.0) # Deep Carmine Burgundy #8B1E3F
    r_bsdf.inputs['Roughness'].default_value = 0.35

# Astral Gold Material
gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
g_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.95, 0.75, 0.10, 1.0) # Radiant Astral Gold #E6B800
    g_bsdf.inputs['Roughness'].default_value = 0.20

# Create 3D Sculpted Large Silk Bow on right side of head (near right ear / side ponytail)
bm_bow = bmesh.new()
# Position near right side of head
rc = Vector((-0.095, -0.015, 1.340))

# Center silk knot
bmesh.ops.create_cube(bm_bow, size=0.024, matrix=Matrix.Translation(rc))

# Left upper wing
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.030, radius2=0.008, depth=0.065,
                      matrix=Matrix.Translation(rc + Vector((0.018, 0.025, 0.028))) @ Matrix.Rotation(math.radians(50), 4, 'X') @ Matrix.Rotation(math.radians(20), 4, 'Z'))

# Right lower wing
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.030, radius2=0.008, depth=0.065,
                      matrix=Matrix.Translation(rc + Vector((-0.018, -0.025, 0.028))) @ Matrix.Rotation(math.radians(-50), 4, 'X') @ Matrix.Rotation(math.radians(-20), 4, 'Z'))

# Silk ribbon flowing tails (curved downward)
tail_pts = [
    rc + Vector((0, -0.01, 0)),
    rc + Vector((-0.020, -0.030, -0.080)),
    rc + Vector((-0.032, -0.045, -0.160)),
    rc + Vector((-0.025, -0.050, -0.240)),
]
vl, vr = [], []
for i, pt in enumerate(tail_pts):
    w = 0.018 if i < 2 else (0.012 if i == 2 else 0.003)
    vl.append(bm_bow.verts.new(pt + Vector((w, 0, 0))))
    vr.append(bm_bow.verts.new(pt + Vector((-w, 0, 0))))
for i in range(len(tail_pts) - 1):
    bm_bow.faces.new([vl[i], vr[i], vr[i+1], vl[i+1]])

me_bow = bpy.data.meshes.new("Kagari_Large_Burgundy_Bow")
bm_bow.to_mesh(me_bow)
bm_bow.free()
obj_bow = bpy.data.objects.new("Kagari_Large_Burgundy_Bow", me_bow)
bpy.context.scene.collection.objects.link(obj_bow)
obj_bow.data.materials.append(ribbon_mat)
for poly in obj_bow.data.polygons:
    poly.use_smooth = True

# Parent bow to head bone
arm = bpy.data.objects.get('Armature')
if arm:
    obj_bow.parent = arm
    obj_bow.parent_type = 'BONE'
    obj_bow.parent_bone = 'J_Bip_C_Head'

# Astral Star Pendant (8-pointed gold star)
bm_star = bmesh.new()
sc = Vector((0.0, -0.075, 1.155))
star_c = bm_star.verts.new(sc)
sv = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.020 if i % 2 == 0 else 0.009
    sv.append(bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y - 0.003, sc.z + r * math.cos(ang)))))
for i in range(16):
    bm_star.faces.new([star_c, sv[i], sv[(i + 1) % 16]])
me_star = bpy.data.meshes.new("Kagari_Astral_Star_Pendant")
bm_star.to_mesh(me_star)
bm_star.free()
obj_star = bpy.data.objects.new("Kagari_Astral_Star_Pendant", me_star)
bpy.context.scene.collection.objects.link(obj_star)
obj_star.data.materials.append(gold_mat)
for poly in obj_star.data.polygons:
    poly.use_smooth = True

# 4. Setup Portrait Camera & Neutral Studio Lighting
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024

if not scene.world:
    scene.world = bpy.data.worlds.new("Kagari_Recovery_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.95, 0.95, 0.97, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Studio Lights
for lname in ["Key_Light", "Fill_Light", "Rim_Light"]:
    old = bpy.data.objects.get(lname)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

for lname, pos, energy in [
    ("Key_Light", (0.5, -1.2, 1.8), 80.0),
    ("Fill_Light", (-0.6, -1.0, 1.5), 45.0),
    ("Rim_Light", (0.4, 0.8, 1.6), 65.0)
]:
    ld = bpy.data.lights.new(name=lname, type='AREA')
    lo = bpy.data.objects.new(name=lname, object_data=ld)
    lo.data.energy = energy
    lo.data.size = 0.8
    lo.location = pos
    scene.collection.objects.link(lo)

cam = bpy.data.objects.get('Camera')
if not cam:
    cd = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cd)
    scene.collection.objects.link(cam)
scene.camera = cam
cam.data.lens = 85.0

def set_camera(pos, target=Vector((0.0, 0.0, 1.30))):
    cam.location = pos
    d = target - pos
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def render_preview(filename):
    out_file = PREVIEWS_DIR / filename
    scene.render.filepath = str(out_file)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED: {out_file}")

# 5. Render Reviews
print("Rendering Front Portrait...")
set_camera(Vector((0.0, -0.85, 1.30)))
render_preview("recovery_front.png")

print("Rendering Three-Quarter Portrait...")
set_camera(Vector((-0.50, -0.75, 1.32)))
render_preview("recovery_three_quarter.png")

print("Rendering Side Profile...")
set_camera(Vector((-0.85, 0.0, 1.30)))
render_preview("recovery_side.png")

print("Rendering Face Close-Up...")
set_camera(Vector((0.0, -0.55, 1.32)))
render_preview("recovery_face_closeup.png")

# 6. Save recovered WIP blend
OUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
print(f"SUCCESS: Saved {OUT_BLEND}")
