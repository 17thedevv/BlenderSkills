"""Kagari Blender Master Script v2.
Precision fidelity tuning:
- Fix Bow geometry & front placement (in front of right ear/ponytail, deep carmine burgundy).
- Fix Astral Star Pendant (faceted 3D 8-point star at neck hollow Z=1.185).
- Clean left flared twintail chunk completely so hair curves into soft bob.
- Ensure side ponytail drapes forward over right collarbone.
- Render all portrait views and assemble side-by-side review comparison.
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

# 1. Refine Hair Mesh
hair = bpy.data.objects.get('Hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    
    # 1.1 Delete punk accessory faces (slots 2, 3, 4, 5)
    acc_faces = [f for f in bm.faces if f.material_index in [2, 3, 4, 5]]
    print(f"Removing {len(acc_faces)} punk accessory faces from Hair")
    bmesh.ops.delete(bm, geom=acc_faces, context='FACES_ONLY')
    
    # 1.2 Delete left high twintail (character left / viewer right: X > 0.05, material 1, Y < 0.16)
    left_twintail = [f for f in bm.faces if f.material_index == 1 and all(v.co.x > 0.05 and v.co.y < 0.16 for v in f.verts)]
    print(f"Removing {len(left_twintail)} left twintail faces")
    bmesh.ops.delete(bm, geom=left_twintail, context='FACES_ONLY')
    
    # 1.3 Clean ALL flared hair on character left (viewer right: X > 0.045, Z < 1.40, Y > -0.065)
    flared_left = [f for f in bm.faces if all(v.co.x > 0.042 and v.co.z < 1.40 and v.co.y > -0.065 for v in f.verts)]
    print(f"Removing {len(flared_left)} flared left strand faces")
    bmesh.ops.delete(bm, geom=flared_left, context='FACES_ONLY')
    
    # Also clean lower tip flared strands on character left (X > 0.05, Z < 1.35)
    flared_tips = [f for f in bm.faces if any(v.co.x > 0.055 and v.co.z < 1.35 for v in f.verts)]
    print(f"Removing {len(flared_tips)} remaining left tip faces")
    bmesh.ops.delete(bm, geom=flared_tips, context='FACES_ONLY')
    
    # 1.4 Reposition right side-ponytail forward over right shoulder
    right_ponytail_verts = [v for v in bm.verts if v.co.x < -0.06 and v.co.z < 1.40]
    for v in right_ponytail_verts:
        z_factor = max(0.0, min(1.0, (1.35 - v.co.z) / 0.50))
        v.co.y -= 0.11 * z_factor   # drape forward
        v.co.x += 0.035 * z_factor  # drape over shoulder toward chest
        v.co.z -= 0.015 * z_factor  # gravity drape
        
    # 1.5 Part the center curtain bangs gently to expose forehead
    bang_verts = [v for v in bm.verts if v.co.y < -0.06 and 1.30 < v.co.z < 1.48]
    for v in bang_verts:
        if -0.020 < v.co.x <= 0.00:
            v.co.x -= 0.018 * (1.46 - v.co.z) / 0.16
        elif 0.00 < v.co.x < 0.020:
            v.co.x += 0.018 * (1.46 - v.co.z) / 0.16
            
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()
    print("Hair geometry refined successfully!")

# 2. Model Kagari's Large Burgundy Silk Hair Bow (Positioned in FRONT on right ear)
print("Modeling Large Burgundy Silk Bow in front of right ponytail...")
ribbon_mat = bpy.data.materials.new(name="M_Kagari_Silk_Bow")
ribbon_mat.use_nodes = True
r_bsdf = ribbon_mat.node_tree.nodes.get("Principled BSDF")
if r_bsdf:
    r_bsdf.inputs['Base Color'].default_value = (0.65, 0.08, 0.18, 1.0) # Radiant Carmine Burgundy #B22234
    r_bsdf.inputs['Roughness'].default_value = 0.32

bm_bow = bmesh.new()
# Position in front of right ear at ponytail base: X = -0.085, Y = -0.055, Z = 1.320
rc = Vector((-0.085, -0.055, 1.320))

# Center knot (beveled cube)
bmesh.ops.create_cube(bm_bow, size=0.026, matrix=Matrix.Translation(rc))

# Left upper wing (loop pointing up-left)
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.035, radius2=0.010, depth=0.075,
                      matrix=Matrix.Translation(rc + Vector((-0.028, -0.010, 0.032))) @ Matrix.Rotation(math.radians(45), 4, 'X') @ Matrix.Rotation(math.radians(35), 4, 'Y'))

# Right lower wing (loop pointing down-left)
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.035, radius2=0.010, depth=0.075,
                      matrix=Matrix.Translation(rc + Vector((-0.026, -0.010, -0.030))) @ Matrix.Rotation(math.radians(-40), 4, 'X') @ Matrix.Rotation(math.radians(-30), 4, 'Y'))

# Flowing silk ribbon tails curving down over shoulder and chest
tail1_pts = [
    rc + Vector((0.005, -0.008, -0.010)),
    rc + Vector((-0.008, -0.018, -0.080)),
    rc + Vector((-0.016, -0.028, -0.160)),
    rc + Vector((-0.012, -0.032, -0.230)),
]
vl1, vr1 = [], []
for i, pt in enumerate(tail1_pts):
    w = 0.018 if i < 2 else (0.012 if i == 2 else 0.004)
    vl1.append(bm_bow.verts.new(pt + Vector((w, 0, 0))))
    vr1.append(bm_bow.verts.new(pt + Vector((-w, 0, 0))))
for i in range(len(tail1_pts) - 1):
    bm_bow.faces.new([vl1[i], vr1[i], vr1[i+1], vl1[i+1]])

tail2_pts = [
    rc + Vector((-0.012, -0.006, -0.010)),
    rc + Vector((-0.028, -0.016, -0.070)),
    rc + Vector((-0.038, -0.022, -0.140)),
    rc + Vector((-0.032, -0.025, -0.210)),
]
vl2, vr2 = [], []
for i, pt in enumerate(tail2_pts):
    w = 0.016 if i < 2 else (0.010 if i == 2 else 0.003)
    vl2.append(bm_bow.verts.new(pt + Vector((w, 0, 0))))
    vr2.append(bm_bow.verts.new(pt + Vector((-w, 0, 0))))
for i in range(len(tail2_pts) - 1):
    bm_bow.faces.new([vl2[i], vr2[i], vr2[i+1], vl2[i+1]])

me_bow = bpy.data.meshes.new("Kagari_Large_Burgundy_Bow")
bm_bow.to_mesh(me_bow)
bm_bow.free()
obj_bow = bpy.data.objects.new("Kagari_Large_Burgundy_Bow", me_bow)
bpy.context.scene.collection.objects.link(obj_bow)
obj_bow.data.materials.append(ribbon_mat)
for poly in obj_bow.data.polygons:
    poly.use_smooth = True

if arm:
    obj_bow.parent = arm
    obj_bow.parent_type = 'OBJECT'
    vg_head = obj_bow.vertex_groups.new(name='J_Bip_C_Head')
    vg_head.add(list(range(len(obj_bow.data.vertices))), 1.0, 'REPLACE')
    mod_arm = obj_bow.modifiers.new(name='Armature', type='ARMATURE')
    mod_arm.object = arm

# 3. Model 8-Point Faceted Astral Star Pendant & Gold Chain
print("Modeling Astral Star Pendant & Gold Chain...")
gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
g_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.96, 0.76, 0.12, 1.0) # Astral Gold #E6B800
    g_bsdf.inputs['Roughness'].default_value = 0.18
    g_bsdf.inputs['Metallic'].default_value = 0.90

bm_star = bmesh.new()
# Neck hollow at X = 0, Y = -0.082, Z = 1.185 (clearly visible in front of collar)
sc = Vector((0.0, -0.082, 1.185))
front_tip = bm_star.verts.new(sc + Vector((0.0, -0.005, 0.0)))
back_tip = bm_star.verts.new(sc + Vector((0.0, 0.003, 0.0)))

ring_verts = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.026 if i % 2 == 0 else 0.012
    v = bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y, sc.z + r * math.cos(ang))))
    ring_verts.append(v)

# Faceted star front and back
for i in range(16):
    v_next = ring_verts[(i + 1) % 16]
    bm_star.faces.new([front_tip, ring_verts[i], v_next])
    bm_star.faces.new([back_tip, v_next, ring_verts[i]])

# Delicate chain around neck
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

# 4. Clean Body Mesh Protruding Hoodie Collar
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

# 5. Non-Destructive Material Binding
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

# 6. Studio Lighting & Cameras
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
key_d.energy = 55.0
key_d.size = 1.6
key_d.color = (1.0, 0.98, 0.95)
key_d.use_shadow = False
key_o = bpy.data.objects.new("Studio_Key", key_d)
key_o.location = (0.0, -1.2, 1.35)
scene.collection.objects.link(key_o)

rim_d = bpy.data.lights.new("Studio_Rim", type='AREA')
rim_d.energy = 32.0
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
cam.data.lens = 85.0

def set_camera(pos, target=Vector((0.0, 0.0, 1.28))):
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
set_camera(Vector((0.0, -0.80, 1.28)))
render_view("kagari_rebuilt_front.png")

set_camera(Vector((-0.45, -0.70, 1.30)))
render_view("kagari_rebuilt_three_quarter.png")

set_camera(Vector((-0.80, 0.0, 1.28)))
render_view("kagari_rebuilt_side.png")

set_camera(Vector((0.0, -0.50, 1.32)))
render_view("kagari_rebuilt_face.png")

OUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
print(f"SUCCESS: Saved master blend at {OUT_BLEND}")
