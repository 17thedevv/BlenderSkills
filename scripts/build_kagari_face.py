"""Build Kagari (篝) - Astral Shrinekeeper Head, Face, Hair & Outfit Prototype in Blender 4.2.

Creates:
- Stylized anime head/face with clean quad loops
- Amber-gold anime eyes with star and crescent catchlights
- Parted curtain bangs + low side-ponytail + crimson ribbon
- Crossover miko collar (burgundy & cream with gold trim) + astral star necklace
- Required VRM 1.0 expression shape keys: blink, blinkLeft, blinkRight, aa, ih, ou, ee, oh, happy, angry, sad, relaxed, surprised
"""
import bpy
import bmesh
import math
from mathutils import Vector, Euler, Matrix
from pathlib import Path

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)

def create_material(name, color_rgba, roughness=0.5, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color_rgba
        bsdf.inputs['Roughness'].default_value = roughness
        if emission_color and 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = emission_color
            bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

def create_anime_materials():
    mats = {}
    # Skin: soft cream-peach anime skin
    mats['skin'] = create_material('M_Kagari_Skin', (0.98, 0.92, 0.88, 1.0), roughness=0.6)
    # Blush: soft sakura pink
    mats['blush'] = create_material('M_Kagari_Blush', (1.0, 0.67, 0.65, 1.0), roughness=0.8)
    # Hair: honey brown anime hair
    mats['hair'] = create_material('M_Kagari_Hair', (0.55, 0.36, 0.25, 1.0), roughness=0.45)
    # Hair highlight: honey gold
    mats['hair_accent'] = create_material('M_Kagari_HairAccent', (0.96, 0.65, 0.15, 1.0), roughness=0.4)
    # Eyes Sclera: clean white with subtle anime lavender tint
    mats['sclera'] = create_material('M_Kagari_Sclera', (0.95, 0.95, 0.98, 1.0), roughness=0.3)
    # Eyes Iris: warm radiant amber-gold
    mats['iris'] = create_material('M_Kagari_Iris', (0.96, 0.55, 0.05, 1.0), roughness=0.2, emission_color=(0.96, 0.65, 0.14, 1.0), emission_strength=0.3)
    # Eyes Pupil & Lash: deep espresso-brown/black
    mats['lash'] = create_material('M_Kagari_Lash', (0.15, 0.10, 0.08, 1.0), roughness=0.5)
    # Eyes Catchlight: pure glowing white
    mats['catchlight'] = create_material('M_Kagari_Catchlight', (1.0, 1.0, 1.0, 1.0), roughness=0.1, emission_color=(1.0, 1.0, 1.0, 1.0), emission_strength=1.5)
    # Ribbon: deep carmine / burgundy red
    mats['ribbon'] = create_material('M_Kagari_Ribbon', (0.55, 0.12, 0.25, 1.0), roughness=0.4)
    # Gold trim / astral star: radiant warm gold
    mats['gold'] = create_material('M_Kagari_Gold', (0.90, 0.72, 0.10, 1.0), roughness=0.25)
    # Outfit Cream: cream-white kimono fabric
    mats['outfit_cream'] = create_material('M_Kagari_OutfitCream', (0.98, 0.96, 0.93, 1.0), roughness=0.6)
    # Outfit Burgundy: miko crossover collar
    mats['outfit_burgundy'] = create_material('M_Kagari_OutfitBurgundy', (0.50, 0.10, 0.22, 1.0), roughness=0.5)
    # Mouth interior: soft rosy pink
    mats['mouth'] = create_material('M_Kagari_Mouth', (0.85, 0.35, 0.40, 1.0), roughness=0.5)
    return mats

def build_head_mesh(mats):
    """Constructs stylized anime head mesh with eyelids, lips, cheeks and nose."""
    bm = bmesh.new()
    
    # Base head dimensions: Head center around Z=1.35, eye level Z=1.38, chin Z=1.18, mouth Z=1.24
    segments_u = 24
    segments_v = 18
    r_x = 0.095
    r_y = 0.115
    r_z = 0.130
    center = Vector((0.0, 0.0, 1.35))
    
    verts_grid = []
    for iv in range(segments_v + 1):
        v_frac = iv / segments_v
        theta = v_frac * math.pi
        row = []
        for iu in range(segments_u):
            u_frac = iu / segments_u
            phi = u_frac * 2.0 * math.pi
            
            x = r_x * math.sin(theta) * math.sin(phi)
            y = -r_y * math.sin(theta) * math.cos(phi) # front is -Y
            z = r_z * math.cos(theta)
            
            # Anime facial shaping:
            # 1. Taper chin in lower front quadrant (z < 0 and y < 0)
            if z < 0.0:
                taper = 1.0 - (-z / r_z) * 0.45
                x *= taper
                if y < 0.0:
                    # Pointed anime chin
                    y += (-z / r_z) * 0.025
                    # Taper jaw width
                    x *= (1.0 - (-z / r_z) * 0.2)
            
            # 2. Flatten face profile and sculpt eye recess
            if y < -0.02:
                # Cheeks slightly pronounced
                if -0.04 < z < 0.04:
                    x *= 1.05
                # Eye orbital recess around Z=0.03 to Z=0.07
                if 0.01 < z < 0.07 and abs(x) > 0.025 and abs(x) < 0.075:
                    y += 0.012  # Eye sockets recessed inward
                # Nose prominence at center front
                if -0.01 < z < 0.03 and abs(x) < 0.012:
                    y -= 0.014 * (1.0 - abs(x)/0.012)
            
            v = bm.verts.new(center + Vector((x, y, z)))
            row.append(v)
        verts_grid.append(row)
    
    # Construct quad faces
    for iv in range(segments_v):
        for iu in range(segments_u):
            next_u = (iu + 1) % segments_u
            v1 = verts_grid[iv][iu]
            v2 = verts_grid[iv][next_u]
            v3 = verts_grid[iv+1][next_u]
            v4 = verts_grid[iv+1][iu]
            
            # Avoid degenerate faces at poles
            if iv == 0:
                try:
                    bm.faces.new([v1, v3, v4])
                except ValueError:
                    pass
            elif iv == segments_v - 1:
                try:
                    bm.faces.new([v1, v2, v3])
                except ValueError:
                    pass
            else:
                try:
                    bm.faces.new([v1, v2, v3, v4])
                except ValueError:
                    pass
    
    # Build neck
    neck_center = Vector((0.0, 0.02, 1.15))
    neck_radius = 0.042
    neck_height = 0.12
    neck_verts_top = []
    neck_verts_bot = []
    for iu in range(16):
        ang = (iu / 16.0) * 2.0 * math.pi
        nx = neck_radius * math.sin(ang)
        ny = neck_radius * math.cos(ang) + 0.015
        neck_verts_top.append(bm.verts.new(Vector((nx, ny, 1.22))))
        neck_verts_bot.append(bm.verts.new(Vector((nx * 1.15, ny * 1.15, 1.12))))
    
    for iu in range(16):
        nu = (iu + 1) % 16
        bm.faces.new([neck_verts_top[iu], neck_verts_top[nu], neck_verts_bot[nu], neck_verts_bot[iu]])
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    me = bpy.data.meshes.new('Kagari_Head')
    bm.to_mesh(me)
    bm.free()
    
    obj = bpy.data.objects.new('Kagari_Head', me)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mats['skin'])
    
    # Subsurf modifier for anime smoothness
    mod = obj.modifiers.new(name='Subsurf', type='SUBSURF')
    mod.levels = 1
    mod.render_levels = 2
    
    return obj

def build_eyes(mats):
    """Builds Kagari's large amber-gold anime eyes, catchlights, and upper lash wings."""
    # Left and right eye centers
    eye_y = -0.092
    eye_z = 1.375
    eye_x = 0.046
    
    eyes_obj_list = []
    for side, sign in [('L', 1), ('R', -1)]:
        bm = bmesh.new()
        center = Vector((sign * eye_x, eye_y, eye_z))
        
        # 1. Sclera (eyeball disk curved slightly)
        w, h = 0.024, 0.028
        segs = 16
        sclera_verts = []
        c_vert = bm.verts.new(center)
        for i in range(segs):
            ang = (i / segs) * 2.0 * math.pi
            x = sign * (eye_x + w * math.cos(ang))
            y = eye_y + 0.004 * math.sin(ang)**2
            z = eye_z + h * math.sin(ang)
            sclera_verts.append(bm.verts.new(Vector((x, y, z))))
        for i in range(segs):
            ni = (i + 1) % segs
            bm.faces.new([c_vert, sclera_verts[i], sclera_verts[ni]])
            
        me_eye = bpy.data.meshes.new(f'Kagari_Sclera_{side}')
        bm.to_mesh(me_eye)
        bm.free()
        obj_sclera = bpy.data.objects.new(f'Kagari_Sclera_{side}', me_eye)
        bpy.context.scene.collection.objects.link(obj_sclera)
        obj_sclera.data.materials.append(mats['sclera'])
        eyes_obj_list.append(obj_sclera)
        
        # 2. Iris disk (amber gold with subtle curvature)
        bm = bmesh.new()
        iw, ih = 0.018, 0.023
        iris_c = bm.verts.new(center + Vector((0, -0.002, 0)))
        iris_verts = []
        for i in range(segs):
            ang = (i / segs) * 2.0 * math.pi
            x = sign * (eye_x + iw * math.cos(ang))
            y = eye_y - 0.002
            z = eye_z + ih * math.sin(ang)
            iris_verts.append(bm.verts.new(Vector((x, y, z))))
        for i in range(segs):
            ni = (i + 1) % segs
            bm.faces.new([iris_c, iris_verts[i], iris_verts[ni]])
            
        me_iris = bpy.data.meshes.new(f'Kagari_Iris_{side}')
        bm.to_mesh(me_iris)
        bm.free()
        obj_iris = bpy.data.objects.new(f'Kagari_Iris_{side}', me_iris)
        bpy.context.scene.collection.objects.link(obj_iris)
        obj_iris.data.materials.append(mats['iris'])
        eyes_obj_list.append(obj_iris)
        
        # 3. Catchlights (crescent highlight + star specular)
        bm = bmesh.new()
        # Primary crescent catchlight in bottom outer iris
        cc_center = center + Vector((sign * 0.006, -0.004, -0.007))
        bmesh.ops.create_circle(bm, cap_ends=True, radius=0.0055, segments=12, matrix=Matrix.Translation(cc_center))
        # Top secondary star catchlight
        sc_center = center + Vector((-sign * 0.005, -0.004, 0.008))
        bmesh.ops.create_circle(bm, cap_ends=True, radius=0.0035, segments=12, matrix=Matrix.Translation(sc_center))
        
        me_cl = bpy.data.meshes.new(f'Kagari_Catchlight_{side}')
        bm.to_mesh(me_cl)
        bm.free()
        obj_cl = bpy.data.objects.new(f'Kagari_Catchlight_{side}', me_cl)
        bpy.context.scene.collection.objects.link(obj_cl)
        obj_cl.data.materials.append(mats['catchlight'])
        eyes_obj_list.append(obj_cl)
        
        # 4. Stylized anime upper eyeliner lash & wing
        bm = bmesh.new()
        lash_curve_pts = [
            Vector((sign * (eye_x - 0.022), eye_y - 0.003, eye_z + 0.018)),
            Vector((sign * (eye_x - 0.010), eye_y - 0.004, eye_z + 0.028)),
            Vector((sign * eye_x,           eye_y - 0.005, eye_z + 0.030)),
            Vector((sign * (eye_x + 0.012), eye_y - 0.004, eye_z + 0.027)),
            Vector((sign * (eye_x + 0.026), eye_y - 0.003, eye_z + 0.020)),
            Vector((sign * (eye_x + 0.035), eye_y - 0.002, eye_z + 0.018)), # outer flick
        ]
        lash_thick = 0.0045
        for i in range(len(lash_curve_pts) - 1):
            p1 = lash_curve_pts[i]
            p2 = lash_curve_pts[i+1]
            t = (1.0 - abs(i - 2)/3.0) * lash_thick
            v1 = bm.verts.new(p1)
            v2 = bm.verts.new(p2)
            v3 = bm.verts.new(p2 + Vector((0, 0, t)))
            v4 = bm.verts.new(p1 + Vector((0, 0, t)))
            bm.faces.new([v1, v2, v3, v4])
            
        me_lash = bpy.data.meshes.new(f'Kagari_Lash_{side}')
        bm.to_mesh(me_lash)
        bm.free()
        obj_lash = bpy.data.objects.new(f'Kagari_Lash_{side}', me_lash)
        bpy.context.scene.collection.objects.link(obj_lash)
        obj_lash.data.materials.append(mats['lash'])
        eyes_obj_list.append(obj_lash)
        
        # 5. Eyebrow arch (clearly elevated above eye level for MediaPipe)
        bm = bmesh.new()
        brow_pts = [
            Vector((sign * (eye_x - 0.016), eye_y - 0.007, eye_z + 0.046)),
            Vector((sign * eye_x,           eye_y - 0.008, eye_z + 0.054)),
            Vector((sign * (eye_x + 0.020), eye_y - 0.007, eye_z + 0.048)),
        ]
        b_thick = 0.0035
        for i in range(len(brow_pts) - 1):
            bp1 = brow_pts[i]
            bp2 = brow_pts[i+1]
            bv1 = bm.verts.new(bp1)
            bv2 = bm.verts.new(bp2)
            bv3 = bm.verts.new(bp2 + Vector((0, 0, b_thick)))
            bv4 = bm.verts.new(bp1 + Vector((0, 0, b_thick)))
            bm.faces.new([bv1, bv2, bv3, bv4])
            
        me_brow = bpy.data.meshes.new(f'Kagari_Brow_{side}')
        bm.to_mesh(me_brow)
        bm.free()
        obj_brow = bpy.data.objects.new(f'Kagari_Brow_{side}', me_brow)
        bpy.context.scene.collection.objects.link(obj_brow)
        obj_brow.data.materials.append(mats['hair'])
        eyes_obj_list.append(obj_brow)

    return eyes_obj_list

def build_hair(mats):
    """Builds Kagari's parted curtain bangs, side locks, skull cap, and side-ponytail with ribbon."""
    hair_objs = []
    
    # 1. Skull cap base (smooth dome)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=16, radius=0.108, matrix=Matrix.Translation(Vector((0.0, 0.015, 1.365))))
    # Remove bottom hemisphere of skull cap
    for v in list(bm.verts):
        if v.co.z < 1.34:
            bm.verts.remove(v)
    me_cap = bpy.data.meshes.new('Kagari_Hair_SkullCap')
    bm.to_mesh(me_cap)
    bm.free()
    obj_cap = bpy.data.objects.new('Kagari_Hair_SkullCap', me_cap)
    bpy.context.scene.collection.objects.link(obj_cap)
    obj_cap.data.materials.append(mats['hair'])
    hair_objs.append(obj_cap)
    
    # Helper to generate tapered curved hair locks
    def create_hair_strand(name, curve_points, widths, material=mats['hair']):
        bm_s = bmesh.new()
        num_pts = len(curve_points)
        verts_left = []
        verts_right = []
        
        for i, pt in enumerate(curve_points):
            w = widths[i]
            # Normal perpendicular in XY plane
            if i < num_pts - 1:
                tangent = (curve_points[i+1] - pt).normalized()
            else:
                tangent = (pt - curve_points[i-1]).normalized()
            normal = Vector((-tangent.y, tangent.x, 0)).normalized()
            if normal.length == 0:
                normal = Vector((1, 0, 0))
            
            vl = bm_s.verts.new(pt - normal * w)
            vr = bm_s.verts.new(pt + normal * w)
            verts_left.append(vl)
            verts_right.append(vr)
            
        for i in range(num_pts - 1):
            bm_s.faces.new([verts_left[i], verts_right[i], verts_right[i+1], verts_left[i+1]])
            
        me_s = bpy.data.meshes.new(name)
        bm_s.to_mesh(me_s)
        bm_s.free()
        obj_s = bpy.data.objects.new(name, me_s)
        bpy.context.scene.collection.objects.link(obj_s)
        obj_s.data.materials.append(material)
        hair_objs.append(obj_s)
        return obj_s

    # 2. Parted Curtain Bangs (Leaves center forehead & eyebrows clear for MediaPipe tracking!)
    # Left curtain bangs (flowing outward to left temple)
    create_hair_strand('Kagari_Bangs_Left_Main', [
        Vector((0.008, -0.096, 1.445)),
        Vector((0.022, -0.106, 1.415)),
        Vector((0.040, -0.109, 1.370)),
        Vector((0.052, -0.102, 1.320)),
        Vector((0.058, -0.092, 1.280)),
    ], [0.012, 0.018, 0.016, 0.010, 0.002])
    
    create_hair_strand('Kagari_Bangs_Left_Inner', [
        Vector((0.005, -0.098, 1.440)),
        Vector((0.014, -0.108, 1.410)),
        Vector((0.026, -0.111, 1.365)),
        Vector((0.032, -0.108, 1.315)),
    ], [0.008, 0.012, 0.009, 0.002])

    # Right curtain bangs (flowing outward to right temple)
    create_hair_strand('Kagari_Bangs_Right_Main', [
        Vector((-0.008, -0.096, 1.445)),
        Vector((-0.022, -0.106, 1.415)),
        Vector((-0.040, -0.109, 1.370)),
        Vector((-0.052, -0.102, 1.320)),
        Vector((-0.058, -0.092, 1.280)),
    ], [0.012, 0.018, 0.016, 0.010, 0.002])
    
    create_hair_strand('Kagari_Bangs_Right_Inner', [
        Vector((-0.005, -0.098, 1.440)),
        Vector((-0.014, -0.108, 1.410)),
        Vector((-0.026, -0.111, 1.365)),
        Vector((-0.032, -0.108, 1.315)),
    ], [0.008, 0.012, 0.009, 0.002])

    # Center micro-accent hair strand (above eyebrow level)
    create_hair_strand('Kagari_Bangs_Center_Accent', [
        Vector((0.000, -0.099, 1.455)),
        Vector((-0.002, -0.110, 1.435)),
        Vector((-0.005, -0.112, 1.415)),
    ], [0.006, 0.008, 0.002], material=mats['hair_accent'])

    # 3. Side face-framing locks
    # Left cheek lock
    create_hair_strand('Kagari_SideLock_L', [
        Vector((0.065, -0.070, 1.420)),
        Vector((0.082, -0.080, 1.350)),
        Vector((0.088, -0.075, 1.270)),
        Vector((0.082, -0.060, 1.200)),
        Vector((0.075, -0.045, 1.150)),
    ], [0.015, 0.020, 0.016, 0.010, 0.002])
    
    # Right cheek lock
    create_hair_strand('Kagari_SideLock_R', [
        Vector((-0.065, -0.070, 1.420)),
        Vector((-0.082, -0.080, 1.350)),
        Vector((-0.088, -0.075, 1.270)),
        Vector((-0.082, -0.060, 1.200)),
        Vector((-0.075, -0.045, 1.150)),
    ], [0.015, 0.020, 0.016, 0.010, 0.002])

    # 4. Low Side-Ponytail (Draped gracefully over right shoulder)
    create_hair_strand('Kagari_Ponytail_Main', [
        Vector((-0.075, 0.000, 1.330)), # Base behind right ear
        Vector((-0.095, -0.020, 1.270)),
        Vector((-0.105, -0.045, 1.200)),
        Vector((-0.098, -0.065, 1.130)), # Draping forward over shoulder
        Vector((-0.085, -0.075, 1.070)),
        Vector((-0.070, -0.080, 1.010)),
    ], [0.025, 0.032, 0.030, 0.025, 0.018, 0.004])

    create_hair_strand('Kagari_Ponytail_Sub', [
        Vector((-0.078, 0.005, 1.325)),
        Vector((-0.102, -0.015, 1.260)),
        Vector((-0.112, -0.040, 1.190)),
        Vector((-0.105, -0.060, 1.120)),
        Vector((-0.092, -0.070, 1.050)),
    ], [0.018, 0.022, 0.020, 0.014, 0.003], material=mats['hair_accent'])

    # 5. Crimson Ribbon Bow & Tails on Side Ponytail
    bm_rib = bmesh.new()
    rib_center = Vector((-0.082, -0.010, 1.315))
    # Ribbon knot
    bmesh.ops.create_cube(bm_rib, size=0.018, matrix=Matrix.Translation(rib_center))
    # Left loop
    bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.016, radius2=0.006, depth=0.035, 
                          matrix=Matrix.Translation(rib_center + Vector((0.012, 0.020, 0.015))) @ Matrix.Rotation(math.radians(45), 4, 'X'))
    # Right loop
    bmesh.ops.create_cone(bm_rib, cap_ends=True, radius1=0.016, radius2=0.006, depth=0.035, 
                          matrix=Matrix.Translation(rib_center + Vector((-0.012, -0.020, 0.015))) @ Matrix.Rotation(math.radians(-45), 4, 'X'))
    me_rib = bpy.data.meshes.new('Kagari_Ribbon_Tie')
    bm_rib.to_mesh(me_rib)
    bm_rib.free()
    obj_rib = bpy.data.objects.new('Kagari_Ribbon_Tie', me_rib)
    bpy.context.scene.collection.objects.link(obj_rib)
    obj_rib.data.materials.append(mats['ribbon'])
    hair_objs.append(obj_rib)

    # Ribbon flowing tails
    create_hair_strand('Kagari_Ribbon_Tail1', [
        rib_center,
        rib_center + Vector((-0.015, -0.015, -0.050)),
        rib_center + Vector((-0.022, -0.025, -0.100)),
        rib_center + Vector((-0.018, -0.030, -0.150)),
    ], [0.010, 0.012, 0.009, 0.002], material=mats['ribbon'])

    return hair_objs

def build_outfit_and_collar(mats):
    """Builds Kagari's crossover miko collar (burgundy & cream with gold trim) and astral star pendant."""
    outfit_objs = []
    
    # 1. Base upper torso (shoulders & chest)
    bm_torso = bmesh.new()
    torso_verts = []
    # Build upper torso mesh
    segs = 16
    for iz, z in enumerate([1.18, 1.10, 1.00, 0.90]):
        rx = 0.08 + iz * 0.035
        ry = 0.06 + iz * 0.025
        row = []
        for i in range(segs):
            ang = (i / segs) * 2.0 * math.pi
            vx = rx * math.sin(ang)
            vy = ry * math.cos(ang)
            row.append(bm_torso.verts.new(Vector((vx, vy, z))))
        torso_verts.append(row)
        
    for iz in range(len(torso_verts) - 1):
        for i in range(segs):
            ni = (i + 1) % segs
            bm_torso.faces.new([torso_verts[iz][i], torso_verts[iz][ni], torso_verts[iz+1][ni], torso_verts[iz+1][i]])
            
    me_torso = bpy.data.meshes.new('Kagari_Torso_Base')
    bm_torso.to_mesh(me_torso)
    bm_torso.free()
    obj_torso = bpy.data.objects.new('Kagari_Torso_Base', me_torso)
    bpy.context.scene.collection.objects.link(obj_torso)
    obj_torso.data.materials.append(mats['outfit_cream'])
    outfit_objs.append(obj_torso)

    # 2. Crossover Burgundy Collar / Lapel
    bm_lapel = bmesh.new()
    lapel_pts_l = [
        Vector((0.040, 0.020, 1.16)),
        Vector((0.048, -0.040, 1.12)),
        Vector((0.025, -0.070, 1.05)),
        Vector((-0.010, -0.080, 0.98)),
    ]
    lapel_pts_r = [
        Vector((-0.040, 0.020, 1.16)),
        Vector((-0.048, -0.040, 1.12)),
        Vector((-0.025, -0.072, 1.05)),
        Vector((0.015, -0.082, 0.98)),
    ]
    w = 0.024
    for pts in [lapel_pts_l, lapel_pts_r]:
        for i in range(len(pts) - 1):
            p1 = pts[i]
            p2 = pts[i+1]
            t = Vector((0, -0.005, 0))
            v1 = bm_lapel.verts.new(p1)
            v2 = bm_lapel.verts.new(p2)
            v3 = bm_lapel.verts.new(p2 + Vector((w, 0, 0)) + t)
            v4 = bm_lapel.verts.new(p1 + Vector((w, 0, 0)) + t)
            bm_lapel.faces.new([v1, v2, v3, v4])
            
    me_lapel = bpy.data.meshes.new('Kagari_Miko_Collar')
    bm_lapel.to_mesh(me_lapel)
    bm_lapel.free()
    obj_lapel = bpy.data.objects.new('Kagari_Miko_Collar', me_lapel)
    bpy.context.scene.collection.objects.link(obj_lapel)
    obj_lapel.data.materials.append(mats['outfit_burgundy'])
    outfit_objs.append(obj_lapel)

    # 3. Gold Trim along collar edges
    bm_trim = bmesh.new()
    tw = 0.004
    for pts in [lapel_pts_l, lapel_pts_r]:
        for i in range(len(pts) - 1):
            p1 = pts[i] + Vector((0, -0.002, 0))
            p2 = pts[i+1] + Vector((0, -0.002, 0))
            v1 = bm_trim.verts.new(p1)
            v2 = bm_trim.verts.new(p2)
            v3 = bm_trim.verts.new(p2 + Vector((tw, 0, 0)))
            v4 = bm_trim.verts.new(p1 + Vector((tw, 0, 0)))
            bm_trim.faces.new([v1, v2, v3, v4])
            
    me_trim = bpy.data.meshes.new('Kagari_Gold_Trim')
    bm_trim.to_mesh(me_trim)
    bm_trim.free()
    obj_trim = bpy.data.objects.new('Kagari_Gold_Trim', me_trim)
    bpy.context.scene.collection.objects.link(obj_trim)
    obj_trim.data.materials.append(mats['gold'])
    outfit_objs.append(obj_trim)

    # 4. Astral Star Necklace & Pendant
    bm_star = bmesh.new()
    star_center = Vector((0.0, -0.068, 1.115))
    # 8-pointed star
    star_r_outer = 0.016
    star_r_inner = 0.007
    star_verts = []
    star_c = bm_star.verts.new(star_center)
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
    obj_star.data.materials.append(mats['gold'])
    outfit_objs.append(obj_star)

    return outfit_objs

def add_vrm_shape_keys(head_obj):
    """Adds the required VRM 1.0 expression shape keys to the head mesh."""
    me = head_obj.data
    # 1. Basis key
    head_obj.shape_key_add(name='Basis', from_mix=False)
    
    # Coordinates of basis vertices
    basis_coords = [Vector(v.co) for v in me.vertices]
    
    # 2. Blink keys (Upper eyelid descent)
    # Left eye center: (0.046, -0.092, 1.375)
    # Right eye center: (-0.046, -0.092, 1.375)
    def make_blink_key(name, side_filter):
        sk = head_obj.shape_key_add(name=name, from_mix=False)
        for i, co in enumerate(basis_coords):
            # Eye socket / eyelid region: Z in [1.36, 1.405], Y < -0.05
            if 1.355 <= co.z <= 1.410 and co.y < -0.05:
                # Check side
                if (side_filter == 'L' and co.x > 0.015) or \
                   (side_filter == 'R' and co.x < -0.015) or \
                   (side_filter == 'BOTH' and abs(co.x) > 0.015):
                    # Distance from upper lid center
                    eye_cx = 0.046 if co.x > 0 else -0.046
                    dist = math.sqrt((co.x - eye_cx)**2 + (co.z - 1.385)**2)
                    if dist < 0.038:
                        falloff = max(0.0, 1.0 - dist / 0.038)
                        # Descend downward and slightly outward to cover eyeball
                        new_co = Vector(co)
                        new_co.z -= 0.018 * falloff
                        new_co.y -= 0.005 * falloff
                        sk.data[i].co = new_co
        return sk

    make_blink_key('blink', 'BOTH')
    make_blink_key('blinkLeft', 'L')
    make_blink_key('blinkRight', 'R')

    # 3. Mouth Vowels / Visemes (aa, ih, ou, ee, oh)
    # Mouth center around (0.0, -0.075, 1.240)
    def make_mouth_key(name, dz, dx, dy):
        sk = head_obj.shape_key_add(name=name, from_mix=False)
        for i, co in enumerate(basis_coords):
            # Mouth region: Z in [1.21, 1.27], Y < -0.04, abs(X) < 0.045
            dist = math.sqrt(co.x**2 + (co.z - 1.240)**2 + (co.y - (-0.075))**2)
            if dist < 0.040:
                falloff = max(0.0, 1.0 - dist / 0.040)
                new_co = Vector(co)
                # Lower lip drops down
                if co.z < 1.245:
                    new_co.z += dz * falloff
                else:
                    new_co.z -= (dz * 0.3) * falloff
                # Mouth width
                new_co.x += math.copysign(dx * falloff * abs(co.x), co.x)
                new_co.y += dy * falloff
                sk.data[i].co = new_co
        return sk

    make_mouth_key('aa', -0.024, 0.15, -0.004) # Open tall & wide
    make_mouth_key('ih', -0.008, 0.35, 0.002)  # Wide slit
    make_mouth_key('ou', -0.018, -0.30, -0.010) # Puckered small circle
    make_mouth_key('ee', -0.014, 0.28, 0.001)  # Smiling open
    make_mouth_key('oh', -0.026, -0.05, -0.006) # Tall oval

    # 4. Five Primary Emotions: happy, angry, sad, relaxed, surprised
    # Happy: eye smile + lip corner lift
    sk_happy = head_obj.shape_key_add(name='happy', from_mix=False)
    for i, co in enumerate(basis_coords):
        # Mouth corners lift
        if 1.22 <= co.z <= 1.26 and abs(co.x) > 0.015:
            d = math.sqrt(co.x**2 + (co.z - 1.24)**2)
            if d < 0.035:
                sk_happy.data[i].co.z += 0.008 * (1.0 - d/0.035)
        # Eye squint upward
        if 1.35 <= co.z <= 1.38 and abs(co.x) > 0.025:
            d = math.sqrt((abs(co.x) - 0.046)**2 + (co.z - 1.37)**2)
            if d < 0.025:
                sk_happy.data[i].co.z += 0.007 * (1.0 - d/0.025)

    # Angry: eyebrows down & inward
    sk_angry = head_obj.shape_key_add(name='angry', from_mix=False)
    for i, co in enumerate(basis_coords):
        if 1.39 <= co.z <= 1.44 and abs(co.x) < 0.06:
            d = math.sqrt(co.x**2 + (co.z - 1.41)**2)
            if d < 0.045:
                sk_angry.data[i].co.z -= 0.010 * (1.0 - d/0.045)
                sk_angry.data[i].co.x *= 0.92

    # Sad: inner brows raised, mouth corners droop
    sk_sad = head_obj.shape_key_add(name='sad', from_mix=False)
    for i, co in enumerate(basis_coords):
        if 1.40 <= co.z <= 1.44 and abs(co.x) < 0.03:
            sk_sad.data[i].co.z += 0.009 * (1.0 - abs(co.x)/0.03)
        if 1.22 <= co.z <= 1.25 and abs(co.x) > 0.015:
            sk_sad.data[i].co.z -= 0.006

    # Relaxed: gentle micro-smile
    sk_relaxed = head_obj.shape_key_add(name='relaxed', from_mix=False)
    for i, co in enumerate(basis_coords):
        if 1.22 <= co.z <= 1.26 and abs(co.x) > 0.012:
            d = math.sqrt(co.x**2 + (co.z - 1.24)**2)
            if d < 0.030:
                sk_relaxed.data[i].co.z += 0.004 * (1.0 - d/0.030)

    # Surprised: eyes wide, jaw drop 'O'
    sk_surprised = head_obj.shape_key_add(name='surprised', from_mix=False)
    for i, co in enumerate(basis_coords):
        if 1.38 <= co.z <= 1.43 and abs(co.x) > 0.02:
            sk_surprised.data[i].co.z += 0.008
        if 1.20 <= co.z <= 1.25 and abs(co.x) < 0.025:
            sk_surprised.data[i].co.z -= 0.020

def setup_lighting_and_camera():
    """Sets up studio cameras and 3-point anime lighting for technical & beauty reviews."""
    # Key light: Warm soft key from front-right
    key_light_data = bpy.data.lights.new(name="Light_Key", type='AREA')
    key_light_data.energy = 80.0
    key_light_data.size = 0.8
    key_light_data.color = (1.0, 0.95, 0.90)
    key_light = bpy.data.objects.new(name="Light_Key", object_data=key_light_data)
    key_light.location = (0.5, -1.2, 1.8)
    bpy.context.scene.collection.objects.link(key_light)
    
    # Fill light: Cool soft fill from front-left
    fill_light_data = bpy.data.lights.new(name="Light_Fill", type='AREA')
    fill_light_data.energy = 40.0
    fill_light_data.size = 1.0
    fill_light_data.color = (0.90, 0.95, 1.0)
    fill_light = bpy.data.objects.new(name="Light_Fill", object_data=fill_light_data)
    fill_light.location = (-0.6, -1.0, 1.5)
    bpy.context.scene.collection.objects.link(fill_light)
    
    # Rim light: Crisp rim light from rear-right
    rim_light_data = bpy.data.lights.new(name="Light_Rim", type='AREA')
    rim_light_data.energy = 60.0
    rim_light_data.size = 0.5
    rim_light_data.color = (1.0, 0.98, 0.90)
    rim_light = bpy.data.objects.new(name="Light_Rim", object_data=rim_light_data)
    rim_light.location = (0.4, 0.8, 1.6)
    bpy.context.scene.collection.objects.link(rim_light)

    # Portrait Studio Camera
    cam_data = bpy.data.cameras.new(name="Camera_Review")
    cam_data.lens = 85.0 # Flattering portrait focal length for anime face
    cam_obj = bpy.data.objects.new(name="Camera_Review", object_data=cam_data)
    cam_obj.location = (0.0, -1.05, 1.34)
    cam_obj.rotation_euler = (math.radians(90), 0.0, 0.0)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

def main():
    print("=== BUILDING KAGARI HEAD & FACE PROTOTYPE ===")
    reset_scene()
    mats = create_anime_materials()
    head = build_head_mesh(mats)
    eyes = build_eyes(mats)
    hair = build_hair(mats)
    outfit = build_outfit_and_collar(mats)
    add_vrm_shape_keys(head)
    setup_lighting_and_camera()
    
    output_blend = Path('outputs/wip/kagari_gate_b_wip.blend')
    output_blend.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
    print(f"SUCCESS: Saved {output_blend}")

if __name__ == '__main__':
    main()
