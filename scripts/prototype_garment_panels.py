"""Independent flat-panel garment study. No rejected garment mesh is reused."""
import bpy, bmesh, json, math, hashlib, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path('D:/Project-17/blender')
SOURCE=ROOT/'outputs/wip/kagari_v03_clay_03.blend'
REPORT=ROOT/'outputs/reports/garment_reset'
PRE=ROOT/'outputs/previews/garment_reset'
RAW=ROOT/'outputs/wip/kagari_panel_seams_setup.blend'
OUT=ROOT/'outputs/wip/kagari_panel_drape_prototype_01.blend'
for p in [REPORT,PRE,OUT.parent]: p.mkdir(parents=True,exist_ok=True)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
original_sha=sha(SOURCE)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    dst.objects=['Body','Armature']
body,arm=dst.objects
scene=bpy.context.scene
for o in [body,arm]: scene.collection.objects.link(o)
body.name='Study_Duplicate_Mannequin'; arm.name='Study_Duplicate_Armature'
for mod in body.modifiers:
    if mod.type=='ARMATURE': mod.object=arm
body.parent=arm
bm=bmesh.new(); bm.from_mesh(body.data)
skin_ids={i for i,m in enumerate(body.data.materials) if m and any(s in m.name for s in ['Body_00_SKIN','Detail_Inner_Ivory','Detail_Clean_Neck'])}
remove=[f for f in bm.faces if f.material_index not in skin_ids or f.calc_center_median().z<.82 or f.calc_center_median().z>1.295]
bmesh.ops.delete(bm,geom=remove,context='FACES_ONLY')
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
bm.to_mesh(body.data); bm.free(); body.data.update()
for m in list(body.modifiers):
    if m.type!='ARMATURE': body.modifiers.remove(m)
for side,ang in [('L',-30),('R',30)]:
    arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_mode='XYZ'
    arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler=(0,0,math.radians(ang))
    arm.pose.bones['J_Bip_'+side+'_LowerArm'].rotation_mode='XYZ'
    arm.pose.bones['J_Bip_'+side+'_LowerArm'].rotation_euler=(0,0,0)
bpy.context.view_layer.update()
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
clay=bpy.data.materials.new('Study_Neutral_Clay'); clay.diffuse_color=(.62,.62,.62,1)
body.data.materials.clear(); body.data.materials.append(clay)
for p in body.data.polygons: p.material_index=0; p.use_smooth=True
# A plain head surrogate completes the duplicate mannequin, not character work.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=(0,.02,1.395))
head=bpy.context.object; head.name='Study_Plain_Mannequin_Head'; head.scale=(.086,.078,.108)
head.data.materials.append(clay)
for p in head.data.polygons: p.use_smooth=True
body.modifiers.new('Mannequin_Collision','COLLISION')
body.collision.thickness_outer=.0035; body.collision.thickness_inner=.001

vs=[]; fs=[]; ws=[]; pins=[]; panel_uv=[]; panel_ids={}; seams=[]
H=24; W=16; SW=24
def smooth(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)
def add(p,w,pin=0,uv=(0,0)):
    idx=len(vs); vs.append(tuple(p)); ws.append({n:x for n,x in w.items() if x>1e-8}); pins.append(pin); panel_uv.append(uv); return idx
def torso_weight(x,z):
    chest=smooth((1.20-z)/.18)
    shoulder=smooth((x-.07)/.09)*smooth((z-1.09)/.15)*.38
    return {'J_Bip_C_Chest':chest*(1-shoulder),'J_Bip_C_UpperChest':(1-chest)*(1-shoulder),'J_Bip_L_Shoulder':shoulder}
def front_coord(side,i,j):
    t=i/H; u=j/W
    # Opposite sloping boundaries create a real, broad front-panel overlap.
    inner=side*(.055-.143*t)
    x=inner*(1-u)+side*.158*u
    z=1.251-.287*t
    # Ease envelope is only the initial placement; free panels are then draped.
    y=-.050-(.085*smooth(t/.23))+.014*u*u
    if side<0: y+=.008
    return Vector((x,y,z))
front={}
for side,name in [(1,'Left_Over_Front'),(-1,'Right_Under_Front')]:
    ids=[]
    for i in range(H+1):
        row=[]
        for j in range(W+1):
            p=front_coord(side,i,j)
            pin=1 if i==0 else (.65 if j==0 else 0)
            row.append(add(p,torso_weight(p.x,p.z),pin,(j/W,i/H)))
        ids.append(row)
    for i in range(H):
        for j in range(W): fs.append((ids[i][j],ids[i][j+1],ids[i+1][j+1],ids[i+1][j]))
    front[side]=ids; panel_ids[name]=ids

back=[]
for i in range(H+1):
    t=i/H; row=[]
    for j in range(2*W+1):
        x=-.158+.316*j/(2*W)
        z=1.251-.287*t
        y=.080+.026*smooth(t/.22)
        if i==0 and abs(x)<.055: y=.071
        row.append(add(Vector((x,y,z)),torso_weight(x,z),1 if i==0 else 0,(j/(2*W),t)))
    back.append(row)
for i in range(H):
    for j in range(2*W): fs.append((back[i][j],back[i][j+1],back[i+1][j+1],back[i+1][j]))
panel_ids['Back_Support']=back

# Shoulder bridge panels share their inner/outer boundary vertices. Each seam
# is geometry, not a disconnected cap or texture. Centre back neck stays open.
for side in [1,-1]:
    prev=front[side][0]
    xvalues=[vs[k][0] for k in prev]
    # x samples align each front shoulder to corresponding back x positions.
    shoulder_rows=[prev]
    for step in range(1,7):
        t=step/7; row=[]
        for j,idx in enumerate(prev):
            p=Vector(vs[idx]); x=p.x
            p.y=p.y*(1-t)+.080*t
            p.z+=.016*math.sin(math.pi*t)
            row.append(add(p,torso_weight(p.x,p.z),1,(j/W,t)))
        shoulder_rows.append(row)
    # Build independent back edge matching the front's x positions; bridge onto
    # back top with matching indices through a modest ordered triangle fan.
    end=[]
    for x in xvalues:
        nearest=min(range(2*W+1),key=lambda j:abs(vs[back[0][j]][0]-x))
        end.append(back[0][nearest])
    shoulder_rows.append(end)
    for r in range(7):
        for j in range(W):
            f=(shoulder_rows[r][j],shoulder_rows[r][j+1],shoulder_rows[r+1][j+1],shoulder_rows[r+1][j])
            f=tuple(dict.fromkeys(f))
            if len(f)>=3: fs.append(f)
    seams.append({'name':'shoulder_'+str(side),'front_boundary':prev,'back_boundary':end})

# Unsleeved side: stitch torso support below the open armhole.
for i in range(9,H):
    fs.append((front[-1][i][-1],back[i][0],back[i+1][0],front[-1][i+1][-1]))

# Exactly one broad front/back sleeve rectangle, continuous with positive-X
# torso side. The top is a shoulder fold, lower edge is a hanging bag seam.
sleeve={}
for label,base in [('Sleeve_Front',front[1]),('Sleeve_Back',back)]:
    grid=[]
    for i in range(H+1):
        t=i/H; row=[base[i][-1]]
        for j in range(1,SW+1):
            u=j/SW; x=.158+.285*u
            z=1.251-.287*t
            # Soft starting roundness separates front/back sheets and provides
            # collision-free enclosing volume; not radial tube construction.
            sign=-1 if label=='Sleeve_Front' else 1
            y=sign*(.070+.027*math.sin(math.pi*t))+(.006 if sign>0 else 0)
            root=Vector(vs[row[0]])
            y=root.y*(1-smooth(u/.22))+y*smooth(u/.22)
            armw=smooth(u/.32)
            w0=ws[row[0]]; w={n:v*(1-armw) for n,v in w0.items()}
            w['J_Bip_L_UpperArm']=armw
            pin=1 if i==0 else (0.35*(1-t) if j==1 else 0)
            row.append(add(Vector((x,y,z)),w,pin,(u,t)))
        grid.append(row)
    for i in range(H):
        for j in range(SW): fs.append((grid[i][j],grid[i][j+1],grid[i+1][j+1],grid[i+1][j]))
    sleeve[label]=grid; panel_ids[label]=grid
# Close the top fold and the hanging bottom seam with narrow shared bridges.
for edge,name in [(0,'top_fold'),(H,'hanging_bottom_seam')]:
    for j in range(SW): fs.append((sleeve['Sleeve_Front'][edge][j],sleeve['Sleeve_Back'][edge][j],sleeve['Sleeve_Back'][edge][j+1],sleeve['Sleeve_Front'][edge][j+1]))
    seams.append({'name':name,'front':sleeve['Sleeve_Front'][edge],'back':sleeve['Sleeve_Back'][edge]})
# Distal seam has an opening for the forearm only at the top 100 mm.
for i in range(9,H):
    fs.append((sleeve['Sleeve_Front'][i][-1],sleeve['Sleeve_Back'][i][-1],sleeve['Sleeve_Back'][i+1][-1],sleeve['Sleeve_Front'][i+1][-1]))
seams.append({'name':'one_sleeve_torso_join','front_shared_indices':[r[-1] for r in front[1]],'back_shared_indices':[r[-1] for r in back]})

def mesh_obj(name,coords,faces,weights=None):
    me=bpy.data.meshes.new(name); me.from_pydata(coords,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); scene.collection.objects.link(ob); me.materials.append(clay)
    for p in me.polygons: p.use_smooth=True
    if weights:
        groups={n:ob.vertex_groups.new(name=n) for n in {n for w in weights for n in w}}
        for idx,w in enumerate(weights):
            total=sum(w.values())
            for n,v in w.items(): groups[n].add([idx],v/total,'REPLACE')
        mod=ob.modifiers.new('Humanoid_Study_Binding','ARMATURE'); mod.object=arm
        ob.parent=arm; ob['deformation_role']='cloth'
    return ob

cloth=mesh_obj('Panel_Torso_One_Sleeve',vs,fs,ws)
uv=cloth.data.uv_layers.new(name='Panel_Grid_UV')
for p in cloth.data.polygons:
    for li in p.loop_indices: uv.data[li].uv=panel_uv[cloth.data.loops[li].vertex_index]
pin=cloth.vertex_groups.new(name='Cloth_Structural_Anchors')
for i,w in enumerate(pins):
    if w: pin.add([i],w,'REPLACE')
mod=cloth.modifiers.new('Panel_Gravity_Drape','CLOTH')
s=mod.settings; s.quality=8; s.mass=.18
s.tension_stiffness=25; s.compression_stiffness=25; s.shear_stiffness=12; s.bending_stiffness=.28
s.tension_damping=8; s.compression_damping=8; s.shear_damping=5; s.bending_damping=.5
s.vertex_group_mass=pin.name; s.pin_stiffness=1
cs=mod.collision_settings; cs.use_collision=True; cs.distance_min=.004
cs.use_self_collision=True; cs.self_distance_min=.003; cs.collision_quality=5
mod.point_cache.frame_start=1; mod.point_cache.frame_end=65
scene.frame_start=1; scene.frame_end=65; scene.render.fps=24
cloth['construction_method']='Rectangular overlapping front panels, back support, welded shoulder bridge, one front/back sleeve bag; native Cloth drape frozen to rigged mesh.'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(RAW))
raw_hash=sha(RAW)
frames=[]; initial=None; settled=None
for frame in range(1,66):
    scene.frame_set(frame); bpy.context.view_layer.update()
    ev=cloth.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
    coords=[v.co.copy() for v in me.vertices]; ev.to_mesh_clear()
    if frame==1: initial=coords
    if frame in [1,15,30,45,65]:
        frames.append({'frame':frame,'bounds':[[min(p[k] for p in coords),max(p[k] for p in coords)] for k in range(3)]})
        print('DRAPE_FRAME',frame,flush=True)
    if frame==65: settled=coords
assert len(settled)==len(vs),'Simulation changed topology'
assert all(math.isfinite(v) for p in settled for v in p),'Non-finite cloth output'
# Convert actual posed drape back to rest space through its normalized LBS.
bone_mats={b.name:b.matrix@arm.data.bones[b.name].matrix_local.inverted() for b in arm.pose.bones}
def blend(w):
    m=Matrix(((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)))
    total=sum(w.values())
    for n,v in w.items(): m+=bone_mats[n]*(v/total)
    return m
cloth.modifiers.remove(mod)
for i,v in enumerate(cloth.data.vertices): v.co=blend(ws[i]).inverted()@settled[i]
cloth.data.update(); bpy.context.view_layer.update()

# Collar is a sewn finishing band lying directly on each broad panel's edge,
# not a separate X ribbon. Left front is visibly above right front at crossing.
collar_vs=[]; collar_fs=[]; collar_ws=[]; collar_cols=5
for side in [-1,1]:
    ids=front[side]; start=len(collar_vs)
    for i in range(H+1):
        edge=settled[ids[i][0]]; into=settled[ids[i][3]]
        for j in range(collar_cols):
            t=j/(collar_cols-1); p=edge.lerp(into,t)
            p.y-=.0025+.0014*math.sin(math.pi*t)
            w=ws[ids[i][0]]
            collar_vs.append(tuple(blend(w).inverted()@p)); collar_ws.append(w)
    for i in range(H):
        for j in range(collar_cols-1):
            a=start+i*collar_cols+j; collar_fs.append((a,a+1,a+collar_cols+1,a+collar_cols))
# Nape bridge uses explicit smoothly sampled controls, aligned to front ends.
ctrl=[settled[front[1][0][0]],Vector((.050,.022,1.264)),Vector((.037,.072,1.266)),Vector((0,.086,1.263)),Vector((-.037,.072,1.266)),Vector((-.050,.022,1.264)),settled[front[-1][0][0]]]
start=len(collar_vs); rows=37
for i in range(rows):
    t=i/(rows-1)*(len(ctrl)-1); idx=min(len(ctrl)-2,int(t)); frac=t-idx
    p=ctrl[idx].lerp(ctrl[idx+1],frac)
    for j in range(collar_cols):
        u=j/(collar_cols-1); q=p.copy(); q.z-=.031*u
        radial=Vector((q.x,q.y-.022,0)).normalized()
        q+=radial*(.002+.0014*math.sin(math.pi*u))
        w={'J_Bip_C_UpperChest':1}
        collar_vs.append(tuple(q)); collar_ws.append(w)
for i in range(rows-1):
    for j in range(collar_cols-1):
        a=start+i*collar_cols+j; collar_fs.append((a,a+1,a+collar_cols+1,a+collar_cols))
collar=mesh_obj('Sewn_Overlapping_Collar',collar_vs,collar_fs,collar_ws)
for ob in [cloth,collar]:
    thick=ob.modifiers.new('Readable_Fabric_Thickness','SOLIDIFY'); thick.thickness=.0016; thick.offset=0
    ob['prototype_only']=True

# Document planar pattern coordinates separate from draped geometry in JSON.
pattern={name:{'grid_indices':ids,'rest_pattern_coordinates':[[vs[k] for k in row] for row in ids]} for name,ids in panel_ids.items()}
(REPORT/'panel_patterns_and_seams.json').write_text(json.dumps({'panels':pattern,'seams':seams,'pins':[(i,w) for i,w in enumerate(pins) if w]},indent=2),encoding='utf-8')
drape={'source_sha256':original_sha,'raw_panel_setup':{'path':RAW.relative_to(ROOT).as_posix(),'sha256':raw_hash},
       'frames':frames,'simulation_steps':65,'fps':24,'quality':s.quality if False else 8,
       'cloth_modifiers_applied_to_static_geometry':True,'max_vertex_displacement':max((a-b).length for a,b in zip(settled,initial)),
       'mean_vertex_displacement':sum((a-b).length for a,b in zip(settled,initial))/len(initial),
       'sleeve_count':1,'no_rejected_garment_geometry_reused':True,'collision_clearance_m':.004,
       'exported_vrm':'NOT_TESTED','live_runtime':'NOT_TESTED'}
(REPORT/'drape_execution.json').write_text(json.dumps(drape,indent=2),encoding='utf-8')

scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=900; scene.render.resolution_y=900
scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'
scene.world=bpy.data.worlds.new('Study_Background'); scene.world.color=(.15,.15,.15)
shade=scene.display.shading; shade.light='STUDIO'; shade.color_type='SINGLE'; shade.single_color=(.62,.62,.62)
shade.show_shadows=True; shade.show_cavity=True; shade.cavity_type='WORLD'; shade.cavity_ridge_factor=.6; shade.cavity_valley_factor=.6
shade.show_specular_highlight=False; shade.background_type='WORLD'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Study_Review_Camera'; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=.84
target=Vector((.07,0,1.16)); views={'front':(0,-2,1.16),'three_quarter':(1.20,-1.7,1.20),'side':(2,0,1.16),'back':(0,2,1.16),'arm_raised':(0,-2,1.16)}
def set_pose(raised=False):
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    if raised: arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(30)
    bpy.context.view_layer.update()
def set_cam(name):
    cam.location=views[name]; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
scene.frame_set(1); set_pose(); set_cam('front')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT)); out_hash=sha(OUT)
renders=[]
for name in views:
    set_pose(name=='arm_raised'); set_cam(name)
    scene.render.filepath=str(PRE/('prototype_'+name+'_clay.png')); bpy.ops.render.render(write_still=True)
    renders.append({'view':name,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
                    'artifact_sha256':out_hash,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),
                    'ortho_scale':cam.data.ortho_scale,'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler),
                    'pose_type':'ORDINARY_ARMATURE_SKINNING_ONLY; no cloth solver or corrective morph after freeze'})
set_pose(); set_cam('front')
assert sha(SOURCE)==original_sha and sha(OUT)==out_hash
manifest={'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':out_hash,'version':'panel-drape-prototype-01'},
          'baseline':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':original_sha},'renders':renders,
          'mannequin_pose':'Duplicate upper arms 30 degrees down from rest; test left raised by additional 30 degrees to horizontal.',
          'decision':'REQUIRES_HUMAN_ART_REVIEW','source_unchanged':True,'original_character_geometry_modified':False,
          'prototype_objects':[cloth.name,collar.name],'construction_space':'New mannequin study, not a replacement full character',
          'raw_setup':drape['raw_panel_setup']}
(REPORT/'render_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('PANEL_PROTOTYPE_SAVED',out_hash,flush=True)
