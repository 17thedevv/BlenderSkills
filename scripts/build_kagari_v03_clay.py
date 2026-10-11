"""One scoped low-density garment construction experiment; no ornament/export.

The existing body's skin topology supplies continuous shoulder/arm seams and
weights. Cloth ease is authored in the relaxed pose then returned to rest space.
The head, facial morphs, armature and hair are fingerprinted and left intact.
"""
import bpy
import bmesh
import math
import json
import hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path('D:/Project-17/blender')
SOURCE=ROOT/'outputs/wip/kagari_outfit_detail_v1.blend'
BASE=ROOT/'outputs/wip/kagari_v03_clay_baseline.blend'
OUT=ROOT/'outputs/wip/kagari_v03_clay_01.blend'
PRE=ROOT/'outputs/previews/v03_clay'
REPORT=ROOT/'outputs/reports/v03_clay'
PRE.mkdir(parents=True,exist_ok=True); REPORT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene; arm=bpy.data.objects['Armature']; body=bpy.data.objects['Body']

def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def protected():
    result={}
    for name in ['Face','Hair']:
        ob=bpy.data.objects[name]
        result[name]=digest({'vertices':[tuple(v.co) for v in ob.data.vertices],
            'polygons':[(tuple(p.vertices),p.material_index) for p in ob.data.polygons],
            'keys':{k.name:[tuple(v.co) for v in k.data] for k in ob.data.shape_keys.key_blocks} if ob.data.shape_keys else {},
            'key_values':{k.name:k.value for k in ob.data.shape_keys.key_blocks} if ob.data.shape_keys else {},
            'materials':[m.name if m else None for m in ob.data.materials],
            'weights':[[(g.group,g.weight) for g in v.groups] for v in ob.data.vertices],
            'groups':[g.name for g in ob.vertex_groups],
            'modifiers':[(m.name,m.type,m.object.name if m.type=='ARMATURE' and m.object else None) for m in ob.modifiers],
            'transform':[list(row) for row in ob.matrix_world]})
    result['Armature']=digest({'bones':[(b.name,b.parent.name if b.parent else None,tuple(b.head_local),tuple(b.tail_local),b.use_deform) for b in arm.data.bones],
        'pose':[(b.name,[list(row) for row in b.matrix_basis]) for b in arm.pose.bones],
        'transform':[list(row) for row in arm.matrix_world]})
    return result

def filehash(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

before=protected(); source_hash=filehash(SOURCE)
neutral_pose={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
original_body_faces=len(body.data.polygons)

# Neutral geometric display only. Original texture data and materials are intact.
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=900; scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
shade=scene.display.shading
shade.light='STUDIO'; shade.color_type='SINGLE'; shade.single_color=(.58,.58,.58)
shade.show_shadows=True; shade.show_cavity=True; shade.cavity_type='WORLD'
shade.cavity_ridge_factor=.6; shade.cavity_valley_factor=.6
shade.show_specular_highlight=False
shade.background_type='WORLD'; scene.world.color=(.15,.15,.15)
scene.view_settings.view_transform='Standard'
scene.view_settings.look='Medium High Contrast' if 'Medium High Contrast' in [e.identifier for e in scene.view_settings.bl_rna.properties['look'].enum_items] else 'None'
scene.view_settings.exposure=0; scene.view_settings.gamma=1
scene.camera.data.type='ORTHO'

# Existing decorations are consistently excluded from the neutral comparison.
decoration_words=['Piping','Gold_','Embroidered_','Brocade_','Obi_Trim','Obijime','Necklace','Pendant','Astral_Star','Stitch','Charm','Blossom','Flower']
excluded=[]
for ob in bpy.data.objects:
    if ob.name.startswith('Kagari_') and any(w in ob.name for w in decoration_words):
        ob.hide_render=True; excluded.append(ob.name)

target=Vector((0,.015,1.145))
views={
    'front':((0,-2,1.145),.85),
    'three_quarter':((-.95,-1.6,1.20),.85),
    'side':((-2,.015,1.145),.85),
    'back':((0,2,1.145),.85),
    'pose_arm_raise':((0,-2,1.145),.85),
    'portrait':((0,-2,1.21),.65),
}
renders=[]

def set_pose(raised=False):
    for name,mat in neutral_pose.items():
        arm.pose.bones[name].matrix_basis=mat.copy()
    if raised:
        for side,delta in [('L',30),('R',-30)]:
            b=arm.pose.bones['J_Bip_'+side+'_UpperArm']
            b.rotation_mode='XYZ'
            b.rotation_euler.z+=math.radians(delta)
    bpy.context.view_layer.update()

def camera(name):
    pos,scale=views[name]
    cam=scene.camera; cam.location=pos; cam.data.ortho_scale=scale
    look=target if name!='portrait' else Vector((0,.015,1.21))
    cam.rotation_euler=(look-cam.location).to_track_quat('-Z','Y').to_euler()

def render_set(prefix,artifact_hash):
    for name in views:
        set_pose(name=='pose_arm_raise'); camera(name)
        scene.render.filepath=str(PRE/(prefix+'_'+name+'_clay.png'))
        bpy.ops.render.render(write_still=True)
        renders.append({'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),
                        'artifact_sha256':artifact_hash,'view':name,'comparison':prefix,
                        'camera_location':list(scene.camera.location),'camera_rotation':list(scene.camera.rotation_euler),
                        'ortho_scale':scene.camera.data.ortho_scale,
                        'upper_arm_pose':{s:list(arm.pose.bones['J_Bip_'+s+'_UpperArm'].rotation_euler) for s in ['L','R']},
                        'isolated_garment':False})
    set_pose()
    hair_objects=[o for o in scene.objects if o.name in ['Hair','Face'] or o.name.startswith('Kagari_Silk_Bow') or o.name=='Kagari_Bow_Gathered_Knot']
    flags={o.name:o.hide_render for o in hair_objects}
    for o in hair_objects: o.hide_render=True
    for name in ['side','back']:
        camera(name)
        scene.render.filepath=str(PRE/(prefix+'_'+name+'_garment_isolated.png'))
        bpy.ops.render.render(write_still=True)
        renders.append({'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),
                        'artifact_sha256':artifact_hash,'view':name,'comparison':prefix,
                        'camera_location':list(scene.camera.location),'camera_rotation':list(scene.camera.rotation_euler),
                        'ortho_scale':scene.camera.data.ortho_scale,'isolated_garment':True,
                        'temporarily_hidden_unmodified_objects':list(flags)})
    for o in hair_objects: o.hide_render=flags[o.name]
    set_pose(); camera('front')

set_pose(); camera('front')
bpy.ops.wm.save_as_mainfile(filepath=str(BASE))
base_hash=filehash(BASE)
render_set('before',base_hash)

# Preserve source objects; only superseded garment pieces are disabled here.
superseded=[]
for ob in scene.objects:
    if ob.name.startswith(('Kagari_Haori_Cream_Shell','Kagari_Inner_Wrapped_Robe','Kagari_Collar_Under','Kagari_Collar_Over','Kagari_Haori_Lapel_')):
        ob.hide_render=True; ob.hide_set(True); superseded.append(ob.name)

skin_materials={i for i,m in enumerate(body.data.materials) if m and ('Body_00_SKIN' in m.name or 'Detail_Inner_Ivory' in m.name or 'Detail_Clean_Neck' in m.name)}
bone_mats={b.name:b.matrix @ arm.data.bones[b.name].matrix_local.inverted() for b in arm.pose.bones}

def vertex_weights(v):
    values={body.vertex_groups[g.group].name:g.weight for g in v.groups
            if g.weight>1e-8 and body.vertex_groups[g.group].name in bone_mats}
    total=sum(values.values())
    if not total:
        raise RuntimeError('Source skin vertex lacks rig weights: '+str(v.index))
    return {n:w/total for n,w in values.items()}

def blend_matrix(weights):
    m=Matrix(((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)))
    for name,w in weights.items():
        m+=bone_mats[name]*w
    return m

def smooth(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)

clay=bpy.data.materials.new('Kagari_v03_Structural_Clay')
clay.diffuse_color=(.58,.58,.58,1); clay.use_nodes=True
clay.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.58,.58,.58,1)
clay.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.85

def new_mesh(name,vs,fs,weights,thickness=.0015):
    data=bpy.data.meshes.new(name); data.from_pydata(vs,[],fs); data.update()
    bm=bmesh.new(); bm.from_mesh(data); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(data); bm.free()
    ob=bpy.data.objects.new(name,data); scene.collection.objects.link(ob)
    data.materials.append(clay)
    for p in data.polygons: p.use_smooth=True
    names=sorted({n for ws in weights for n in ws})
    groups={n:ob.vertex_groups.new(name=n) for n in names}
    for i,ws in enumerate(weights):
        for n,w in ws.items(): groups[n].add([i],w,'REPLACE')
    rig=ob.modifiers.new('Source_Weighted_Deformation','ARMATURE'); rig.object=arm
    solid=ob.modifiers.new('Cloth_Edge_Thickness','SOLIDIFY'); solid.thickness=thickness; solid.offset=0
    ob.parent=arm; ob['deformation_role']='cloth'; ob['v03_scope']='upper_garment_construction'
    return ob

def garment(inner=False):
    selected=[]
    for p in body.data.polygons:
        if p.material_index not in skin_materials: continue
        c=p.center; x=abs(c.x)
        if not (.943<c.z<1.252): continue
        if inner and x>.123: continue
        if not inner and x>.410: continue
        if x>.125 and c.z<1.145: continue
        cut=(1.177+1.12*x) if inner else (1.133+1.48*x)
        if c.y<.018 and c.z>cut: continue
        if c.z>1.243 and x<.046: continue
        selected.append(p)
    indices=sorted({i for p in selected for i in p.vertices})
    lookup={old:new for new,old in enumerate(indices)}
    faces=[tuple(lookup[i] for i in p.vertices) for p in selected]
    edge_counts={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):
            e=tuple(sorted((a,b))); edge_counts[e]=edge_counts.get(e,0)+1
    boundary={i for e,count in edge_counts.items() if count==1 for i in e}
    vertices=[]; allweights=[]; posed=[]
    for i,index in enumerate(indices):
        v=body.data.vertices[index]; co=v.co.copy(); ws=vertex_weights(v); m=blend_matrix(ws)
        if i in boundary:
            if abs(co.x)>.385 and not inner:
                co.x=math.copysign(.407,co.x)
            elif co.z<.976:
                co.z=.947
            elif co.y<.018 and abs(co.x)<.105:
                co.z=(1.177+1.12*abs(co.x)) if inner else (1.133+1.48*abs(co.x))
            elif co.z>1.232 and abs(co.x)<.075:
                co.z=1.243
        p=m@co
        n=(m.to_3x3().inverted().transposed()@v.normal).normalized()
        ease=.004 if inner else .010
        q=p+n*ease
        if not inner and abs(co.x)>.101:
            s='L' if co.x>0 else 'R'
            b=arm.pose.bones['J_Bip_'+s+'_UpperArm']; axis=(b.tail-b.head).normalized()
            radial=p-b.head-axis*(p-b.head).dot(axis)
            blend=smooth((abs(co.x)-.104)/.092)
            underside=max(0,-n.z)
            q+=radial*(.48*blend)
            q.z-=(.011+.026*underside)*blend
            # Broad diagonal folds anchored below the armhole, not periodic noise.
            armpit=math.exp(-((abs(co.x)-.165)/.044)**2)*max(0,-n.y)*max(0,1-abs(n.z))
            q+=n*(.005*armpit)
        elif not inner:
            # Shoulder-to-waist slack: one broad front fold from the armhole.
            anchor=math.exp(-((abs(co.x)-(.077+.07*(1.20-co.z)))/.025)**2)
            waist=smooth((1.20-co.z)/.18)
            if co.y<.01: q+=n*(.004*anchor*waist)
        vertices.append(tuple(m.inverted()@q)); posed.append(q); allweights.append(ws)
    if len(vertices)<100: raise RuntimeError('Source garment region extraction unexpectedly small')
    ob=new_mesh('Kagari_v03_Inner_Top' if inner else 'Kagari_v03_Outer_Robe_And_Sleeves',vertices,faces,allweights)
    return ob

outer=garment(); inner_top=garment(True)

# Remove only superseded source jacket geometry in the upper garment ROI.
# No face/skin/hair vertices or morphs are modified.
bm=bmesh.new(); bm.from_mesh(body.data)
old_faces=[f for f in bm.faces if f.material_index==2 and f.calc_center_median().z>.934]
removed=len(old_faces)
bmesh.ops.delete(bm,geom=old_faces,context='FACES_ONLY')
loose=[v for v in bm.verts if not v.link_faces]
bmesh.ops.delete(bm,geom=loose,context='VERTS')
bm.to_mesh(body.data); bm.free(); body.data.update()
bpy.context.view_layer.update()

def bvh_for(ob):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
    bv=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])
    ev.to_mesh_clear(); return bv

skin_bvh=bvh_for(body); cloth_bvh=bvh_for(outer)
# Continuous collar around nape, with one hidden under-end and one front overlap.
controls=[(.008,-.099,1.128),(.037,-.082,1.177),(.055,-.041,1.219),(.047,.011,1.242),
          (.025,.058,1.245),(0,.070,1.245),(-.025,.058,1.245),(-.047,.011,1.242),
          (-.055,-.041,1.219),(-.038,-.084,1.177),(-.002,-.106,1.132),(.066,-.109,1.050),(.097,-.101,1.002)]
def sampled(t):
    tt=t*(len(controls)-1); i=min(len(controls)-2,int(tt)); return Vector(controls[i]).lerp(Vector(controls[i+1]),tt-i)
vertices=[]; weights=[]; rows=65; cols=5
for i in range(rows):
    t=i/(rows-1); p=sampled(t)
    hit,n,idx,d=skin_bvh.find_nearest(p)
    tangent=(sampled(min(1,t+.008))-sampled(max(0,t-.008))).normalized()
    across=n.cross(tangent).normalized()
    for j in range(cols):
        u=j/(cols-1); q=hit+across*((u-.5)*.029)
        # Seam side uses the garment surface; neckline side follows skin.
        if u>.5:
            target_hit,target_n,_,dist=cloth_bvh.find_nearest(q)
            if target_hit is not None and dist<.035:
                q=q.lerp(target_hit,.65)
                q+=target_n*.002
        else:
            target_hit,target_n,_,_=skin_bvh.find_nearest(q)
            q=target_hit+target_n*.003
        q+=n*(.0015*4*u*(1-u))
        # Offset the frontmost end only at the actual overlap.
        if t>.78: q+=n*.002
        z=q.z; chest=max(0,min(1,(1.16-z)/.11))
        ws={'J_Bip_C_UpperChest':1-chest,'J_Bip_C_Chest':chest}
        ws={name:w for name,w in ws.items() if w>1e-8}
        vertices.append(tuple(blend_matrix(ws).inverted()@q)); weights.append(ws)
faces=[(i*cols+j,i*cols+j+1,(i+1)*cols+j+1,(i+1)*cols+j) for i in range(rows-1) for j in range(cols-1)]
collar=new_mesh('Kagari_v03_Sewn_Cross_Collar',vertices,faces,weights,.0014)

set_pose(); camera('front')
after=protected()
assert before==after,'Protected face/hair/rig state changed during garment construction'
assert filehash(SOURCE)==source_hash,'Original source file changed'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
out_hash=filehash(OUT)
render_set('after',out_hash)
assert filehash(OUT)==out_hash,'Candidate changed after temporary render setup'
assert filehash(BASE)==base_hash,'Frozen baseline changed'
assert protected()==before,'Temporary pose was not restored'

manifest={'schema_version':'0.3','source':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':source_hash},
          'baseline':{'path':BASE.relative_to(ROOT).as_posix(),'sha256':base_hash},
          'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':out_hash,'version':'v0.3-clay-01'},
          'concept':'outputs/design/concept_option2_kagari.jpg','renders':renders,
          'renderer':{'engine':scene.render.engine,'resolution':[900,900],'studio_light':shade.studio_light,
                      'color_type':'SINGLE','single_color':list(shade.single_color),'shadows':shade.show_shadows,
                      'cavity_ridge':shade.cavity_ridge_factor,'cavity_valley':shade.cavity_valley_factor,
                      'view_transform':scene.view_settings.view_transform,'look':scene.view_settings.look},
          'clay_excluded_existing_decorations':excluded,'superseded_garment_objects_retained_hidden':superseded,
          'body_change':{'removed_upper_source_jacket_faces':removed,'original_faces':original_body_faces,'current_faces':len(body.data.polygons)},
          'new_structural_objects':[outer.name,inner_top.name,collar.name],
          'decision':'REQUIRES_HUMAN_ART_REVIEW','vrm_export':'NOT_TESTED','warudo':'NOT_TESTED'}
(REPORT/'render_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(REPORT/'protected_invariants.json').write_text(json.dumps({'source_sha256':source_hash,'baseline_sha256':base_hash,'candidate_sha256':out_hash,
    'before':before,'after':after,'face_geometry_and_all_morphs_unchanged':before['Face']==after['Face'],
    'hair_geometry_bindings_and_materials_unchanged':before['Hair']==after['Hair'],
    'armature_and_neutral_pose_unchanged':before['Armature']==after['Armature'],
    'source_file_unchanged':filehash(SOURCE)==source_hash,'final_render_pose_restored':protected()==before},indent=2),encoding='utf-8')
print('CLAY_CANDIDATE_SAVED',OUT,out_hash)
