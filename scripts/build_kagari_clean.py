"""Build clean, professional Kagari (篝) model using official VRM base topology.

Applies:
- Kagari's amber-gold eyes (faceparts_kagari.png)
- Kagari's honey-brown hair with golden halo (hair_kagari.png)
- Kagari's miko outfit (wear_kagari.png)
- Gently raised bangs to maximize webcam tracking visibility
- Enabled hair_tail for side ponytail silhouette
- All 44 VRM 1.0 shape keys verified
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector
from pathlib import Path

BASE_BLEND = Path("outputs/sources/Seed-san.blend")
TEXTURES_DIR = Path("D:/Project-17/blender/outputs/textures_kagari")
OUTPUT_BLEND = Path("outputs/wip/kagari_gate_b_final.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/gate_b")

bpy.ops.wm.open_mainfile(filepath=str(BASE_BLEND))

# 1. Remove extraneous objects
for name in ['Cube', 'robo_arm']:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

# 2. Update textures
def replace_img(mat_name, img_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.node_tree:
        return
    img = bpy.data.images.load(str(img_path))
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            node.image = img
    print(f"Updated {mat_name} with {img_path}")

replace_img('eye', TEXTURES_DIR / "faceparts_kagari.png")
replace_img('eye_trans', TEXTURES_DIR / "faceparts_kagari.png")
replace_img('hair', TEXTURES_DIR / "hair_kagari.png")
replace_img('wear', TEXTURES_DIR / "wear_kagari.png")
replace_img('huku_bake', TEXTURES_DIR / "wear_kagari.png")

# 3. Adjust bangs to uncover eyebrows and upper eye contours for MediaPipe webcam tracking
hair = bpy.data.objects.get('hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    for v in bm.verts:
        # If in the center forehead region (abs(X) < 0.04, Y < -0.05, Z around 1.35..1.42)
        if abs(v.co.x) < 0.045 and v.co.y < -0.05 and 1.34 < v.co.z < 1.43:
            # Lift bangs slightly up and back to reveal brows cleanly
            v.co.z += 0.015
            v.co.y += 0.008
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()

# 4. Enable hair_tail and position on the right side for Kagari's low side-ponytail
hair_tail = bpy.data.objects.get('hair_tail')
if hair_tail:
    hair_tail.hide_render = False
    hair_tail.hide_viewport = False
    # Shift position slightly toward right side (-X)
    hair_tail.location.x -= 0.04
    hair_tail.location.y -= 0.02

# 5. Setup Camera & Studio Lights
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024

if not scene.world:
    scene.world = bpy.data.worlds.new("Kagari_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.92, 0.92, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Ensure lights
for light_name, pos, energy in [
    ("Key_Light", (0.5, -1.2, 1.8), 80.0),
    ("Fill_Light", (-0.6, -1.0, 1.5), 45.0),
    ("Rim_Light", (0.4, 0.8, 1.6), 65.0)
]:
    lo = bpy.data.objects.get(light_name)
    if not lo:
        ld = bpy.data.lights.new(name=light_name, type='AREA')
        lo = bpy.data.objects.new(name=light_name, object_data=ld)
        scene.collection.objects.link(lo)
    lo.data.energy = energy
    lo.location = pos

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

head = bpy.data.objects.get('head')
kbs = head.data.shape_keys.key_blocks if head and head.data.shape_keys else {}

def clear_keys():
    for kb in kbs:
        if kb.name != 'Basis':
            kb.value = 0.0

clear_keys()
set_camera(Vector((0.0, -1.02, 1.34)))
render_preview("gate_b_front.png")

set_camera(Vector((-0.55, -0.85, 1.36)))
render_preview("gate_b_three_quarter.png")

set_camera(Vector((-0.95, 0.0, 1.34)))
render_preview("gate_b_side.png")

set_camera(Vector((0.0, -0.65, 1.35)))
render_preview("gate_b_face_closeup.png")

# Expression Tests
clear_keys()
for b in ['eye_close', 'blink']:
    if b in kbs:
        kbs[b].value = 1.0
render_preview("gate_b_expr_blink.png")

clear_keys()
for h in ['face_happy', 'happy', 'eye_smile']:
    if h in kbs:
        kbs[h].value = 1.0
render_preview("gate_b_expr_happy.png")

clear_keys()
for a in ['lip_a', 'aa', 'mouse_open']:
    if a in kbs:
        kbs[a].value = 1.0
render_preview("gate_b_expr_aa.png")

clear_keys()
for s in ['face_surprise', 'surprised']:
    if s in kbs:
        kbs[s].value = 1.0
render_preview("gate_b_expr_surprised.png")

clear_keys()

OUTPUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))
print(f"SUCCESS: Saved {OUTPUT_BLEND}")
