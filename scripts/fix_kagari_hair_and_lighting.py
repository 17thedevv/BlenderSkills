"""Fix Kagari hair accessories, remove cross-pins, fix shadow tearing, and refine side-ponytail."""
import bpy
import bmesh
import math
from mathutils import Vector, Matrix, Euler
from pathlib import Path

RECOVERY_BLEND = Path("outputs/wip/kagari_vroid_recovery.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/recovery")

bpy.ops.wm.open_mainfile(filepath=str(RECOVERY_BLEND))

# 1. Clean hair accessories (Slots 2, 3, 4, 5 on Hair)
hair = bpy.data.objects.get('Hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    
    # Delete faces in material slots 2, 3, 4, 5 (the cross-pins and star clips)
    faces_to_remove = [f for f in bm.faces if f.material_index in [2, 3, 4, 5]]
    print(f"Removing {len(faces_to_remove)} accessory faces from Hair")
    bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES_ONLY')
    
    # Also clean loose vertices
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    
    # For twintails: Left twintail is at X > 0.08, Z > 1.35
    # Remove left high twintail so only the right side ponytail remains
    left_twintail_faces = [f for f in bm.faces if all(v.co.x > 0.08 and v.co.z > 1.30 for v in f.verts)]
    print(f"Removing {len(left_twintail_faces)} left twintail faces")
    bmesh.ops.delete(bm, geom=left_twintail_faces, context='FACES_ONLY')
    
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()

# 2. Fix lighting & shadows: Soft diffuse anime studio lighting with no harsh shadow tearing
scene = bpy.context.scene

# Remove old harsh lights
for l in list(bpy.data.lights):
    bpy.data.lights.remove(l)

# Soft Studio World
if not scene.world:
    scene.world = bpy.data.worlds.new("Anime_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (1.0, 0.98, 0.96, 1.0)
    bg.inputs['Strength'].default_value = 1.2

# Front Key Light without cast shadows to avoid harsh slicing
key_data = bpy.data.lights.new(name="Soft_Front_Key", type='AREA')
key_data.energy = 40.0
key_data.size = 1.5
key_data.color = (1.0, 0.98, 0.95)
key_data.use_shadow = False  # Disable harsh shadow slicing on anime face!

key_obj = bpy.data.objects.new("Soft_Front_Key", key_data)
key_obj.location = (0.0, -1.2, 1.4)
scene.collection.objects.link(key_obj)

# Gentle rim light from rear
rim_data = bpy.data.lights.new(name="Soft_Rim", type='AREA')
rim_data.energy = 25.0
rim_data.size = 1.0
rim_data.color = (1.0, 0.95, 0.88)
rim_data.use_shadow = False
rim_obj = bpy.data.objects.new("Soft_Rim", rim_data)
rim_obj.location = (0.5, 0.8, 1.6)
scene.collection.objects.link(rim_obj)

# 3. Position Camera
cam = scene.camera
if not cam:
    cam_data = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

cam.data.lens = 85.0

def set_camera(pos, target=Vector((0.0, 0.0, 1.28))):
    cam.location = pos
    d = target - pos
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def render_view(filename):
    out = PREVIEWS_DIR / filename
    scene.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)
    print(f"SAVED: {out}")

print("Rendering Clean Front View...")
set_camera(Vector((0.0, -0.80, 1.28)))
render_view("recovery_front_clean.png")

print("Rendering Clean Face Close-up...")
set_camera(Vector((0.0, -0.52, 1.30)))
render_view("recovery_closeup_clean.png")

print("Rendering Clean Three-Quarter...")
set_camera(Vector((-0.45, -0.70, 1.30)))
render_view("recovery_three_quarter_clean.png")

bpy.ops.wm.save_as_mainfile(filepath=str(RECOVERY_BLEND))
print("SAVED: kagari_vroid_recovery.blend updated.")
