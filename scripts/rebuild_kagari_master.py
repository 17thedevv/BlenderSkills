"""Kagari (篝) — Master Rebuild & Fidelity Recovery Script.

Transforms AvatarSample_B.blend into Kagari with strict 1:1 fidelity to concept_option2_kagari.jpg:
1. Professional texture color grading preserving all hand-painted anime line art.
2. Hair restructuring: single right side-ponytail + parted curtain bangs + removal of punk clips.
3. 3D Large Burgundy Silk Bow with flowing ribbon tails.
4. 8-Point Astral Star Pendant necklace.
5. Crossover Miko Kimono Collar (cream-white inner, burgundy outer, gold trim).
6. Non-destructive MToon material binding (preserves normal maps and matcaps).
7. Soft diffuse studio portrait lighting.
8. Multi-angle portrait renders + side-by-side concept comparison image.
"""
import bpy
import bmesh
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from mathutils import Vector, Matrix, Euler

# Paths
ROOT = Path("D:/Project-17/blender")
SRC_BLEND = ROOT / "outputs/sources/AvatarSample_B.blend"
SRC_TEX = ROOT / "outputs/sources/vroid_textures"
OUT_TEX = ROOT / "outputs/textures_kagari_vroid"
OUT_TEX.mkdir(parents=True, exist_ok=True)
OUT_BLEND = ROOT / "outputs/wip/kagari_vroid_master.blend"
PREVIEWS_DIR = ROOT / "outputs/previews/recovery"
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
CONCEPT_IMG = ROOT / "outputs/design/concept_option2_kagari.jpg"

print("--- Step 1: Generating High-Fidelity Textures ---")

# 1.1 Face Skin Texture
def make_face_skin():
    src = Image.open(SRC_TEX / "_04.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    
    # Mask scalp hair (dark purple) vs skin
    is_scalp = (arr[:, :, 2] > arr[:, :, 1] * 1.05) & (arr[:, :, 0] < 120) & (arr[:, :, 3] > 50)
    is_skin = (~is_scalp) & (arr[:, :, 3] > 50)
    
    out = arr.copy()
    
    # Porcelain peach tone curve
    r_skin = out[:, :, 0] / 255.0
    g_skin = out[:, :, 1] / 255.0
    b_skin = out[:, :, 2] / 255.0
    
    r_new = 1.0 - (1.0 - r_skin)**1.5
    g_new = 1.0 - (1.0 - g_skin)**1.9
    b_new = 1.0 - (1.0 - b_skin)**2.1
    
    out[is_skin, 0] = np.clip(r_new[is_skin] * 255.0, 0, 255)
    out[is_skin, 1] = np.clip(g_new[is_skin] * 242.0, 0, 255)
    out[is_skin, 2] = np.clip(b_new[is_skin] * 235.0, 0, 255)
    
    # Honey brown scalp hair
    lum_scalp = (0.299 * arr[is_scalp, 0] + 0.587 * arr[is_scalp, 1] + 0.114 * arr[is_scalp, 2]) / 255.0
    out[is_scalp, 0] = np.clip(lum_scalp * 350.0 + 50.0, 0, 255)
    out[is_scalp, 1] = np.clip(lum_scalp * 230.0 + 30.0, 0, 255)
    out[is_scalp, 2] = np.clip(lum_scalp * 140.0 + 15.0, 0, 255)
    
    base_im = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    
    # Clean up ear piercings on top left and top right
    draw_clean = ImageDraw.Draw(base_im)
    # Left ear piercing area: x ~ 70-130, y ~ 60-120
    # Right ear piercing area: x ~ 850-910, y ~ 60-120
    ear_skin_color = (252, 230, 222, 255)
    draw_clean.ellipse([60, 60, 140, 120], fill=ear_skin_color)
    draw_clean.ellipse([840, 60, 920, 120], fill=ear_skin_color)
    
    # Add gentle radiant peach blush matching concept art
    w, h = base_im.size
    blush_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(blush_layer)
    # Cheeks: soft warm sakura peach #FFAAA6
    draw_b.ellipse([w * 0.22, h * 0.47, w * 0.38, h * 0.57], fill=(255, 170, 166, 125))
    draw_b.ellipse([w * 0.62, h * 0.47, w * 0.78, h * 0.57], fill=(255, 170, 166, 125))
    # Soft nose contour
    draw_b.ellipse([w * 0.48, h * 0.49, w * 0.52, h * 0.52], fill=(255, 175, 165, 80))
    blush_layer = blush_layer.filter(ImageFilter.GaussianBlur(16))
    
    final_face = Image.alpha_composite(base_im, blush_layer)
    final_face.save(OUT_TEX / "kagari_face_skin.png")
    print("Saved kagari_face_skin.png")

make_face_skin()

# 1.2 Body Skin Texture
def make_body_skin():
    src = Image.open(SRC_TEX / "_10.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    out = arr.copy()
    
    # Lift skin tone to match porcelain peach
    r_skin = out[:, :, 0] / 255.0
    g_skin = out[:, :, 1] / 255.0
    b_skin = out[:, :, 2] / 255.0
    
    r_new = np.clip((1.0 - (1.0 - r_skin)**1.5) * 255.0, 0, 255)
    g_new = np.clip((1.0 - (1.0 - g_skin)**1.9) * 242.0, 0, 255)
    b_new = np.clip((1.0 - (1.0 - b_skin)**2.1) * 235.0, 0, 255)
    
    # Apply to skin areas (where not black cloth)
    is_skin = (arr[:, :, 0] > 120) & (arr[:, :, 1] > 80)
    out[is_skin, 0] = r_new[is_skin]
    out[is_skin, 1] = g_new[is_skin]
    out[is_skin, 2] = b_new[is_skin]
    
    body_im = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    draw = ImageDraw.Draw(body_im)
    
    # Clean choker around neck (x ~ 800-1250, y ~ 120-220)
    neck_skin = (252, 238, 230, 255)
    draw.rectangle([780, 120, 1270, 230], fill=neck_skin)
    # Clean chest tattoo/chain (x ~ 880-1170, y ~ 230-360)
    draw.rectangle([860, 230, 1190, 360], fill=neck_skin)
    
    body_im = body_im.filter(ImageFilter.BoxBlur(1))
    body_im.save(OUT_TEX / "kagari_body_skin.png")
    print("Saved kagari_body_skin.png")

make_body_skin()

# 1.3 Hair Textures (Honey-Brown Gradient)
def make_hair_texture(src_name, out_name):
    src = Image.open(SRC_TEX / src_name).convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    alpha = arr[:, :, 3]
    
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    out = np.zeros_like(arr)
    # Warm honey-brown gradient: shadow (70, 42, 22), mid (165, 110, 58), highlight (240, 195, 135)
    for c, (s, m, h) in enumerate([(70, 165, 240), (42, 110, 195), (22, 58, 135)]):
        val = np.where(lum < 0.5,
                       s + (m - s) * (lum / 0.5),
                       m + (h - m) * ((lum - 0.5) / 0.5))
        out[:, :, c] = val
    out[:, :, 3] = alpha
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / out_name)
    print(f"Saved {out_name}")

make_hair_texture("_15.png", "kagari_hair_01.png")
make_hair_texture("_17.png", "kagari_hair_02.png")

# 1.4 Iris Texture (Amber-Gold Sunset)
def make_iris():
    src = Image.open(SRC_TEX / "_02.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    out = arr.copy()
    is_gold = (g > 100) & (b < 180) & (a > 50)
    out[is_gold, 0] = np.clip(r[is_gold] * 1.12, 0, 255)
    out[is_gold, 1] = np.clip(g[is_gold] * 0.95, 0, 255)
    out[is_gold, 2] = np.clip(b[is_gold] * 0.65, 0, 255)
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_iris.png")
    print("Saved kagari_iris.png")

make_iris()

# 1.5 Eyebrow Texture
def make_brows():
    src = Image.open(SRC_TEX / "_07.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    alpha = arr[:, :, 3]
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    out = np.zeros_like(arr)
    out[:, :, 0] = np.clip(lum * 180 + 70, 0, 255)
    out[:, :, 1] = np.clip(lum * 120 + 40, 0, 255)
    out[:, :, 2] = np.clip(lum * 80 + 20, 0, 255)
    out[:, :, 3] = alpha
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_brows.png")
    print("Saved kagari_brows.png")

make_brows()

# 1.6 Eyeline Texture
def make_eyeline():
    src = Image.open(SRC_TEX / "_09.png").convert("RGBA")
    arr = np.array(src, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    is_pink = (r > 160) & (b > 60) & (g < 120) & (a > 30)
    out = arr.copy()
    out[is_pink, 0] = 150
    out[is_pink, 1] = 60
    out[is_pink, 2] = 40
    res = Image.fromarray(out.astype(np.uint8), mode="RGBA")
    res.save(OUT_TEX / "kagari_eyeline.png")
    print("Saved kagari_eyeline.png")

make_eyeline()

print("\n--- Step 2: Loading Base Blend & Rebuilding Geometry ---")
bpy.ops.wm.open_mainfile(filepath=str(SRC_BLEND))

# Remove default cube
cube = bpy.data.objects.get('Cube')
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)

# 2.1 Refine Hair Mesh
hair = bpy.data.objects.get('Hair')
if hair and hair.data:
    bm = bmesh.new()
    bm.from_mesh(hair.data)
    
    # Delete punk accessory faces (slots 2, 3, 4, 5)
    acc_faces = [f for f in bm.faces if f.material_index in [2, 3, 4, 5]]
    print(f"Removing {len(acc_faces)} punk accessory faces from Hair")
    bmesh.ops.delete(bm, geom=acc_faces, context='FACES_ONLY')
    
    # Delete left high twintail (character's left, viewer's right: X > 0.05, material 1, Y < 0.16)
    left_twintail = [f for f in bm.faces if f.material_index == 1 and all(v.co.x > 0.05 and v.co.y < 0.16 for v in f.verts)]
    print(f"Removing {len(left_twintail)} left twintail faces")
    bmesh.ops.delete(bm, geom=left_twintail, context='FACES_ONLY')
    
    # Reposition right side-ponytail forward over right shoulder
    # In Blender: Character right is X < -0.05.
    # We want the ponytail to drape gracefully forward (Y < 0, toward Y = -0.10) and over the shoulder.
    right_ponytail_verts = [v for v in bm.verts if v.co.x < -0.06 and v.co.z < 1.40]
    for v in right_ponytail_verts:
        # Shift forward (more negative Y) and slightly inward (less extreme negative X)
        z_factor = max(0.0, min(1.0, (1.35 - v.co.z) / 0.50))
        v.co.y -= 0.12 * z_factor   # drape forward
        v.co.x += 0.04 * z_factor   # drape over shoulder toward chest
        v.co.z -= 0.02 * z_factor   # gravity drape
        
    # Part the center curtain bangs gently to expose forehead
    # Bangs are material 0, Y < -0.05, Z between 1.30 and 1.46
    bang_verts = [v for v in bm.verts if v.co.y < -0.06 and 1.30 < v.co.z < 1.48]
    for v in bang_verts:
        # Part center: if between -0.025 and 0.0, sweep slightly right (X < -0.02)
        # if between 0.0 and +0.025, sweep slightly left (X > 0.02)
        if -0.020 < v.co.x <= 0.00:
            v.co.x -= 0.018 * (1.46 - v.co.z) / 0.16
        elif 0.00 < v.co.x < 0.020:
            v.co.x += 0.018 * (1.46 - v.co.z) / 0.16
            
    # Clean loose verts
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    
    bm.to_mesh(hair.data)
    bm.free()
    hair.data.update()
    print("Hair geometry refined successfully!")

# 2.2 Model Kagari's Large Burgundy Silk Hair Bow
print("\n--- Step 3: Modeling Large Burgundy Silk Bow ---")
ribbon_mat = bpy.data.materials.new(name="M_Kagari_Silk_Bow")
ribbon_mat.use_nodes = True
r_bsdf = ribbon_mat.node_tree.nodes.get("Principled BSDF")
if r_bsdf:
    r_bsdf.inputs['Base Color'].default_value = (0.58, 0.09, 0.22, 1.0) # Deep Carmine Burgundy #8B1E3F
    r_bsdf.inputs['Roughness'].default_value = 0.35

bm_bow = bmesh.new()
# Position at ponytail base near right ear / neck: X = -0.105, Y = -0.010, Z = 1.330
rc = Vector((-0.105, -0.010, 1.330))

# Center knot
bmesh.ops.create_cube(bm_bow, size=0.026, matrix=Matrix.Translation(rc))

# Left upper wing
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.034, radius2=0.010, depth=0.075,
                      matrix=Matrix.Translation(rc + Vector((0.020, 0.026, 0.032))) @ Matrix.Rotation(math.radians(52), 4, 'X') @ Matrix.Rotation(math.radians(22), 4, 'Z'))

# Right lower wing
bmesh.ops.create_cone(bm_bow, cap_ends=True, radius1=0.034, radius2=0.010, depth=0.075,
                      matrix=Matrix.Translation(rc + Vector((-0.020, -0.026, 0.032))) @ Matrix.Rotation(math.radians(-52), 4, 'X') @ Matrix.Rotation(math.radians(-22), 4, 'Z'))

# Flowing silk ribbon tails curving down over shoulder
tail_pts = [
    rc + Vector((0.005, -0.015, -0.005)),
    rc + Vector((-0.018, -0.040, -0.070)),
    rc + Vector((-0.028, -0.065, -0.150)),
    rc + Vector((-0.022, -0.075, -0.230)),
]
vl, vr = [], []
for i, pt in enumerate(tail_pts):
    w = 0.020 if i < 2 else (0.014 if i == 2 else 0.004)
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

arm = bpy.data.objects.get('Armature')
if arm:
    obj_bow.parent = arm
    obj_bow.parent_type = 'BONE'
    obj_bow.parent_bone = 'J_Bip_C_Head'

# 2.3 Model 8-Point Astral Star Pendant & Gold Chain
print("\n--- Step 4: Modeling Astral Star Pendant & Gold Chain ---")
gold_mat = bpy.data.materials.new(name="M_Kagari_Astral_Gold")
gold_mat.use_nodes = True
g_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.95, 0.76, 0.12, 1.0) # Astral Gold #E6B800
    g_bsdf.inputs['Roughness'].default_value = 0.20
    g_bsdf.inputs['Metallic'].default_value = 0.85

bm_star = bmesh.new()
# Pendant hollow of neck at X = 0, Y = -0.076, Z = 1.155
sc = Vector((0.0, -0.076, 1.155))
star_c = bm_star.verts.new(sc)
sv = []
for i in range(16):
    ang = (i / 16.0) * 2.0 * math.pi
    r = 0.022 if i % 2 == 0 else 0.010
    sv.append(bm_star.verts.new(Vector((sc.x + r * math.sin(ang), sc.y - 0.003, sc.z + r * math.cos(ang)))))
for i in range(16):
    bm_star.faces.new([star_c, sv[i], sv[(i + 1) % 16]])

# Gold chain around neck
chain_pts = []
for i in range(25):
    ang = -math.pi * 0.40 + (i / 24.0) * math.pi * 0.80
    cx = 0.065 * math.sin(ang)
    cy = -0.035 - 0.040 * math.cos(ang)
    cz = 1.155 + 0.045 * (1.0 - math.cos(ang))
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
    obj_star.parent_type = 'BONE'
    obj_star.parent_bone = 'J_Bip_C_UpperChest'

# 2.4 Model Crossover Miko Kimono Collar
print("\n--- Step 5: Modeling Crossover Miko Kimono Collar ---")
miko_inner_mat = bpy.data.materials.new(name="M_Kagari_Kimono_Inner")
miko_inner_mat.use_nodes = True
mi_bsdf = miko_inner_mat.node_tree.nodes.get("Principled BSDF")
if mi_bsdf:
    mi_bsdf.inputs['Base Color'].default_value = (1.0, 0.98, 0.95, 1.0) # Cream-White #FFF9F2
    mi_bsdf.inputs['Roughness'].default_value = 0.60

miko_outer_mat = bpy.data.materials.new(name="M_Kagari_Kimono_Burgundy")
miko_outer_mat.use_nodes = True
mo_bsdf = miko_outer_mat.node_tree.nodes.get("Principled BSDF")
if mo_bsdf:
    mo_bsdf.inputs['Base Color'].default_value = (0.55, 0.10, 0.22, 1.0) # Burgundy #8B1E3F
    mo_bsdf.inputs['Roughness'].default_value = 0.50

# Collar mesh: Crossover V-neck
bm_collar = bmesh.new()

# Inner white collar band (crossing left to right)
# Left band
l_pts = [
    Vector((0.045, -0.065, 1.180)),
    Vector((0.020, -0.080, 1.135)),
    Vector((-0.015, -0.084, 1.080)),
]
# Right band (outer burgundy crossing over)
r_pts = [
    Vector((-0.055, -0.065, 1.185)),
    Vector((-0.025, -0.082, 1.140)),
    Vector((0.035, -0.086, 1.075)),
]

def make_ribbon_strip(bm, pts, width, mat_idx, normal_offset=Vector((0, -0.005, 0))):
    v_l, v_r = [], []
    for i, p in enumerate(pts):
        tang = (pts[min(len(pts)-1, i+1)] - pts[max(0, i-1)]).normalized()
        perp = Vector((-tang.z, 0, tang.x)).normalized() * width
        v_l.append(bm.verts.new(p + perp + normal_offset))
        v_r.append(bm.verts.new(p - perp + normal_offset))
    for i in range(len(pts) - 1):
        f = bm.faces.new([v_l[i], v_r[i], v_r[i+1], v_l[i+1]])
        f.material_index = mat_idx

# White inner collar (width 0.016, mat 0)
make_ribbon_strip(bm_collar, l_pts, 0.016, 0, Vector((0, -0.002, 0)))
# Burgundy outer collar (width 0.024, mat 1)
make_ribbon_strip(bm_collar, r_pts, 0.024, 1, Vector((0, -0.006, 0)))

# Gold border trim on outer collar
make_ribbon_strip(bm_collar, r_pts, 0.004, 2, Vector((-0.024, -0.007, 0)))

me_collar = bpy.data.meshes.new("Kagari_Miko_Kimono_Collar")
bm_collar.to_mesh(me_collar)
bm_collar.free()
obj_collar = bpy.data.objects.new("Kagari_Miko_Kimono_Collar", me_collar)
bpy.context.scene.collection.objects.link(obj_collar)
obj_collar.data.materials.append(miko_inner_mat)
obj_collar.data.materials.append(miko_outer_mat)
obj_collar.data.materials.append(gold_mat)
for poly in obj_collar.data.polygons:
    poly.use_smooth = True

if arm:
    obj_collar.parent = arm
    obj_collar.parent_type = 'BONE'
    obj_collar.parent_bone = 'J_Bip_C_UpperChest'

# Hide or clean punk hoodie jacket on Body mesh
body = bpy.data.objects.get('Body')
if body and body.data:
    bm_b = bmesh.new()
    bm_b.from_mesh(body.data)
    # Remove punk hoodie jacket faces (material 2) around the upper neck/collar area
    jacket_neck = [f for f in bm_b.faces if f.material_index == 2 and any(v.co.z > 1.15 for v in f.verts)]
    print(f"Removing {len(jacket_neck)} protruding hoodie collar faces")
    bmesh.ops.delete(bm_b, geom=jacket_neck, context='FACES_ONLY')
    bm_b.to_mesh(body.data)
    bm_b.free()
    body.data.update()

print("\n--- Step 6: Precise Non-Destructive Material Binding ---")
def bind_mtoon_texture(mat_name, image_path):
    mat = bpy.data.materials.get(mat_name)
    if not mat or not mat.node_tree:
        print(f"Warning: Material {mat_name} not found")
        return
    img = bpy.data.images.load(str(image_path), check_existing=True)
    # Bind ONLY to BaseColor and ShadeMultiply! Preserve Normal & Matcap!
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

# Body skin texture
bind_mtoon_texture("N00_000_00_Body_00_SKIN (Instance)", OUT_TEX / "kagari_body_skin.png")
bind_mtoon_texture("MToon Outline (N00_000_00_Body_00_SKIN (Instance))", OUT_TEX / "kagari_body_skin.png")

# Hair textures
bind_mtoon_texture("N00_000_Hair_00_HAIR_01 (Instance)", OUT_TEX / "kagari_hair_01.png")
bind_mtoon_texture("MToon Outline (N00_000_Hair_00_HAIR_01 (Instance))", OUT_TEX / "kagari_hair_01.png")
bind_mtoon_texture("N00_000_Hair_00_HAIR_02 (Instance)", OUT_TEX / "kagari_hair_02.png")
bind_mtoon_texture("MToon Outline (N00_000_Hair_00_HAIR_02 (Instance))", OUT_TEX / "kagari_hair_02.png")

print("\n--- Step 7: Studio Lighting & Camera Setup ---")
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 768
scene.render.resolution_y = 1024

# Clear lights
for l in list(bpy.data.lights):
    bpy.data.lights.remove(l)

# Soft Studio World
if not scene.world:
    scene.world = bpy.data.worlds.new("Kagari_World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.98, 0.97, 0.96, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Soft diffuse front key light without harsh shadow tearing
key_d = bpy.data.lights.new("Studio_Key", type='AREA')
key_d.energy = 50.0
key_d.size = 1.5
key_d.color = (1.0, 0.98, 0.95)
key_d.use_shadow = False
key_o = bpy.data.objects.new("Studio_Key", key_d)
key_o.location = (0.0, -1.2, 1.35)
scene.collection.objects.link(key_o)

# Subtle warm rim light
rim_d = bpy.data.lights.new("Studio_Rim", type='AREA')
rim_d.energy = 30.0
rim_d.size = 1.2
rim_d.color = (1.0, 0.95, 0.88)
rim_d.use_shadow = False
rim_o = bpy.data.objects.new("Studio_Rim", rim_d)
rim_o.location = (0.5, 0.8, 1.5)
scene.collection.objects.link(rim_o)

# Camera
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

print("\n--- Step 8: Multi-Angle Renders ---")
set_camera(Vector((0.0, -0.80, 1.28)))
f_front = render_view("kagari_rebuilt_front.png")

set_camera(Vector((-0.45, -0.70, 1.30)))
f_tq = render_view("kagari_rebuilt_three_quarter.png")

set_camera(Vector((-0.80, 0.0, 1.28)))
f_side = render_view("kagari_rebuilt_side.png")

set_camera(Vector((0.0, -0.50, 1.32)))
f_face = render_view("kagari_rebuilt_face.png")

# Save master WIP blend
OUT_BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
print(f"SUCCESS: Saved {OUT_BLEND}")

print("\n--- Step 9: Assembling Side-by-Side Review Image ---")
if CONCEPT_IMG.exists():
    c_img = Image.open(CONCEPT_IMG).convert("RGB")
    m_img = Image.open(f_front).convert("RGB")
    
    # Resize to equal height
    h = 1024
    w_c = int(c_img.width * (h / c_img.height))
    w_m = int(m_img.width * (h / m_img.height))
    c_resized = c_img.resize((w_c, h), Image.Resampling.LANCZOS)
    m_resized = m_img.resize((w_m, h), Image.Resampling.LANCZOS)
    
    # Stitch side by side
    combo = Image.new("RGB", (w_c + w_m + 20, h), (30, 30, 35))
    combo.paste(c_resized, (0, 0))
    combo.paste(m_resized, (w_c + 20, 0))
    
    # Add labels
    draw = ImageDraw.Draw(combo)
    draw.rectangle([10, 10, 240, 45], fill=(0, 0, 0, 180))
    draw.text((20, 18), "2D Concept (Authoritative)", fill=(255, 220, 100))
    draw.rectangle([w_c + 30, 10, w_c + 270, 45], fill=(0, 0, 0, 180))
    draw.text((w_c + 40, 18), "3D Blender Prototype", fill=(100, 220, 255))
    
    combo_path = PREVIEWS_DIR / "kagari_side_by_side_review.png"
    combo.save(combo_path)
    print(f"SUCCESS: Assembled side-by-side review image at {combo_path}")
