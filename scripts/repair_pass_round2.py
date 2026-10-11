"""Repair Pass Round 2: Refine Kagari's Hair, Parted Fringe, Miko Collar, and Remove Suspenders."""
import bpy
import bmesh
import math
from mathutils import Vector, Matrix, Euler
from pathlib import Path

INPUT_BLEND = Path("outputs/wip/kagari_gate_b_wip.blend")
OUTPUT_BLEND = Path("outputs/wip/kagari_gate_b_round2.blend")
PREVIEWS_DIR = Path("D:/Project-17/blender/outputs/previews/gate_b")

bpy.ops.wm.open_mainfile(filepath=str(INPUT_BLEND))

# 1. Hide the bulky suspenders/wear object from render
wear = bpy.data.objects.get('wear')
if wear:
    wear.hide_render = True
    wear.hide_viewport = True

# Also hide any leftover objects
for name in ['Cube', 'robo_arm', 'hair_tail']:
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

# 2. Get materials
hair_mat = bpy.data.materials.get('hair')
skin_mat = bpy.data.materials.get('body_bake')

# Create clean Miko Collar & Kimono materials
miko_burgundy = bpy.data.materials.new(name="M_Kagari_Miko_Burgundy")
miko_burgundy.use_nodes = True
b_bsdf = miko_burgundy.node_tree.nodes.get("Principled BSDF")
if b_bsdf:
    b_bsdf.inputs['Base Color'].default_value = (0.50, 0.08, 0.20, 1.0)
    b_bsdf.inputs['Roughness'].default_value = 0.4

kimono_cream = bpy.data.materials.new(name="M_Kagari_Kimono_Cream")
kimono_cream.use_nodes = True
k_bsdf = kimono_cream.node_tree.nodes.get("Principled BSDF")
if k_bsdf:
    k_bsdf.inputs['Base Color'].default_value = (0.98, 0.96, 0.92, 1.0)
    k_bsdf.inputs['Roughness'].default_value = 0.5

gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
g_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.95, 0.75, 0.10, 1.0)
    g_bsdf.inputs['Roughness'].default_value = 0.25

ribbon_mat = bpy.data.materials.new(name="M_Kagari_Ribbon_Carmine")
ribbon_mat.use_nodes = True
r_bsdf = ribbon_mat.node_tree.nodes.get("Principled BSDF")
if r_bsdf:
    r_bsdf.inputs['Base Color'].default_value = (0.65, 0.10, 0.22, 1.0)
    r_bsdf.inputs['Roughness'].default_value = 0.35

# 3. Clean up the choppy bangs on original hair mesh
hair = bpy.data.objects.get('hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    # Remove center front bangs faces that block the forehead
    verts_to_remove = []
    for v in bm.verts:
        # Front center bangs: Y < -0.05, abs(X) < 0.045, Z between 1.34 and 1.48
        if v.co.y < -0.045 and abs(v.co.x) < 0.042 and 1.34 < v.co.z < 1.46:
            verts_to_remove.append(v)
    bmesh.ops.delete(bm, geom=verts_to_remove, context='VERTS')
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()

# 4. Build Kagari's elegant parted curtain bangs (Framing forehead cleanly)
def build_curved_hair_strand(name, pts, widths, mat=hair_mat):
    bm = bmesh.new()
    num = len(pts)
    vl = []
    vr = []
    for i in range(num):
        p = pts[i]
        w = widths[i]
        tang = (pts[min(i+1, num-1)] - pts[max(i-1, 0)]).normalized()
        norm = Vector((-tang.y, tang.x, 0)).normalized()
        if norm.length == 0:
            norm = Vector((1, 0, 0))
        vl.append(bm.verts.new(p - norm * w))
        vr.append(bm.verts.new(p + norm * w))
    for i in range(num - 1):
        bm.faces.new([vl[i], vr[i], vr[i+1], vl[i+1]])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    # Smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj

# Left parted bangs (flowing outward to left temple)
build_curved_hair_strand('Kagari_Bangs_Left_1', [
    Vector((0.008, -0.088, 1.455)),
    Vector((0.025, -0.098, 1.425)),
    Vector((0.045, -0.100, 1.385)),
    Vector((0.055, -0.092, 1.335)),
    Vector((0.058, -0.080, 1.285)),
], [0.010, 0.016, 0.014, 0.009, 0.002])

build_curved_hair_strand('Kagari_Bangs_Left_2', [
    Vector((0.005, -0.090, 1.450)),
    Vector((0.016, -0.099, 1.420)),
    Vector((0.030, -0.101, 1.375)),
    Vector((0.038, -0.095, 1.330)),
], [0.007, 0.011, 0.008, 0.002])

# Right parted bangs (flowing outward to right temple)
build_curved_hair_strand('Kagari_Bangs_Right_1', [
    Vector((-0.008, -0.088, 1.455)),
    Vector((-0.025, -0.098, 1.425)),
    Vector((-0.045, -0.100, 1.385)),
    Vector((-0.055, -0.092, 1.335)),
    Vector((-0.058, -0.080, 1.285)),
], [0.010, 0.016, 0.014, 0.009, 0.002])

build_curved_hair_strand('Kagari_Bangs_Right_2', [
    Vector((-0.005, -0.090, 1.450)),
    Vector((-0.016, -0.099, 1.420)),
    Vector((-0.030, -0.101, 1.375)),
    Vector((-0.038, -0.095, 1.330)),
], [0.007, 0.011, 0.008, 0.002])

# Side cheek framing locks
build_curved_hair_strand('Kagari_SideLock_L', [
    Vector((0.065, -0.060, 1.410)),
    Vector((0.078, -0.075, 1.340)),
    Vector((0.082, -0.070, 1.260)),
    Vector((0.076, -0.055, 1.180)),
    Vector((0.068, -0.040, 1.120)),
], [0.014, 0.018, 0.015, 0.009, 0.002])

build_curved_hair_strand('Kagari_SideLock_R', [
    Vector((-0.065, -0.060, 1.410)),
    Vector((-0.078, -0.075, 1.340)),
    Vector((-0.082, -0.070, 1.260)),
    Vector((-0.076, -0.055, 1.180)),
    Vector((-0.068, -0.040, 1.120)),
], [0.014, 0.018, 0.015, 0.009, 0.002])

# 5. Low Side-Ponytail on Right Side (Draped over right collarbone)
build_curved_hair_strand('Kagari_SidePonytail', [
    Vector((-0.082, -0.010, 1.340)),
    Vector((-0.102, -0.035, 1.270)),
    Vector((-0.112, -0.060, 1.200)),
    Vector((-0.105, -0.080, 1.120)),
    Vector((-0.090, -0.090, 1.050)),
    Vector((-0.075, -0.095, 0.980)),
], [0.024, 0.032, 0.030, 0.024, 0.016, 0.003])

# Crimson Silk Ribbon Bow at base of side-ponytail
bm_bow = bmesh.new()
bc = Vector((-0.086, -0.025, 1.315))
# Center knot
bmesh.ops.create_cube(bm_bow, size=0.018, matrix=Matrix.Translation(bc))
# Bow loops
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.022, radius2=0.008, depth=0.045,
                      matrix=Matrix.Translation(bc + Vector((0.015, 0.020, 0.018))) @ Matrix.Rotation(math.radians(55), 4, 'X'))
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.022, radius2=0.008, depth=0.045,
                      matrix=Matrix.Translation(bc + Vector((-0.015, -0.020, 0.018))) @ Matrix.Rotation(math.radians(-55), 4, 'X'))
me_bow = bpy.data.meshes.new('Kagari_Ribbon_Bow')
bm_bow.to_mesh(me_bow)
bm_bow.free()
obj_bow = bpy.data.objects.new('Kagari_Ribbon_Bow', me_bow)
bpy.context.scene.collection.objects.link(obj_bow)
obj_bow.data.materials.append(ribbon_mat)
for poly in obj_bow.data.polygons:
    poly.use_smooth = True

# Ribbon flowing tails
build_curved_hair_strand('Kagari_Ribbon_Tails', [
    bc,
    bc + Vector((-0.018, -0.025, -0.060)),
    bc + Vector((-0.024, -0.040, -0.130)),
    bc + Vector((-0.018, -0.045, -0.200)),
], [0.012, 0.015, 0.010, 0.002], mat=ribbon_mat)

# 6. Upper Torso Kimono & Miko Crossover Collar
bm_torso = bmesh.new()
# Torso cylinder for clean cream kimono
segs = 16
for iz, z in enumerate([1.22, 1.14, 1.04, 0.94]):
    rx = 0.09 + iz * 0.035
    ry = 0.07 + iz * 0.025
    for i in range(segs):
        ang = (i / segs) * 2.0 * math.pi
        vx = rx * math.sin(ang)
        vy = ry * math.cos(ang) - 0.01
        bm_torso.verts.new(Vector((vx, vy, z)))
bm_torso.verts.ensure_lookup_table()
for iz in range(3):
    for i in range(segs):
        i0 = iz * segs + i
        i1 = iz * segs + (i + 1) % segs
        i2 = (iz + 1) * segs + (i + 1) % segs
        i3 = (iz + 1) * segs + i
        bm_torso.faces.new([bm_torso.verts[i0], bm_torso.verts[i1], bm_torso.verts[i2], bm_torso.verts[i3]])
me_torso = bpy.data.meshes.new('Kagari_Kimono_Body')
bm_torso.to_mesh(me_torso)
bm_torso.free()
obj_torso = bpy.data.objects.new('Kagari_Kimono_Body', me_torso)
bpy.context.scene.collection.objects.link(obj_torso)
obj_torso.data.materials.append(kimono_cream)
for poly in obj_torso.data.polygons:
    poly.use_smooth = True

# Crossover Burgundy Haori Collar
bm_collar = bmesh.new()
lapel_left = [
    Vector((0.045, -0.020, 1.18)),
    Vector((0.052, -0.070, 1.14)),
    Vector((0.028, -0.095, 1.07)),
    Vector((-0.015, -0.105, 1.00)),
]
lapel_right = [
    Vector((-0.045, -0.020, 1.18)),
    Vector((-0.052, -0.070, 1.14)),
    Vector((-0.028, -0.097, 1.07)),
    Vector((0.015, -0.107, 1.00)),
]
lw = 0.032
for pts in [lapel_left, lapel_right]:
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
obj_collar.data.materials.append(miko_burgundy)
for poly in obj_collar.data.polygons:
    poly.use_smooth = True

# Gold trim along lapels
bm_gt = bmesh.new()
gw = 0.005
for pts in [lapel_left, lapel_right]:
    for i in range(len(pts) - 1):
        p1 = pts[i] + Vector((0, -0.003, 0))
        p2 = pts[i+1] + Vector((0, -0.003, 0))
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
for poly in obj_gt.data.polygons:
    poly.use_smooth = True

# Astral 8-point Star Pendant
bm_star = bmesh.new()
sc = Vector((0.0, -0.088, 1.135))
star_c = bm_star.verts.new(sc)
sv = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.016 if i % 2 == 0 else 0.007
    sv.append(bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y - 0.003, sc.z + r * math.cos(ang)))))
for i in range(16):
    bm_star.faces.new([star_c, sv[i], sv[(i + 1) % 16]])
me_star = bpy.data.meshes.new('Kagari_Astral_Star')
bm_star.to_mesh(me_star)
bm_star.free()
obj_star = bpy.data.objects.new('Kagari_Astral_Star', me_star)
bpy.context.scene.collection.objects.link(obj_star)
obj_star.data.materials.append(gold_mat)

# 7. Render Review Views
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
