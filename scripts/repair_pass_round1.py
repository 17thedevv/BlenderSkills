"""Repair Pass Round 1 for Kagari (篝) Gate B Prototype.

Fixes Top 3 Defects:
1. Removes stray pink box and cleans up scene hierarchy.
2. Reshapes hair bangs into parted curtain bangs, adds side cheek locks, and low side-ponytail with crimson ribbon bow.
3. Hides/removes backpack and updates upper outfit to Kagari's crossover miko collar (burgundy & cream with gold trim).
"""
import bpy
import bmesh
import math
from mathutils import Vector, Matrix, Euler
from pathlib import Path

WIP_BLEND = Path("outputs/wip/kagari_gate_b_wip.blend")
OUTPUT_BLEND = Path("outputs/wip/kagari_gate_b_round1.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/gate_b")

bpy.ops.wm.open_mainfile(filepath=str(WIP_BLEND))

# 1. Clean up unwanted objects
for obj_name in ['Kagari_Ribbon_Bow', 'Kagari_Astral_Star', 'Cube', 'robo_arm']:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

# Remove backpack objects if present
for obj in list(bpy.data.objects):
    if 'backpack' in obj.name.lower():
        bpy.data.objects.remove(obj, do_unlink=True)

# 2. Reshape bangs on existing hair mesh to create parted curtain bangs
hair = bpy.data.objects.get('hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    for v in bm.verts:
        # Front bangs: Y < -0.05, Z around 1.34..1.48
        if v.co.y < -0.04 and 1.33 < v.co.z < 1.48:
            # If near center (abs(X) < 0.035), part outward to left or right
            if abs(v.co.x) < 0.035:
                # Part to sides
                sign = 1.0 if v.co.x >= 0 else -1.0
                v.co.x += sign * 0.025 * (1.0 - abs(v.co.x)/0.035)
                # Slightly raise center forehead tips to expose brows
                if v.co.z < 1.40:
                    v.co.z += 0.015
            # Lengthen side bangs (abs(X) between 0.04 and 0.08)
            elif 0.035 <= abs(v.co.x) <= 0.085:
                v.co.z -= 0.020 # Elegant framing side fringe
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()

# 3. Build Kagari's low side-ponytail and long cheek locks
hair_mat = bpy.data.materials.get('hair')

def create_hair_lock(name, pts, radii):
    bm = bmesh.new()
    num = len(pts)
    vl = []
    vr = []
    for i in range(num):
        p = pts[i]
        r = radii[i]
        tang = (pts[min(i+1, num-1)] - pts[max(i-1, 0)]).normalized()
        norm = Vector((-tang.y, tang.x, 0)).normalized()
        if norm.length == 0:
            norm = Vector((1, 0, 0))
        vl.append(bm.verts.new(p - norm * r))
        vr.append(bm.verts.new(p + norm * r))
    for i in range(num - 1):
        bm.faces.new([vl[i], vr[i], vr[i+1], vl[i+1]])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    if hair_mat:
        obj.data.materials.append(hair_mat)
    # Parent to armature head bone if armature exists
    arm = bpy.data.objects.get('Armature')
    if arm:
        obj.parent = arm
        obj.parent_type = 'BONE'
        obj.parent_bone = 'head 1' if 'head 1' in arm.data.bones else 'head'
    return obj

# Left cheek framing lock
create_hair_lock('Kagari_Lock_Left', [
    Vector((0.065, -0.040, 1.400)),
    Vector((0.080, -0.060, 1.330)),
    Vector((0.082, -0.065, 1.250)),
    Vector((0.075, -0.050, 1.180)),
], [0.012, 0.016, 0.012, 0.002])

# Right cheek framing lock
create_hair_lock('Kagari_Lock_Right', [
    Vector((-0.065, -0.040, 1.400)),
    Vector((-0.080, -0.060, 1.330)),
    Vector((-0.082, -0.065, 1.250)),
    Vector((-0.075, -0.050, 1.180)),
], [0.012, 0.016, 0.012, 0.002])

# Low Side-Ponytail draped over right shoulder
create_hair_lock('Kagari_SidePonytail_Main', [
    Vector((-0.075, 0.005, 1.330)),
    Vector((-0.098, -0.015, 1.260)),
    Vector((-0.108, -0.040, 1.180)),
    Vector((-0.098, -0.065, 1.100)),
    Vector((-0.085, -0.075, 1.030)),
    Vector((-0.070, -0.080, 0.960)),
], [0.022, 0.030, 0.028, 0.022, 0.015, 0.003])

# 4. Crimson Silk Ribbon Bow & Tails on Side Ponytail
rib_mat = bpy.data.materials.new(name="M_Kagari_Ribbon_Red")
rib_mat.use_nodes = True
bsdf = rib_mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.55, 0.10, 0.22, 1.0) # Deep Carmine Burgundy
    bsdf.inputs['Roughness'].default_value = 0.35

bm_rib = bmesh.new()
rc = Vector((-0.088, -0.010, 1.300))
# Knot
bmesh.ops.create_cube(bm_rib, size=0.018, matrix=Matrix.Translation(rc))
# Bow loops
bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.020, radius2=0.006, depth=0.042,
                      matrix=Matrix.Translation(rc + Vector((0.012, 0.025, 0.018))) @ Matrix.Rotation(math.radians(50), 4, 'X'))
bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.020, radius2=0.006, depth=0.042,
                      matrix=Matrix.Translation(rc + Vector((-0.012, -0.025, 0.018))) @ Matrix.Rotation(math.radians(-50), 4, 'X'))
me_rib = bpy.data.meshes.new('Kagari_Ribbon_Bow')
bm_rib.to_mesh(me_rib)
bm_rib.free()
obj_rib = bpy.data.objects.new('Kagari_Ribbon_Bow', me_rib)
bpy.context.scene.collection.objects.link(obj_rib)
obj_rib.data.materials.append(rib_mat)
arm = bpy.data.objects.get('Armature')
if arm:
    obj_rib.parent = arm
    obj_rib.parent_type = 'BONE'
    obj_rib.parent_bone = 'head 1' if 'head 1' in arm.data.bones else 'head'

# Ribbon trailing tails
create_hair_lock('Kagari_Ribbon_Tail', [
    rc,
    rc + Vector((-0.015, -0.020, -0.060)),
    rc + Vector((-0.022, -0.035, -0.130)),
    rc + Vector((-0.018, -0.040, -0.200)),
], [0.012, 0.014, 0.010, 0.002])
obj_tail = bpy.data.objects.get('Kagari_Ribbon_Tail')
if obj_tail:
    obj_tail.data.materials.clear()
    obj_tail.data.materials.append(rib_mat)

# 5. Crossover Miko Collar (Cream white, Burgundy lapel, Gold trim)
gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
bsdf_g = gold_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_g:
    bsdf_g.inputs['Base Color'].default_value = (0.95, 0.75, 0.10, 1.0)
    bsdf_g.inputs['Roughness'].default_value = 0.25

bm_collar = bmesh.new()
# Left and right overlapping lapel plates
lapel_l = [
    Vector((0.042, 0.010, 1.17)),
    Vector((0.048, -0.050, 1.13)),
    Vector((0.022, -0.075, 1.06)),
    Vector((-0.015, -0.088, 0.98)),
]
lapel_r = [
    Vector((-0.042, 0.010, 1.17)),
    Vector((-0.048, -0.050, 1.13)),
    Vector((-0.022, -0.077, 1.06)),
    Vector((0.015, -0.090, 0.98)),
]
lw = 0.030
for pts in [lapel_l, lapel_r]:
    for i in range(len(pts) - 1):
        p1 = pts[i]
        p2 = pts[i+1]
        v1 = bm_collar.verts.new(p1)
        v2 = bm_collar.verts.new(p2)
        v3 = bm_collar.verts.new(p2 + Vector((lw, 0, 0)))
        v4 = bm_collar.verts.new(p1 + Vector((lw, 0, 0)))
        bm_collar.faces.new([v1, v2, v3, v4])
me_collar = bpy.data.meshes.new('Kagari_Miko_Collar')
bm_collar.to_mesh(me_collar)
bm_collar.free()
obj_collar = bpy.data.objects.new('Kagari_Miko_Collar', me_collar)
bpy.context.scene.collection.objects.link(obj_collar)
obj_collar.data.materials.append(rib_mat)

# Gold trim along lapel edges
bm_gt = bmesh.new()
gw = 0.005
for pts in [lapel_l, lapel_r]:
    for i in range(len(pts) - 1):
        p1 = pts[i] + Vector((0, -0.002, 0))
        p2 = pts[i+1] + Vector((0, -0.002, 0))
        v1 = bm_gt.verts.new(p1)
        v2 = bm_gt.verts.new(p2)
        v3 = bm_gt.verts.new(p2 + Vector((gw, 0, 0)))
        v4 = bm_gt.verts.new(p1 + Vector((gw, 0, 0)))
        bm_gt.faces.new([v1, v2, v3, v4])
me_gt = bpy.data.meshes.new('Kagari_Gold_Collar_Trim')
bm_gt.to_mesh(me_gt)
bm_gt.free()
obj_gt = bpy.data.objects.new('Kagari_Gold_Collar_Trim', me_gt)
bpy.context.scene.collection.objects.link(obj_gt)
obj_gt.data.materials.append(gold_mat)

# Astral Star Pendant
bm_star = bmesh.new()
sc = Vector((0.0, -0.075, 1.130))
star_c = bm_star.verts.new(sc)
sv = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.016 if i % 2 == 0 else 0.007
    sv.append(bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y - 0.002, sc.z + r * math.cos(ang)))))
for i in range(16):
    bm_star.faces.new([star_c, sv[i], sv[(i + 1) % 16]])
me_star = bpy.data.meshes.new('Kagari_Astral_Star')
bm_star.to_mesh(me_star)
bm_star.free()
obj_star = bpy.data.objects.new('Kagari_Astral_Star', me_star)
bpy.context.scene.collection.objects.link(obj_star)
obj_star.data.materials.append(gold_mat)

# 6. Re-Render All 8 Review Images
scene = bpy.context.scene
cam = scene.camera

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

# Expressions
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
