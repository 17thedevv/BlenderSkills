"""Renders Kagari Gate B review previews: Multiangle and Expression verification."""
import bpy
import math
from mathutils import Vector, Euler
from pathlib import Path

OUTPUT_DIR = Path("outputs/previews/gate_b")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024 # 3:4 portrait aspect ratio
scene.render.film_transparent = False

# Ensure background world color is clean soft studio grey
if not scene.world:
    scene.world = bpy.data.worlds.new("Studio_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.92, 0.92, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 1.0

cam = scene.camera
if not cam:
    cam_data = bpy.data.cameras.new("Cam_Render")
    cam = bpy.data.objects.new("Cam_Render", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

cam.data.lens = 85.0
target = Vector((0.0, 0.0, 1.34)) # Face center target

def set_camera_view(pos, target_pt=target):
    cam.location = pos
    direction = target_pt - pos
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

def render_image(filename):
    out_path = OUTPUT_DIR / filename
    scene.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED: {out_path}")
    return str(out_path)

# 1. Front View
set_camera_view(Vector((0.0, -1.02, 1.34)))
render_image("gate_b_front.png")

# 2. Three-Quarter View (Flattering 30 deg angle)
set_camera_view(Vector((-0.52, -0.88, 1.36)))
render_image("gate_b_three_quarter.png")

# 3. Side Profile View
set_camera_view(Vector((-1.00, 0.0, 1.34)))
render_image("gate_b_side.png")

# 4. Face Close-Up (Framing mouth to brows for detail review)
set_camera_view(Vector((0.0, -0.62, 1.34)))
render_image("gate_b_face_closeup.png")

# Expression Renders (using shape keys on Kagari_Head)
head_obj = bpy.data.objects.get("Kagari_Head")
if head_obj and head_obj.data.shape_keys:
    key_blocks = head_obj.data.shape_keys.key_blocks
    
    def reset_shape_keys():
        for kb in key_blocks:
            if kb.name != 'Basis':
                kb.value = 0.0
                
    # 5. Blink Test
    reset_shape_keys()
    if 'blink' in key_blocks:
        key_blocks['blink'].value = 1.0
    set_camera_view(Vector((0.0, -0.62, 1.34)))
    render_image("gate_b_expr_blink.png")
    
    # 6. Happy / Smile Test
    reset_shape_keys()
    if 'happy' in key_blocks:
        key_blocks['happy'].value = 1.0
    render_image("gate_b_expr_happy.png")
    
    # 7. Vowel AA Mouth Test
    reset_shape_keys()
    if 'aa' in key_blocks:
        key_blocks['aa'].value = 1.0
    render_image("gate_b_expr_aa.png")
    
    # 8. Surprised Test
    reset_shape_keys()
    if 'surprised' in key_blocks:
        key_blocks['surprised'].value = 1.0
    render_image("gate_b_expr_surprised.png")
    
    # Reset to neutral
    reset_shape_keys()

print("ALL PREVIEWS RENDERED SUCCESSFULLY.")
