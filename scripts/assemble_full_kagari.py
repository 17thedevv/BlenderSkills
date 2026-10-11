"""Integrate the concept-directed garment into the complete original avatar."""
import bpy,bmesh,json,math,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path('D:/Project-17/blender'); sys.path.insert(0,str(ROOT/'scripts'))
from kagari_invariants import snapshot
REPORT=ROOT/'outputs/reports/full_concept_v3'; PRE=ROOT/'outputs/previews/full_concept_v3'
SOURCE=ROOT/'outputs/wip/kagari_v03_clay_03.blend'; STUDY=ROOT/'outputs/wip/kagari_concept_garment_v3.blend'
OUT=ROOT/'outputs/wip/kagari_full_concept_v3.blend'
for p in [REPORT,PRE,OUT.parent]: p.mkdir(parents=True,exist_ok=True)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
source_hash=sha(SOURCE); study_hash=sha(STUDY)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE)); scene=bpy.context.scene; arm=bpy.data.objects['Armature']
bpy.context.view_layer.update(); before=snapshot()
neutral={p.name:p.matrix_basis.copy() for p in arm.pose.bones}
archive=bpy.data.collections.new('ARCHIVE_Rejected_Garments_Do_Not_Export'); scene.collection.children.link(archive)
old_names=['Kagari_v03_Outer_Robe_And_Sleeves','Kagari_v03_Inner_Top','Kagari_v03_Sewn_Cross_Collar','Kagari_v03_Attached_Over_Wrap_Edge','Kagari_Obi_Woven_Band']
for name in old_names:
    o=bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    archive.objects.link(o); o.hide_render=True; o.hide_set(True); o['superseded_by']='full-concept-v1'
archive.hide_render=True; archive.hide_viewport=True
with bpy.data.libraries.load(str(STUDY),link=False) as (a,b): b.objects=['Concept_Torso_One_Long_Sleeve','Concept_Continuous_Crossed_Collar']
cloth,collar=b.objects
for o in [cloth,collar]:
    scene.collection.objects.link(o); o.parent=arm
    for m in o.modifiers:
        if m.type=='ARMATURE': m.object=arm
cloth.name='Kagari_Concept_Robe_Two_Sleeves'; collar.name='Kagari_Concept_Crossed_Collar'
source_body=bpy.data.objects['Body']; assert not source_body.data.shape_keys,'Body display extraction requires a body with no morphs'
display_body=source_body.copy(); display_body.data=source_body.data.copy(); display_body.name='Body_GarmentDisplay'
scene.collection.objects.link(display_body); display_body.hide_render=False; display_body.hide_set(False)
bm=bmesh.new(); bm.from_mesh(display_body.data)
legacy=[f for f in bm.faces if f.material_index in {2,3} or (f.material_index==4 and f.calc_center_median().z<1.005)]
removed_body_cloth_faces=len(legacy)
bmesh.ops.delete(bm,geom=legacy,context='FACES_ONLY')
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
bm.to_mesh(display_body.data); bm.free(); display_body.data.update()
for c in list(source_body.users_collection): c.objects.unlink(source_body)
archive.objects.link(source_body); source_body.hide_render=True; source_body.hide_set(True)
display_body['display_extraction']='Skin/shoes/inner upper torso from original Body; original Body and UV/material/weights remain intact in archive. Legacy lower cloth slots and inner cloth below waist removed in this display copy only.'
data=json.loads((ROOT/'outputs/reports/concept_garment_v3/panel_seams.json').read_text()); panels=data['panels']
left=panels['Left_Over_Front']; right=panels['Right_Under_Front']; back=panels['Back']
posed=[Vector(p) for p in data['authored_pose_vertices']]
start=panels['Sleeve_Front'][0][1]; old=cloth.data
coords=[v.co.copy() for v in old.vertices]; weights=[{cloth.vertex_groups[g.group].name:g.weight for g in v.groups} for v in old.vertices]
uvs=[(0,0) for _ in coords]
for poly in old.polygons:
    for li in poly.loop_indices: uvs[old.loops[li].vertex_index]=tuple(old.uv_layers.active.data[li].uv)
root_rows=len(panels['Sleeve_Front'])-1
opposite={left[i][-1]:right[i][-1] for i in range(root_rows+2)}
opposite.update({back[i][-1]:back[i][0] for i in range(root_rows+2)})
# Top fold's root shares all shoulder cross-section vertices.
top=next(s for s in data['seams'] if s['name']=='Top_Fold')['root']
for idx in top:
    target=Vector((-posed[idx].x,posed[idx].y,posed[idx].z))
    match=min(range(start),key=lambda k:(posed[k]-target).length_squared)
    assert (posed[match]-target).length<.001,'No exact opposite shoulder vertex'
    opposite[idx]=match
remove={right[root_rows][-1],back[root_rows][0],back[root_rows+1][0],right[root_rows+1][-1]}
faces=[tuple(p.vertices) for p in old.polygons if set(p.vertices)!=remove]
def mirrored_weight(w):
    return {n.replace('J_Bip_L_','J_Bip_R_'):v for n,v in w.items()}
mapping={}
def mirror(idx):
    if idx in opposite: return opposite[idx]
    if idx not in mapping:
        p=coords[idx]; mapping[idx]=len(coords)
        coords.append(Vector((-p.x,p.y,p.z))); weights.append(mirrored_weight(weights[idx])); uvs.append(uvs[idx])
    return mapping[idx]
original_sleeve=[tuple(p.vertices) for p in old.polygons if any(k>=start for k in p.vertices)]
for face in original_sleeve: faces.append(tuple(mirror(k) for k in reversed(face)))
me=bpy.data.meshes.new('Kagari_Concept_Two_Sleeve_Controlled_Panels'); me.from_pydata(coords,[],faces); me.update()
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
cloth.data=me
for g in list(cloth.vertex_groups): cloth.vertex_groups.remove(g)
groups={n:cloth.vertex_groups.new(name=n) for n in {n for w in weights for n in w}}
for i,w in enumerate(weights):
    for n,v in w.items(): groups[n].add([i],v,'REPLACE')
uv=me.uv_layers.new(name='Working_Panel_UV')
for p in me.polygons:
    p.use_smooth=True
    for li in p.loop_indices: uv.data[li].uv=uvs[me.loops[li].vertex_index]
cream=bpy.data.materials['Kagari_Detail_Cream_Silk']; burgundy=bpy.data.materials['Kagari_Detail_Burgundy']
for o,mat in [(cloth,cream),(collar,burgundy)]:
    o.data.materials.clear(); o.data.materials.append(mat)
    for p in o.data.polygons: p.material_index=0
    o['prototype_only']=False; o['full_avatar_integration']='full-concept-v1; unapproved WIP'
# A narrow waist cloth surface follows the torso and rolls at its top/bottom.
v=[]; f=[]; w=[]; N=96; ROWS=10
for row in range(ROWS+1):
    t=row/ROWS
    for j in range(N):
        a=2*math.pi*j/N
        z=.906+.071*t+.0025*math.sin(a)*math.sin(math.pi*t)
        rx=.150-.019*t+.0025*math.sin(math.pi*t)
        depth=((.151-.014*t) if math.cos(a)>0 else (.112-.015*t))+.0015*math.sin(math.pi*t)
        fold=.0022*math.exp(-((t-(.28+.11*math.sin(a)))/.11)**2)*max(0,math.cos(a))
        p=Vector((rx*math.sin(a),.008-(depth+fold)*math.cos(a),z))
        chest=.35+.15*t; ww={'J_Bip_C_Chest':chest,'J_Bip_C_Spine':1-chest}
        mat=Matrix(((0,0,0,0),)*4)
        for n,val in ww.items(): mat+=(arm.pose.bones[n].matrix@arm.data.bones[n].matrix_local.inverted())*val
        v.append(mat.inverted()@p); w.append(ww)
for i in range(ROWS):
    for j in range(N): f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
me=bpy.data.meshes.new('Kagari_Waist_Cloth_Surface'); me.from_pydata(v,[],f); me.update()
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
sash=bpy.data.objects.new('Kagari_Concept_Soft_Waist_Sash',me); scene.collection.objects.link(sash); sash.parent=arm; me.materials.append(burgundy)
groups={n:sash.vertex_groups.new(name=n) for n in ['J_Bip_C_Chest','J_Bip_C_Spine']}
for i,ww in enumerate(w):
    for n,val in ww.items(): groups[n].add([i],val,'REPLACE')
for p in me.polygons: p.use_smooth=True
uv=me.uv_layers.new(name='Working_Sash_UV')
for p in me.polygons:
    for li in p.loop_indices:
        idx=me.loops[li].vertex_index; uv.data[li].uv=(idx%N/N,idx//N/ROWS)
mod=sash.modifiers.new('Humanoid_Sash_Binding','ARMATURE'); mod.object=arm
mod=sash.modifiers.new('Thin_Cloth_Thickness','SOLIDIFY'); mod.thickness=.002; mod.offset=0
# New lower cloth shell prevents the original cut garment boundaries from showing.
v=[]; f=[]; w=[]; N=96; ROWS=30
for row in range(ROWS+1):
    t=row/ROWS
    for j in range(N):
        a=2*math.pi*j/N; rx=.143+.134*t
        depth=(.139+.064*t) if math.cos(a)>0 else (.102+.111*t)
        # Sparse vertical fold channels originate at waist and fan toward the hem.
        folds=0
        for anchor in [.46,-.55,2.65,3.70]:
            delta=(a-anchor+math.pi)%(2*math.pi)-math.pi
            folds+=math.exp(-(delta/(.075+.035*t))**2)
        relief=.0085*(t**.7)*folds
        p=Vector(((rx+relief)*math.sin(a),.008-(depth+relief)*math.cos(a),.959-.726*t+.002*math.cos(a)*t*t))
        hip=min(1,t*2); ww={'J_Bip_C_Hips':hip,'J_Bip_C_Spine':1-hip}
        mat=Matrix(((0,0,0,0),)*4)
        for n,val in ww.items(): mat+=(arm.pose.bones[n].matrix@arm.data.bones[n].matrix_local.inverted())*val
        v.append(mat.inverted()@p); w.append(ww)
for i in range(ROWS):
    for j in range(N): f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
me=bpy.data.meshes.new('Kagari_Lower_Robe_Cloth_Panels'); me.from_pydata(v,[],f); me.update()
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
lower=bpy.data.objects.new('Kagari_Concept_Lower_Robe',me); scene.collection.objects.link(lower); lower.parent=arm; me.materials.append(cream)
groups={n:lower.vertex_groups.new(name=n) for n in ['J_Bip_C_Hips','J_Bip_C_Spine']}
for i,ww in enumerate(w):
    for n,val in ww.items():
        if val>0: groups[n].add([i],val,'REPLACE')
for p in me.polygons: p.use_smooth=True
uv=me.uv_layers.new(name='Working_Lower_Robe_UV')
for p in me.polygons:
    for li in p.loop_indices:
        idx=me.loops[li].vertex_index; uv.data[li].uv=(idx%N/N,idx//N/ROWS)
mod=lower.modifiers.new('Humanoid_Lower_Robe_Binding','ARMATURE'); mod.object=arm
mod=lower.modifiers.new('Thin_Cloth_Thickness','SOLIDIFY'); mod.thickness=.0016; mod.offset=0
new=[cloth,collar,sash,lower]
bpy.context.view_layer.update(); after=snapshot(); assert before==after,'Protected avatar data changed'
scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=1000; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
shade=scene.display.shading; shade.light='STUDIO'; shade.color_type='SINGLE'; shade.single_color=(.62,.62,.62)
shade.show_shadows=True; shade.show_cavity=True; shade.cavity_type='WORLD'; shade.cavity_ridge_factor=.5; shade.cavity_valley_factor=.5
shade.show_specular_highlight=False; shade.background_type='WORLD'; scene.world.color=(.15,.15,.15)
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
cam=scene.camera; cam.data.type='ORTHO'
views={'front':((0,-2,1.16),(0,0,1.16),1.04),'three_quarter':((1.2,-1.7,1.20),(0,0,1.16),1.04),
    'side':((2,0,1.16),(0,0,1.16),1.04),'back':((0,2,1.16),(0,0,1.16),1.04),
    'arm_raised':((0,-2,1.16),(0,0,1.16),1.35),'arm_horizontal':((0,-2,1.16),(0,0,1.16),1.58),
    'full_front':((0,-3,.77),(0,0,.77),1.70),'full_three_quarter':((1.7,-2.4,.90),(0,0,.77),1.70),
    'portrait':((0,-2,1.30),(0,0,1.30),.67)}
def pose(name):
    for n,mat in neutral.items(): arm.pose.bones[n].matrix_basis=mat.copy()
    if name=='arm_raised':
        for side,delta in [('L',30),('R',-30)]: arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z+=math.radians(delta)
    if name=='arm_horizontal':
        for side in ['L','R']: arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z=0
    bpy.context.view_layer.update()
def camera(name):
    pos,target,scale=views[name]; cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=scale
pose('front'); camera('three_quarter'); bpy.ops.wm.save_as_mainfile(filepath=str(OUT)); digest=sha(OUT)
renders=[]
for name in views:
    pose(name); camera(name); scene.render.filepath=str(PRE/(name+'_clay.png')); bpy.ops.render.render(write_still=True)
    renders.append({'view':name,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
        'artifact_sha256':digest,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,
        'upper_arm_pose':{s:list(arm.pose.bones['J_Bip_'+s+'_UpperArm'].rotation_euler) for s in ['L','R']},'pose_type':'ORDINARY_ARMATURE_ONLY'})
pose('front'); camera('three_quarter'); assert snapshot()==before
assert sha(OUT)==digest and sha(SOURCE)==source_hash and sha(STUDY)==study_hash
manifest={'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':digest,'version':'full-kagari-concept-outfit-v3'},
    'baseline':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':source_hash},'garment_input':{'path':STUDY.relative_to(ROOT).as_posix(),'sha256':study_hash},
    'renders':renders,'new_objects':[o.name for o in new],'archived_objects':old_names,'original_face_hair_body_rest_rig_and_saved_pose_unchanged':True,
    'source_unchanged':True,'existing_materials_reused':['Kagari_Detail_Cream_Silk','Kagari_Detail_Burgundy'],'new_decorations':False,
    'reference':'outputs/design/concept_option2_kagari.jpg','decision':'REQUIRES_HUMAN_ART_REVIEW','human_approval':'NOT_APPROVED',
    'body_display':'Original Body remains intact and archived; Body_GarmentDisplay is an independent copy with old clothing slots2/3 and slot4 below waist removed, retaining skin/shoes/inner upper torso. No Body morphs existed.',
    'removed_legacy_cloth_faces_from_display_copy':removed_body_cloth_faces,
    'lower_garment':'New waist-to-ankle cloth shell with sparse folds; inferred lower design because concept shows only upper body. Original lower-body geometry remains in archived Body.'}
(REPORT/'render_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(REPORT/'protected_invariants.json').write_text(json.dumps({'before':before,'after':after,'identical':before==after,'source_sha256':source_hash,'candidate_sha256':digest},indent=2),encoding='utf-8')
(REPORT/'sleeve_integration.json').write_text(json.dumps({'original_sleeve_faces':len(original_sleeve),'added_vertices':len(mapping),'mapped_shared_root_vertices':len(opposite),'second_sleeve_reuses_opposite_root_indices':True,'no_mirrored_duplicate_torso':True},indent=2),encoding='utf-8')
print('FULL_KAGARI_SAVED',digest,flush=True)
