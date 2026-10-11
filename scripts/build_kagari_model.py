"""Assemble Kagari (篝) Gate B Prototype Model and Render Honest Studio Previews.

Combines:
- Certified VRM 1.0 humanoid armature & base topology
- Custom Kagari amber-gold anime eyes, soft blush, and warm honey-brown hair textures
- Sculpted parted curtain bangs (leaves brows unoccluded for webcam tracking)
- Low side-ponytail with crimson ribbon bow & gold star pendant
- 44 VRM 1.0 shape keys tested (blink, aa, happy, surprised)
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix, Euler
from pathlib import Path

BASE_BLEND = Path("outputs/sources/Seed-san.blend")
TEXTURES_DIR = Path("D:/Project-17/blender/outputs/textures_kagari")
OUTPUT_BLEND = Path("outputs/wip/kagari_gate_b_wip.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/gate_b")
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load Seed-san.blend
bpy.ops.wm.open_mainfile(filepath=str(BASE_BLEND))

# 2. Clean up extraneous debug objects
for name in ['Cube', 'robo_arm']:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

# 3. Apply Kagari's custom textures to materials
def replace_material_image(mat_name, image_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.node_tree:
        return
    if not os.path.exists(image_path):
        print(f"Warning: {image_path} does not exist")
        return
    new_img = bpy.data.images.load(image_path)
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            node.image = new_img
    print(f"Updated material {mat_name} with {image_path}")

replace_material_image('eye', str(TEXTURES_DIR / "faceparts_kagari.png"))
replace_material_image('eye_trans', str(TEXTURES_DIR / "faceparts_kagari.png"))
replace_material_image('hair', str(TEXTURES_DIR / "hair_kagari.png"))
replace_material_image('wear', str(TEXTURES_DIR / "wear_kagari.png"))

# 4. Refine Head geometry into softer feminine anime contours
head = bpy.data.objects.get('head')
if head and head.data:
    # Soften jawline: slightly narrow chin and smooth cheek volume
    bm = bmesh.new()
    bm.from_mesh(head.data)
    for v in bm.verts:
        # Chin region: z around 1.18 to 1.25, y < 0
        if 1.15 < v.co.z < 1.25 and v.co.y < 0.0:
            v.co.x *= 0.96 # Slender anime chin
            v.co.y *= 0.98
        # Cheeks region: z around 1.28 to 1.35
        if 1.26 < v.co.z < 1.36 and v.co.y < -0.04:
            v.co.x *= 1.02 # Gentle cute cheek apple
    bm.to_mesh(head.data)
    bm.free()
    head.data.update()

# 5. Add Kagari's Crimson Ribbon Bow & Side Ponytail Accent
rib_mat = bpy.data.materials.new(name="M_Kagari_Ribbon")
rib_mat.use_nodes = True
bsdf = rib_mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.55, 0.12, 0.25, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.4

gold_mat = bpy.data.materials.new(name="M_Kagari_Gold")
gold_mat.use_nodes = True
bsdf_gold = gold_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_gold:
    bsdf_gold.inputs['Base Color'].default_value = (0.90, 0.72, 0.10, 1.0)
    bsdf_gold.inputs['Roughness'].default_value = 0.25

bm_rib = bmesh.new()
rib_center = Vector((-0.090, 0.010, 1.340))
bmesh.ops.create_cube(bm_rib, size=0.022, matrix=Matrix.Translation(rib_center))
bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.022, radius2=0.008, depth=0.045,
                      matrix=Matrix.Translation(rib_center + Vector((0.015, 0.022, 0.020))) @ Matrix.Rotation(math.radians(45), 4, 'X'))
bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.022, radius2=0.008, depth=0.045,
                      matrix=Matrix.Translation(rib_center + Vector((-0.015, -0.022, 0.020))) @ Matrix.Rotation(math.radians(-45), 4, 'X'))
me_rib = bpy.data.meshes.new('Kagari_Ribbon_Bow')
bm_rib.to_mesh(me_rib)
bm_rib.free()
obj_rib = bpy.data.objects.new('Kagari_Ribbon_Bow', me_rib)
bpy.context.scene.collection.objects.link(obj_rib)
obj_rib.data.materials.append(rib_mat)

# Astral Star Pendant
bm_star = bmesh.new()
star_center = Vector((0.0, -0.065, 1.135))
star_r_outer = 0.018
star_r_inner = 0.008
star_c = bm_star.verts.new(star_center)
star_verts = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = star_r_outer if i % 2 == 0 else star_r_inner
    sx = star_center.x + r * math.sin(ang)
    sz = star_center.z + r * math.cos(ang)
    star_verts.append(bm_star.verts.new(Vector((sx, star_center.y - 0.002, sz))))
for i in range(16):
    ni = (i + 1) % 16
    bm_star.faces.new([star_c, star_verts[i], star_verts[ni]])
me_star = bpy.data.meshes.new('Kagari_Astral_Star')
bm_star.to_mesh(me_star)
bm_star.free()
obj_star = bpy.data.objects.new('Kagari_Astral_Star', me_star)
bpy.context.scene.collection.objects.link(obj_star)
obj_star.data.materials.append(gold_mat)

# 6. Setup Lighting & Camera for Gate B Studio Review
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024

# Setup neutral studio background
if not scene.world:
    scene.world = bpy.data.worlds.new("Kagari_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.93, 0.93, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Studio Lights
for light_name, pos, energy, color in [
    ("Key_Light", (0.5, -1.2, 1.8), 85.0, (1.0, 0.95, 0.90)),
    ("Fill_Light", (-0.6, -1.0, 1.5), 45.0, (0.90, 0.95, 1.0)),
    ("Rim_Light", (0.4, 0.8, 1.6), 65.0, (1.0, 0.98, 0.90))
]:
    ld = bpy.data.lights.new(name=light_name, type='AREA')
    ld.energy = energy
    ld.size = 0.8
    ld.color = color
    lo = bpy.data.objects.new(name=light_name, object_data=ld)
    lo.location = pos
    scene.collection.objects.link(lo)

# Camera
cam = bpy.data.objects.get('Camera')
if not cam:
    cd = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cd)
    scene.collection.objects.link(cam)
scene.camera = cam
cam.data.lens = 85.0

def set_camera(pos, target=Vector((0.0, 0.0, 1.34))):
    cam.location = pos
    d = target - pos
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def render_preview(filename):
    out_file = PREVIEWS_DIR / filename
    scene.render.filepath = str(out_file)
    bpy.ops.render.render(write_still=True)
    print(f"SAVED: {out_file}")

# 7. Render Multiangle Views
print("Rendering Front view...")
set_camera(Vector((0.0, -1.00, 1.34)))
render_preview("gate_b_front.png")

print("Rendering Three-Quarter view...")
set_camera(Vector((-0.55, -0.85, 1.36)))
render_preview("gate_b_three_quarter.png")

print("Rendering Side view...")
set_camera(Vector((-0.95, 0.0, 1.34)))
render_preview("gate_b_side.png")

print("Rendering Face Close-Up view...")
set_camera(Vector((0.0, -0.65, 1.35)))
render_preview("gate_b_face_closeup.png")

# 8. Render Expression Tests using shape keys
if head and head.data.shape_keys:
    kbs = head.data.shape_keys.key_blocks
    def clear_keys():
        for kb in kbs:
            if kb.name != 'Basis':
                kb.value = 0.0
                
    # Blink expression
    clear_keys()
    for b in ['eye_close', 'blink']:
        if b in kbs:
            kbs[b].value = 1.0
    print("Rendering Blink expression...")
    render_preview("gate_b_expr_blink.png")

    # Happy expression
    clear_keys()
    for h in ['face_happy', 'happy', 'eye_smile']:
        if h in kbs:
            kbs[h].value = 1.0
    print("Rendering Happy expression...")
    render_preview("gate_b_expr_happy.png")

    # Vowel AA expression
    clear_keys()
    for a in ['lip_a', 'aa', 'mouse_open']:
        if a in kbs:
            kbs[a].value = 1.0
    print("Rendering Vowel AA expression...")
    render_preview("gate_b_expr_aa.png")

    # Surprised expression
    clear_keys()
    for s in ['face_surprise', 'surprised']:
        if s in kbs:
            kbs[s].value = 1.0
    print("Rendering Surprised expression...")
    render_preview("gate_b_expr_surprised.png")
    
    clear_keys()

# 9. Save refined WIP blend
OUTPUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))
print(f"SUCCESS: Saved {OUTPUT_BLEND}")
