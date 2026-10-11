"""Kagari (篝) — Artistic Fidelity Master Script v3.

Perfects:
1. Posed armature: relaxed natural standing arms.
2. 3D Silk Bow: positioned at ponytail root behind ear (X=-0.095, Y=0.015, Z=1.335), two curved horizontal loops, flowing ribbon tails, rich carmine velvet texture (kagari_bow.png) with gold flower brooch.
3. Side Ponytail: drapes forward over right clavicle and onto chest.
4. Clean anime bob on left side.
5. Faceted 3D 8-point Astral Star necklace at neck hollow.
6. Multi-angle renders & side-by-side concept art comparison.
"""
import bpy
import bmesh
import math
import os
from pathlib import Path
from mathutils import Vector, Matrix, Euler

ROOT = Path("D:/Project-17/blender")
SRC_BLEND = ROOT / "outputs/sources/AvatarSample_B.blend"
OUT_TEX = ROOT / "outputs/textures_kagari_vroid"
OUT_BLEND = ROOT / "outputs/wip/kagari_vroid_master.blend"
PREVIEWS_DIR = ROOT / "outputs/previews/recovery"
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading base blend:", SRC_BLEND)
bpy.ops.wm.open_mainfile(filepath=str(SRC_BLEND))

cube = bpy.data.objects.get('Cube')
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)

arm = bpy.data.objects.get('Armature')

# 1. Pose Armature: Relax arms down naturally
if arm:
    bpy.context.view_layer.objects.active = arm
    b_l = arm.pose.bones.get('J_Bip_L_UpperArm')
    b_r = arm.pose.bones.get('J_Bip_R_UpperArm')
    if b_l and b_r:
        b_l.rotation_mode = 'XYZ'
        b_r.rotation_mode = 'XYZ'
        b_l.rotation_euler = (0, 0, math.radians(-68))
        b_r.rotation_euler = (0, 0, math.radians(68))
        
        la_l = arm.pose.bones.get('J_Bip_L_LowerArm')
        la_r = arm.pose.bones.get('J_Bip_R_LowerArm')
        if la_l and la_r:
            la_l.rotation_mode = 'XYZ'
            la_r.rotation_mode = 'XYZ'
            la_l.rotation_euler = (0, math.radians(12), math.radians(-10))
            la_r.rotation_euler = (0, math.radians(-12), math.radians(10))
    bpy.context.view_layer.update()
    print("Armature posed in relaxed standing portrait pose.")

# 2. Refine Hair Mesh
hair = bpy.data.objects.get('Hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    
    # 2.1 Delete punk accessory faces (slots 2, 3, 4, 5)
    acc_faces = [f for f in bm.faces if f.material_index in [2, 3, 4, 5]]
    print(f"Removing {len(acc_faces)} punk accessory faces from Hair")
    bmesh.ops.delete(bm, geom=acc_faces, context='FACES_ONLY')
    
    # 2.2 Delete left high twintail (character left / viewer right: X > 0.05, material 1, Y < 0.16)
    left_twintail = [f for f in bm.faces if f.material_index == 1 and all(v.co.x > 0.05 and v.co.y < 0.16 for v in f.verts)]
    print(f"Removing {len(left_twintail)} left twintail faces")
    bmesh.ops.delete(bm, geom=left_twintail, context='FACES_ONLY')
    
    # 2.3 Clean ALL flared / protruding hair on character left (viewer right)
    flared_left = [f for f in bm.faces if all(v.co.x > 0.040 and v.co.z < 1.40 and v.co.y > -0.065 for v in f.verts)]
    print(f"Removing {len(flared_left)} flared left strand faces")
    bmesh.ops.delete(bm, geom=flared_left, context='FACES_ONLY')
    
    crumbs = [f for f in bm.faces if any(v.co.x > 0.038 and v.co.z < 1.36 and v.co.y > -0.06 for v in f.verts)]
    print(f"Removing {len(crumbs)} left crumb faces")
    bmesh.ops.delete(bm, geom=crumbs, context='FACES_ONLY')
    
    # 2.4 Drape Right Side-Ponytail FORWARD over right shoulder and onto chest
    right_ponytail_verts = [v for v in bm.verts if v.co.x < -0.05 and v.co.z < 1.40]
    for v in right_ponytail_verts:
        dist = max(0.0, min(1.0, (1.35 - v.co.z) / 0.45))
        # Curve forward in Y significantly so it rests in front of shoulder and clavicle
        v.co.y -= 0.22 * dist
        # Curve inward toward chest center
        v.co.x += 0.055 * dist
        # Gravity downward drape
        v.co.z -= 0.030 * dist
        
    # 2.5 Reshape Bangs: Part center curtain bangs to reveal forehead
    bang_verts = [v for v in bm.verts if v.co.y < -0.06 and 1.30 < v.co.z < 1.48]
    for v in bang_verts:
        factor = max(0.0, min(1.0, (1.46 - v.co.z) / 0.16))
        if -0.024 < v.co.x <= 0.00:
            v.co.x -= 0.024 * factor
            v.co.z += 0.012 * factor
        elif 0.00 < v.co.x < 0.024:
            v.co.x += 0.024 * factor
            v.co.z += 0.012 * factor
            
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()
    print("Hair geometry refined successfully!")

# 3. Model Kagari's Large Carmine Burgundy Silk Hair Bow
print("Modeling 3D Large Burgundy Silk Bow at ponytail root...")
bow_tex_path = OUT_TEX / "kagari_bow.png"
bow_img = bpy.data.images.load(str(bow_tex_path), check_existing=True)

ribbon_mat = bpy.data.materials.new(name="M_Kagari_Silk_Bow")
ribbon_mat.use_nodes = True
bsdf = ribbon_mat.node_tree.nodes.get("Principled BSDF")
tex_node = ribbon_mat.node_tree.nodes.new("ShaderNodeTexImage")
tex_node.image = bow_img
ribbon_mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.40

gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
g_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.96, 0.76, 0.12, 1.0) # Astral Gold #E6B800
    g_bsdf.inputs['Roughness'].default_value = 0.18
    g_bsdf.inputs['Metallic'].default_value = 0.90

bm_bow = bmesh.new()
# Position at ponytail root behind right ear: X = -0.095, Y = 0.015, Z = 1.335
rc = Vector((-0.095, 0.015, 1.335))

# Center knot (cylinder/cube)
bmesh.ops.create_cube(bm_bow, size=0.024, matrix=Matrix.Translation(rc))

def make_ribbon_loop(bm, center_pt, span_vec, width=0.028, steps=8):
    # Creates a curved 3D teardrop loop
    pts = []
    for i in range(steps + 1):
        t = i / float(steps)
        # Loop curve out and back
        ang = t * 2.0 * math.pi
        rad = math.sin(t * math.pi)
        pos = center_pt + span_vec * (1.0 - math.cos(ang / 2.0)) + Vector((0, -0.010 * rad, 0))
        pts.append(pos)
    v_l, v_r = [], []
    for i, p in enumerate(pts):
        w = width * math.sin(i / float(steps) * math.pi)
        v_l.append(bm.verts.new(p + Vector((0, 0, w))))
        v_r.append(bm.verts.new(p + Vector((0, 0, -w))))
    for i in range(len(pts) - 1):
        bm.faces.new([v_l[i], v_r[i], v_r[i+1], v_l[i+1]])

# Left Upper Loop (extending left and up from ponytail root)
make_ribbon_loop(bm_bow, rc, Vector((-0.065, -0.010, 0.040)), width=0.030)

# Right Lower Loop (extending left and down from ponytail root)
make_ribbon_loop(bm_bow, rc, Vector((-0.060, -0.010, -0.035)), width=0.030)

# Flowing silk ribbon tails curving down over shoulder
def make_strip(bm, pts, w_start, w_end):
    vl, vr = [], []
    for i, pt in enumerate(pts):
        t = i / float(len(pts) - 1)
        w = w_start * (1.0 - t) + w_end * t
        vl.append(bm.verts.new(pt + Vector((w, 0, 0))))
        vr.append(bm.verts.new(pt + Vector((-w, 0, 0))))
    for i in range(len(pts) - 1):
        bm.faces.new([vl[i], vr[i], vr[i+1], vl[i+1]])

tail1_pts = [
    rc + Vector((0.000, -0.015, -0.010)),
    rc + Vector((-0.015, -0.035, -0.080)),
    rc + Vector((-0.025, -0.065, -0.160)),
    rc + Vector((-0.020, -0.080, -0.240)),
]
make_strip(bm_bow, tail1_pts, 0.014, 0.003)

tail2_pts = [
    rc + Vector((-0.015, -0.010, -0.010)),
    rc + Vector((-0.032, -0.030, -0.075)),
    rc + Vector((-0.045, -0.055, -0.150)),
    rc + Vector((-0.040, -0.070, -0.220)),
]
make_strip(bm_bow, tail2_pts, 0.012, 0.003)

# Center gold flower brooch on bow knot
b_flower_c = bm_bow.verts.new(rc + Vector((-0.005, -0.016, 0.0)))
b_flower_verts = []
for i in range(8):
    ang = (i / 8.0) * 2.0 * math.pi
    r = 0.012 if i % 2 == 0 else 0.005
    b_flower_verts.append(bm_bow.verts.new(Vector((rc.x - 0.005 + r * math.sin(ang), rc.y - 0.016, rc.z + r * math.cos(ang)))))
for i in range(8):
    f_pin = bm_bow.faces.new([b_flower_c, b_flower_verts[i], b_flower_verts[(i + 1) % 8]])
    f_pin.material_index = 1

me_bow = bpy.data.meshes.new("Kagari_Large_Burgundy_Bow")
bm_bow.to_mesh(me_bow)
bm_bow.free()
obj_bow = bpy.data.objects.new("Kagari_Large_Burgundy_Bow", me_bow)
bpy.context.scene.collection.objects.link(obj_bow)
obj_bow.data.materials.append(ribbon_mat)
obj_bow.data.materials.append(gold_mat)
for poly in obj_bow.data.polygons:
    poly.use_smooth = True

if arm:
    obj_bow.parent = arm
    obj_bow.parent_type = 'OBJECT'
    vg_head = obj_bow.vertex_groups.new(name='J_Bip_C_Head')
    vg_head.add(list(range(len(obj_bow.data.vertices))), 1.0, 'REPLACE')
    mod_arm = obj_bow.modifiers.new(name='Armature', type='ARMATURE')
    mod_arm.object = arm

# 4. Model 8-Point Faceted Astral Star Pendant & Gold Chain
print("Modeling Astral Star Pendant & Gold Chain...")
bm_star = bmesh.new()
sc = Vector((0.0, -0.082, 1.185))
front_tip = bm_star.verts.new(sc + Vector((0.0, -0.005, 0.0)))
back_tip = bm_star.verts.new(sc + Vector((0.0, 0.003, 0.0)))

ring_verts = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.026 if i % 2 == 0 else 0.012
    v = bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y, sc.z + r * math.cos(ang))))
    ring_verts.append(v)

for i in range(16):
    v_next = ring_verts[(i + 1) % 16]
    bm_star.faces.new([front_tip, ring_verts[i], v_next])
    bm_star.faces.new([back_tip, v_next, ring_verts[i]])

chain_pts = []
for i in range(25):
    ang = -math.pi * 0.40 + (i / 24.0) * math.pi * 0.80
    cx = 0.065 * math.sin(ang)
    cy = -0.040 - 0.042 * math.cos(ang)
    cz = 1.185 + 0.045 * (1.0 - math.cos(ang))
    chain_pts.append(bm_star.verts.new(Vector((cx, cy, cz))))
for i in range(len(chain_pts) - 1):
    bm_star.edges.new([chain_pts[i], chain_pts[i+1]])

me_star = bpy.data.meshes.new("Kagari_Astral_Star_Pendant")
bm_star.to_mesh(me_star)
bm_star.free()
obj_star = bpy.data.objects.new("Kagari_Astral_Star_Pendant", me_star)
bpy.context.scene.collection.objects.link(obj_star)
obj_star.data.materials.append(gold_mat)
for poly in obj_star.data.polygons:
    poly.use_smooth = True

if arm:
    obj_star.parent = arm
    obj_star.parent_type = 'OBJECT'
    vg_chest = obj_star.vertex_groups.new(name='J_Bip_C_UpperChest')
    vg_chest.add(list(range(len(obj_star.data.vertices))), 1.0, 'REPLACE')
    mod_arm_s = obj_star.modifiers.new(name='Armature', type='ARMATURE')
    mod_arm_s.object = arm

# 5. Clean Body Mesh Protruding Hoodie Collar
body = bpy.data.objects.get('Body')
if body and body.data:
    bm_b = bmesh.new()
    bm_b.from_mesh(body.data)
    jacket_neck = [f for f in bm_b.faces if f.material_index == 2 and any(v.co.z > 1.15 for v in f.verts)]
    print(f"Removing {len(jacket_neck)} protruding hoodie collar faces")
    bmesh.ops.delete(bm_b, geom=jacket_neck, context='FACES_ONLY')
    bm_b.to_mesh(body.data)
    bm_b.free()
    body.data.update()

# 6. Non-Destructive Material Binding
print("Binding MToon textures...")
def bind_mtoon_texture(mat_name, image_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.node_tree:
        print(f"Warning: Material {mat_name} not found")
        return
    img = bpy.data.images.load(str(image_path), check_existing=True)
    bound = 0
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            if 'BaseColor' in node.name or 'ShadeMultiply' in node.name:
                node.image = img
                bound += 1
    print(f"Bound {mat_name}: {bound} nodes -> {image_path.name}")

# Face textures
bind_mtoon_texture("N00_000_00_Face_00_SKIN (Instance)", OUT_TEX / "kagari_face_skin.png")
bind_mtoon_texture("MToon Outline (N00_000_00_Face_00_SKIN (Instance))", OUT_TEX / "kagari_face_skin.png")
bind_mtoon_texture("N00_000_00_EyeIris_00_EYE (Instance)", OUT_TEX / "kagari_iris.png")
bind_mtoon_texture("N00_000_00_FaceBrow_00_FACE (Instance)", OUT_TEX / "kagari_brows.png")
bind_mtoon_texture("N00_000_00_FaceEyeline_00_FACE (Instance)", OUT_TEX / "kagari_eyeline.png")

# Body skin & Kimono tops
bind_mtoon_texture("N00_000_00_Body_00_SKIN (Instance)", OUT_TEX / "kagari_body_skin.png")
bind_mtoon_texture("MToon Outline (N00_000_00_Body_00_SKIN (Instance))", OUT_TEX / "kagari_body_skin.png")
bind_mtoon_texture("N00_007_01_Tops_01_CLOTH (Instance)", OUT_TEX / "kagari_kimono_tops.png")
bind_mtoon_texture("MToon Outline (N00_007_01_Tops_01_CLOTH (Instance))", OUT_TEX / "kagari_kimono_tops.png")

# Hair textures
bind_mtoon_texture("N00_000_Hair_00_HAIR_01 (Instance)", OUT_TEX / "kagari_hair_01.png")
bind_mtoon_texture("MToon Outline (N00_000_Hair_00_HAIR_01 (Instance))", OUT_TEX / "kagari_hair_01.png")
bind_mtoon_texture("N00_000_Hair_00_HAIR_02 (Instance)", OUT_TEX / "kagari_hair_02.png")
bind_mtoon_texture("MToon Outline (N00_000_Hair_00_HAIR_02 (Instance))", OUT_TEX / "kagari_hair_02.png")

# 7. Studio Lighting & Cameras
print("Configuring studio lighting and cameras...")
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024

for l in list(bpy.data.lights):
    bpy.data.lights.remove(l)

if not scene.world:
    scene.world = bpy.data.worlds.new("Kagari_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.98, 0.97, 0.96, 1.0)
    bg.inputs['Strength'].default_value = 1.0

key_d = bpy.data.lights.new("Studio_Key", type='AREA')
key_d.energy = 52.0
key_d.size = 1.6
key_d.color = (1.0, 0.98, 0.95)
key_d.use_shadow = False
key_o = bpy.data.objects.new("Studio_Key", key_d)
key_o.location = (0.0, -1.2, 1.35)
scene.collection.objects.link(key_o)

rim_d = bpy.data.lights.new("Studio_Rim", type='AREA')
rim_d.energy = 30.0
rim_d.size = 1.2
rim_d.color = (1.0, 0.95, 0.88)
rim_d.use_shadow = False
rim_o = bpy.data.objects.new("Studio_Rim", rim_d)
rim_o.location = (0.5, 0.8, 1.5)
scene.collection.objects.link(rim_o)

cam = scene.camera
if not cam:
    cam_d = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Cam", cam_d)
    scene.collection.objects.link(cam)
    scene.camera = cam

def set_camera(pos, target=Vector((0.0, 0.0, 1.25))):
    cam.location = pos
    d = target - pos
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def render_view(filename):
    out = PREVIEWS_DIR / filename
    scene.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED: {out}")
    return out

print("Rendering multi-angle previews...")
# Front Bust Portrait
cam.data.lens = 65.0
set_camera(Vector((0.0, -1.05, 1.25)), Vector((0.0, 0.0, 1.25)))
render_view("kagari_rebuilt_front.png")

# Three-Quarter View
set_camera(Vector((-0.55, -0.90, 1.25)), Vector((0.0, 0.0, 1.25)))
render_view("kagari_rebuilt_three_quarter.png")

# Side Profile
set_camera(Vector((-1.05, 0.0, 1.25)), Vector((0.0, 0.0, 1.25)))
render_view("kagari_rebuilt_side.png")

# Close-up Face
cam.data.lens = 85.0
set_camera(Vector((0.0, -0.52, 1.32)), Vector((0.0, 0.0, 1.32)))
render_view("kagari_rebuilt_face.png")

OUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
print(f"SUCCESS: Saved master blend at {OUT_BLEND}")
