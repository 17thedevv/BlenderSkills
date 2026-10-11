"""Concept-directed, controlled cloth sheets; no reuse of rejected garment mesh."""
import bpy, bmesh, json, math, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path('D:/Project-17/blender')
REPORT=ROOT/'outputs/reports/concept_garment_v3'; PRE=ROOT/'outputs/previews/concept_garment_v3'
OUT=ROOT/'outputs/wip/kagari_concept_garment_v3.blend'
SOURCE=ROOT/'outputs/wip/kagari_v03_clay_03.blend'
PRIOR=ROOT/'outputs/wip/kagari_panel_drape_reset_final.blend'
for p in [REPORT,PRE,OUT.parent]: p.mkdir(parents=True,exist_ok=True)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
source_hash=sha(SOURCE); prior_hash=sha(PRIOR)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(PRIOR),link=False) as (a,b):
    b.objects=['Study_Duplicate_Mannequin','Study_Duplicate_Armature','Study_Plain_Mannequin_Head']
body,arm,head=b.objects
scene=bpy.context.scene
for o in [body,arm,head]: scene.collection.objects.link(o)
for mod in list(body.modifiers):
    if mod.type=='ARMATURE': mod.object=arm
    else: body.modifiers.remove(mod)
body.parent=arm
for side,angle in [('L',-60),('R',60)]:
    arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_mode='XYZ'
    arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler=(0,0,math.radians(angle))
    arm.pose.bones['J_Bip_'+side+'_LowerArm'].rotation_euler=(0,0,0)
bpy.context.view_layer.update()
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
bone_mats={b.name:b.matrix@arm.data.bones[b.name].matrix_local.inverted() for b in arm.pose.bones}
ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
body_bvh=BVHTree.FromPolygons([v.co.copy() for v in me.vertices],[list(p.vertices) for p in me.polygons])
ev.to_mesh_clear()
clay=bpy.data.materials.new('Concept_Study_Neutral_Clay'); clay.diffuse_color=(.65,.65,.65,1)
for ob in [body,head]:
    ob.data.materials.clear(); ob.data.materials.append(clay)
    for p in ob.data.polygons: p.material_index=0
def smooth(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)
def mix(a,b,t): return a*(1-t)+b*t
def blend(w):
    m=Matrix(((0,0,0,0),)*4)
    for n,v in w.items(): m+=bone_mats[n]*v
    return m
def normalize(w):
    w={n:v for n,v in w.items() if v>1e-6}; total=sum(w.values())
    return {n:v/total for n,v in w.items()}
def torso_w(x,z):
    upper=smooth((z-1.075)/.115)
    side='L' if x>=0 else 'R'
    sh=.18*smooth((abs(x)-.05)/.074)*smooth((z-1.1)/.13)
    ua=.52*smooth((abs(x)-.068)/.052)*smooth((z-1.10)/.105)
    return normalize({'J_Bip_C_Chest':(1-upper)*(1-sh-ua),'J_Bip_C_UpperChest':upper*(1-sh-ua),
                     'J_Bip_'+side+'_Shoulder':sh,'J_Bip_'+side+'_UpperArm':ua})
def clear_body(p,gap=.007):
    # Only correct local body intrusions; do not shrinkwrap the whole surface.
    near=body_bvh.find_nearest(p)
    if near and near[0] is not None:
        q,n,idx,d=near
        signed=(p-q).dot(n)
        if d<.055 and signed<gap: p=p+n*(gap-signed)
    return p
vs=[]; fs=[]; ws=[]; uvs=[]; panels={}; seam_records=[]
def add(p,w,uv=(0,0)):
    idx=len(vs); vs.append(Vector(p)); ws.append(normalize(w)); uvs.append(uv); return idx
H=30; W=20; ROOT_ROWS=15; LENGTH=30; BRIDGE=8
def coords_front(side,i,j):
    t=i/H; u=j/W
    width=.122-.017*smooth((t-.40)/.6)
    inner=side*(.044-.102*smooth(t))
    x=mix(inner,side*width,u)
    z=mix(1.260-.043*smooth(u),.975,t)
    # Torso depth varies with bust and waist; side seams wrap around the body.
    depth=.057+.098*smooth(t/.26)-.029*smooth((t-.6)/.4)
    y=.021-depth*(max(.025,1-(abs(x)/(width+.009))**2))**.24
    fold=.0045*math.exp(-((u-.63-.1*t)/.13)**2)*math.sin(math.pi*t)
    fold+=.0055*math.exp(-((t-(.72+.13*u))/.028)**2)*math.sin(math.pi*u)
    fold+=.0035*math.exp(-((t-(.91-.06*u))/.022)**2)*math.sin(math.pi*u)
    y-=fold
    # Front-directed clearance preserves a broad fabric envelope over the bust.
    hit=body_bvh.ray_cast(Vector((x,-1,z)),Vector((0,1,0)),2)
    if hit[0] is not None: y=min(y,hit[0].y-.016)
    if side<0: y+=.007*smooth(t/.4)
    else: y-=.004*smooth(t/.4)
    return Vector((x,y,z))
front={}
for side,name in [(1,'Left_Over_Front'),(-1,'Right_Under_Front')]:
    grid=[]
    for i in range(H+1):
        row=[]
        for j in range(W+1):
            p=coords_front(side,i,j); row.append(add(p,torso_w(p.x,p.z),(j/W,i/H)))
        grid.append(row)
    for i in range(H):
        for j in range(W): fs.append((grid[i][j],grid[i][j+1],grid[i+1][j+1],grid[i+1][j]))
    front[side]=grid; panels[name]=grid
back=[]
back_top_x=[vs[k].x for k in reversed(front[-1][0])]+[-.022,0,.022]+[vs[k].x for k in front[1][0]]
BW=len(back_top_x)-1
for i in range(H+1):
    t=i/H; width=.122-.017*smooth((t-.4)/.6); row=[]
    for j in range(BW+1):
        u=j/BW; x=back_top_x[j]/.122*width
        z=mix(1.260-.043*smooth((abs(back_top_x[j])-.044)/.078),.975,t)
        y=.021+(.046+.022*smooth(t/.3))*math.sqrt(max(.025,1-(abs(x)/(width+.009))**2))
        y+=.0035*math.exp(-((abs(x)-.068+.012*t)/.020)**2)*math.sin(math.pi*t)
        hit=body_bvh.ray_cast(Vector((x,1,z)),Vector((0,-1,0)),2)
        if hit[0] is not None: y=max(y,hit[0].y+.009)
        p=Vector((x,y,z)); row.append(add(p,torso_w(p.x,p.z),(u,t)))
    back.append(row)
for i in range(H):
    for j in range(BW): fs.append((back[i][j],back[i][j+1],back[i+1][j+1],back[i+1][j]))
panels['Back']=back
# Each shoulder bridge has the same sampling on front/back, without fans.
shoulder_outer={}
for side in [1,-1]:
    first=front[side][0]; end=[]
    for j in range(W+1):
        x=vs[first[j]].x
        nearest=W-j if side<0 else W+4+j
        end.append(back[0][nearest])
    rows=[first]
    for r in range(1,BRIDGE):
        t=r/BRIDGE; row=[]
        for j,(a,b) in enumerate(zip(first,end)):
            p=vs[a].lerp(vs[b],t)
            p.z+=.010*math.sin(math.pi*t)*(1-.35*j/W)
            hit=body_bvh.ray_cast(Vector((p.x,p.y,1.5)),Vector((0,0,-1)),.35)
            if hit[0] is not None and hit[1].z>.2: p.z=max(p.z,hit[0].z+.007)
            row.append(add(p,torso_w(p.x,p.z),(j/W,t)))
        rows.append(row)
    rows.append(end)
    for a,b in zip(rows,rows[1:]):
        for j in range(W):
            face=tuple(dict.fromkeys((a[j],a[j+1],b[j+1],b[j])))
            if len(face)>=3: fs.append(face)
    shoulder_outer[side]=[row[-1] for row in rows]
    seam_records.append({'name':'Curved_Shoulder_'+str(side),'front':first,'back':end})
# Negative side closes below its open armhole; positive side closes at sleeve bag root.
for side in [-1,1]:
    bindex=0 if side<0 else -1
    for i in range(ROOT_ROWS+(1 if side>0 else 0),H):
        fs.append((front[side][i][-1],back[i][bindex],back[i+1][bindex],front[side][i+1][-1]))
sleeves={}
for label,base,sign in [('Sleeve_Front',front[1],-1),('Sleeve_Back',back,1)]:
    grid=[]
    for i in range(ROOT_ROWS+1):
        t=i/ROOT_ROWS; root=base[i][-1]; row=[root]
        for j in range(1,LENGTH+1):
            s=j/LENGTH; r=vs[root]
            cuff=Vector((.341-.120*smooth(t),.021+sign*(.049+.015*math.sin(math.pi*t)),.855-.137*t))
            p=r.lerp(cuff,s)
            p.x+=.010*math.sin(math.pi*s)*math.sin(math.pi*t)
            # Smooth bag fullness, then two large controlled valleys.
            p.y+=sign*(.027*math.sin(math.pi*s)*math.sin(math.pi*t))
            p.y+=sign*(-.007*math.exp(-((t-.46-.18*s)/.13)**2)*math.sin(math.pi*s))
            p.z-=.012*math.sin(math.pi*s)*smooth(t)
            p=clear_body(p,.008)
            move=smooth(s/.36)
            lower=smooth((s-.37)/.47)*.82
            w={n:v*(1-move) for n,v in ws[root].items()}
            w['J_Bip_L_UpperArm']=w.get('J_Bip_L_UpperArm',0)+move*(1-lower)
            w['J_Bip_L_LowerArm']=move*lower
            row.append(add(p,w,(s,t)))
        grid.append(row)
    for i in range(ROOT_ROWS):
        for j in range(LENGTH): fs.append((grid[i][j],grid[i][j+1],grid[i+1][j+1],grid[i+1][j]))
    sleeves[label]=grid; panels[label]=grid
# Rounded sleeve top/bottom surfaces, sharing the anatomical root shoulder edge.
for i,label in [(0,'Top_Fold'),(ROOT_ROWS,'Bottom_Seam')]:
    rows=[sleeves['Sleeve_Front'][i]]
    for r in range(1,BRIDGE):
        t=r/BRIDGE; row=[]
        if i==0: row.append(shoulder_outer[1][r])
        else:
            a=sleeves['Sleeve_Front'][i][0]; b=sleeves['Sleeve_Back'][i][0]
            row.append(add(vs[a].lerp(vs[b],t),normalize({**ws[a]})))
        for j in range(1,LENGTH+1):
            a=sleeves['Sleeve_Front'][i][j]; b=sleeves['Sleeve_Back'][i][j]
            p=vs[a].lerp(vs[b],t)
            p.z+=(1 if i==0 else -1)*(.011 if i==0 else .006)*math.sin(math.pi*t)
            w={n:ws[a].get(n,0)*(1-t)+ws[b].get(n,0)*t for n in ws[a].keys()|ws[b].keys()}
            row.append(add(clear_body(p,.008),w,(j/LENGTH,t)))
        rows.append(row)
    rows.append(sleeves['Sleeve_Back'][i])
    for a,b in zip(rows,rows[1:]):
        for j in range(LENGTH): fs.append((a[j],a[j+1],b[j+1],b[j]))
    if i==ROOT_ROWS:
        root_indices=[row[0] for row in rows]
        for a,b in zip(root_indices,root_indices[1:]):
            # Root rounding joins the torso side closure, no hanging gusset slit.
            fs.append((a,b,front[1][ROOT_ROWS+1][-1]))
        fs.append((root_indices[-1],back[ROOT_ROWS+1][-1],front[1][ROOT_ROWS+1][-1]))
    seam_records.append({'name':label,'root': [row[0] for row in rows]})
def mesh_obj(name,coords,faces,weights,texcoords):
    rest=[blend(w).inverted()@p for p,w in zip(coords,weights)]
    me=bpy.data.meshes.new(name); me.from_pydata(rest,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); scene.collection.objects.link(ob); ob.parent=arm; me.materials.append(clay)
    groups={n:ob.vertex_groups.new(name=n) for n in {n for w in weights for n in w}}
    for i,w in enumerate(weights):
        for n,v in w.items(): groups[n].add([i],v,'REPLACE')
    mod=ob.modifiers.new('Conventional_Humanoid_Skinning','ARMATURE'); mod.object=arm
    uv=me.uv_layers.new(name='Working_Panel_UV')
    for p in me.polygons:
        p.use_smooth=True
        for li in p.loop_indices: uv.data[li].uv=texcoords[me.loops[li].vertex_index]
    thick=ob.modifiers.new('Fabric_Thickness','SOLIDIFY'); thick.thickness=.0015; thick.offset=0
    ob['construction']='New manually controlled cloth sheets fitted to the Kagari front concept; no Cloth simulation.'
    ob['prototype_only']=True
    return ob
cloth=mesh_obj('Concept_Torso_One_Long_Sleeve',vs,fs,ws,uvs)
# Collar follows supporting front panels exactly; 4 cm band tapers toward waist.
cv=[]; cf=[]; cw=[]; cu=[]; leaves={}
for side in [-1,1]:
    ids=[]
    for i in range((18 if side<0 else H)+1):
        row=[]
        for j in range(7):
            u=j/6; sample=u*(7.5-1.4*i/H)
            k=int(sample); f=sample-k; grid=front[side][i]
            p=vs[grid[k]].lerp(vs[grid[k+1]],f)
            # Consistent panel stack: positive-X leaf lies in front of negative-X.
            p.y-=.0032+.0012*math.sin(math.pi*u)
            row.append(len(cv)); cv.append(p); cw.append(ws[grid[k]]); cu.append((u,i/H))
        ids.append(row)
    for a,b in zip(ids,ids[1:]):
        for j in range(6): cf.append((a[j],a[j+1],b[j+1],b[j]))
    leaves[side]=ids
# Nape endpoint vertices are the actual collar leaf endpoints, not separate bands.
def catmull(ctrl,t):
    p=t*(len(ctrl)-1); i=min(len(ctrl)-2,int(p)); u=p-i
    a,b,c,d=ctrl[max(0,i-1)],ctrl[i],ctrl[i+1],ctrl[min(len(ctrl)-1,i+2)]
    return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
left=leaves[1][0]; right=leaves[-1][0]
ctrl=[cv[left[0]],Vector((.047,.005,1.272)),Vector((.038,.059,1.278)),Vector((0,.067,1.279)),Vector((-.038,.059,1.278)),Vector((-.047,.005,1.272)),cv[right[0]]]
rows=[left]; startvec=cv[left[-1]]-cv[left[0]]; endvec=cv[right[-1]]-cv[right[0]]
for r in range(1,48):
    t=r/48; p=catmull(ctrl,t); radial=Vector((p.x,p.y-.021,0)).normalized()
    vec=radial*.014+Vector((0,0,-.029))
    if t<.24: vec=startvec.lerp(vec,smooth(t/.24))
    if t>.76: vec=vec.lerp(endvec,smooth((t-.76)/.24))
    row=[]
    for j in range(7):
        u=j/6; q=p+vec*u+radial*.001*math.sin(math.pi*u)
        row.append(len(cv)); cv.append(q); cw.append({'J_Bip_C_UpperChest':1}); cu.append((u,t))
    rows.append(row)
rows.append(right)
for a,b in zip(rows,rows[1:]):
    for j in range(6): cf.append((a[j],a[j+1],b[j+1],b[j]))
collar=mesh_obj('Concept_Continuous_Crossed_Collar',cv,cf,cw,cu)
collar.modifiers['Fabric_Thickness'].thickness=.0018
# Review uses the same neutral clay and camera configuration for all variants.
scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'
scene.world=bpy.data.worlds.new('Concept_Study_Background'); scene.world.color=(.15,.15,.15)
shade=scene.display.shading; shade.light='STUDIO'; shade.color_type='SINGLE'; shade.single_color=(.65,.65,.65)
shade.show_shadows=True; shade.show_cavity=True; shade.cavity_type='WORLD'; shade.cavity_ridge_factor=.5; shade.cavity_valley_factor=.5
shade.show_specular_highlight=False; shade.background_type='WORLD'; scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
bpy.ops.object.camera_add(); cam=bpy.context.object; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=1.18
target=Vector((.10,0,1.11)); views={'front':(0,-2,1.11),'three_quarter':(1.2,-1.7,1.15),'side':(2,0,1.11),'back':(0,2,1.11),'arm_raised':(0,-2,1.11),'arm_horizontal':(0,-2,1.11)}
def pose(n):
    for name,m in neutral.items(): arm.pose.bones[name].matrix_basis=m.copy()
    if n=='arm_raised': arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(30)
    if n=='arm_horizontal': arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(60)
    bpy.context.view_layer.update()
def camera(n):
    cam.location=views[n]; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
pose('front'); camera('front'); bpy.ops.wm.save_as_mainfile(filepath=str(OUT)); digest=sha(OUT)
renders=[]
for n in views:
    pose(n); camera(n); scene.render.filepath=str(PRE/(n+'_clay.png')); bpy.ops.render.render(write_still=True)
    renders.append({'view':n,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
        'artifact_sha256':digest,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,
        'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler),'pose_type':'ORDINARY_ARMATURE_ONLY'})
pose('front'); camera('front')
assert sha(OUT)==digest and sha(SOURCE)==source_hash and sha(PRIOR)==prior_hash
(REPORT/'render_manifest.json').write_text(json.dumps({'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':digest,'version':'concept-directed-controlled-sheets-v3'},
    'baseline':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':source_hash},'prior_study':{'path':PRIOR.relative_to(ROOT).as_posix(),'sha256':prior_hash},
    'reference':{'path':'outputs/design/concept_option2_kagari.jpg','sha256':sha(ROOT/'outputs/design/concept_option2_kagari.jpg')},
    'renders':renders,'mannequin_neutral_arm_degrees_below_horizontal':60,'cloth_simulation_used':False,'source_unchanged':True,
    'prototype_objects':[cloth.name,collar.name],'human_approval':'NOT_APPROVED','decision':'REQUIRES_HUMAN_ART_REVIEW'},indent=2),encoding='utf-8')
(REPORT/'panel_seams.json').write_text(json.dumps({'panels':panels,'seams':seam_records,'authored_pose_vertices':[list(v) for v in vs],
    'collar_overlap_order':'Positive-X left leaf above negative-X right leaf; side/back inferred from frontal concept.'},indent=2),encoding='utf-8')
print('CONCEPT_STUDY_SAVED',digest,flush=True)
