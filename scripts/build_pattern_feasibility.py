"""Fresh metric fabric panels, real loose-edge sewing, pose cloth snapshots.
Run with local Blender 4.2. No failed garment surface is loaded into this scene.
"""
import bpy,bmesh,json,math,time,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix

ROOT=Path(__file__).resolve().parents[1]
TAG=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'trial1'
REPORT=ROOT/'outputs/reports/pattern_feasibility'/TAG
PRE=ROOT/'outputs/previews/pattern_feasibility'/TAG
SOURCE=ROOT/'outputs/wip/kagari_garment_recovery_v2.blend'
SETUP=ROOT/f'outputs/wip/kagari_pattern_{TAG}_source.blend'
OUT=ROOT/f'outputs/wip/kagari_pattern_{TAG}_prototype.blend'
for p in [REPORT,PRE]:p.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
source_sha=sha(SOURCE)
assert source_sha=='9006f5c03019ad0fd4aeeeba1c97b2a30e96f65ac1b8fa0d9093000664017d6d'
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    dst.objects=['Body_GarmentDisplay','Armature']
body,arm=dst.objects
sc=bpy.context.scene
for o in [body,arm]:sc.collection.objects.link(o);o.hide_render=False;o.hide_set(False)
body.name='Pattern_Duplicate_Upper_Mannequin';arm.name='Pattern_Study_Armature'
arm.animation_data_clear()
saved_pose={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
bm=bmesh.new();bm.from_mesh(body.data)
allowed={i for i,m in enumerate(body.data.materials) if m and any(s in m.name for s in ['Body_00_SKIN','Detail_Inner_Ivory','Detail_Clean_Neck'])}
bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index not in allowed or f.calc_center_median().z<.90 or f.calc_center_median().z>1.315],context='FACES_ONLY')
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
bm.to_mesh(body.data);bm.free()
for m in list(body.modifiers):
    if m.type!='ARMATURE':body.modifiers.remove(m)
    else:m.object=arm
body.parent=arm
clay=bpy.data.materials.new('Pattern_Study_Neutral_Clay');clay.diffuse_color=(.62,.62,.62,1)
body.data.materials.clear();body.data.materials.append(clay)
for p in body.data.polygons:p.material_index=0;p.use_smooth=True
body.modifiers.new('Native_Body_Collision','COLLISION')
body.collision.thickness_outer=.0025;body.collision.thickness_inner=.001
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=(0,.02,1.395))
head=bpy.context.object;head.name='Plain_Mannequin_Head';head.scale=(.082,.075,.105);head.data.materials.append(clay)
for p in head.data.polygons:p.use_smooth=True
# Explicit timelines, poses in degrees below horizontal: saved neutral -68,
# +30 = -38, horizontal 0. Lower-arm rotation restored from source gradually.
def pose(upper,fraction=1):
    for b in arm.pose.bones:b.matrix_basis=saved_pose[b.name].copy()
    for side,sign in [('L',1),('R',-1)]:
        for part in ['UpperArm','LowerArm']:
            b=arm.pose.bones['J_Bip_'+side+'_'+part];b.rotation_mode='XYZ'
            if part=='UpperArm':b.rotation_euler=(0,0,math.radians(upper*sign if side=='L' else 68))
            else:b.rotation_euler=tuple(v*fraction for v in b.rotation_euler)
    bpy.context.view_layer.update()
pose(0,0)
# Right arm also moves from horizontal into neutral.
times=[(1,0,0,0),(35,0,0,0),(70,-68,68,1),(110,-68,68,1),(140,-38,68,1),(170,-38,68,1),(205,0,68,1),(235,0,68,1)]
if TAG!='trial1':times=[(1,0,0,0),(60,0,0,0),(140,-68,68,1),(200,-68,68,1),(250,-38,68,1),(300,-38,68,1),(360,0,68,1),(410,0,68,1)]
snap_frames={times[3][0]:'neutral',times[5][0]:'raised30',times[7][0]:'horizontal'}
end_frame=times[-1][0]
for frame,left,right,fraction in times:
    pose(left,fraction);arm.pose.bones['J_Bip_R_UpperArm'].rotation_euler.z=math.radians(right)
    for side in ['L','R']:
        for part in ['UpperArm','LowerArm']:arm.pose.bones['J_Bip_'+side+'_'+part].keyframe_insert(data_path='rotation_euler',frame=frame)
for fc in arm.animation_data.action.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
sc.frame_set(1)

vs=[];faces=[];edges=[];uvs=[];patterns={};seams=[];pins={}
H=22;W=12;S=26
def panel(name,cols,coord,metric):
    grid=[];flat=[];offset=len(patterns)*.52
    for i in range(H+1):
        row=[];flatrow=[]
        for j in range(cols+1):
            t=i/H;u=j/cols;row.append(len(vs));vs.append(coord(t,u))
            uv=metric(t,u);uvs.append((uv[0]+offset,uv[1]));flatrow.append(uv)
        grid.append(row);flat.append(flatrow)
    for i in range(H):
        for j in range(cols):
            a,b,c,d=grid[i][j],grid[i][j+1],grid[i+1][j+1],grid[i+1][j]
            faces.append((a,b,c,d))
    patterns[name]={'grid':grid,'metric_2d_m':flat,'layout_offset':offset}
    return grid
front={}
for side,name in [(-1,'Front_Under'),(1,'Front_Over')]:
    def width(t,u,s=side):return s*((.048-.128*t)*(1-u)+.135*u)
    front[side]=panel(name,W,lambda t,u,s=side:(width(t,u,s),-.049-.093*t+(.006 if s<0 else 0),1.265-.285*t),lambda t,u,s=side:(width(t,u,s),t*math.hypot(.285,.093)))
back=panel('Back_Support',2*W,lambda t,u:(-.135+.270*u,.085,1.265-.285*t),lambda t,u:(.270*u,.285*t)) if TAG=='trial1' else None
# Neck opening in the back pattern: top four rows are cut to a rounded opening.
# Initial flat panel is cut by removing cells, never collapsed into a fan.
if TAG=='trial1':
    cut=set(back[i][j] for i in range(3) for j in range(9,16))
    faces[:]=[f for f in faces if not all(v in cut for v in f)]
else:
    backs={}
    for side,name in [(-1,'Back_Left'),(1,'Back_Right')]:
        def bx(t,u,s=side):return s*(.048*max(0,1-t*5)*(1-u)+.135*u)
        backs[side]=panel(name,W,lambda t,u,s=side:(bx(t,u,s),.080,1.265-.285*t),lambda t,u,s=side:(bx(t,u,s),.285*t))
    # Synthetic ordered back rows for later side/neck references; no extra faces.
    back=[list(reversed(backs[-1][i]))+backs[1][i] for i in range(H+1)]
sleeves={}
for label,y in [('Sleeve_Front',-.054),('Sleeve_Back',.086)]:
    sleeves[label]=panel(label,S,lambda t,u,y=y:(.135+.335*u,y,1.265-.285*t),lambda t,u:(.335*u,.285*t))
def sew(name,a,b):
    assert len(a)==len(b)
    pairs=list(zip(a,b));edges.extend(pairs);seams.append({'name':name,'pairs':pairs})
for side in [-1,1]:
    # Corresponding shoulder arc only: no welded/pinned shoulder bridge.
    top=front[side][0]
    ids=[back[0][min(range(2*W+1),key=lambda j:abs(vs[back[0][j]][0]-vs[k][0]))] for k in top] if TAG=='trial1' else backs[side][0]
    sew('shoulder_'+str(side),top[2:] if TAG=='trial3' else top,ids[2:] if TAG=='trial3' else ids)
    for k in top[:2]:pins[k]=1
if TAG=='trial1':
    for j in [8,16]:pins[back[2][j]]=1
else:
    for side in [-1,1]:
        pins[backs[side][0][0]]=1
        pins[front[side][-1][0]]=1
    sew('center_back_below_neck',[r[0] for r in backs[-1]][5:],[r[0] for r in backs[1]][5:])
F=sleeves['Sleeve_Front'];B=sleeves['Sleeve_Back']
sew('sleeve_top',F[0],B[0]);sew('sleeve_bottom',F[-1],B[-1])
sew('distal_bag_seam',[r[-1] for r in F][9:],[r[-1] for r in B][9:])
sew('armhole_front',[r[-1] for r in front[1]][:10],[r[0] for r in F][:10])
sew('armhole_back',[r[-1] for r in back][:10],[r[0] for r in B][:10])
sew('torso_right_below_vent',[r[-1] for r in front[1]][10:],[r[-1] for r in back][10:])
sew('torso_left_below_open_armhole',[r[-1] for r in front[-1]][9:],[r[0] for r in back][9:])
# Seal proximal bag below attachment but retain the underarm vent.
sew('proximal_bag_seam',[r[0] for r in F][12:],[r[0] for r in B][12:])

def mesh(name,coords,fs,es=()):
    me=bpy.data.meshes.new(name);me.from_pydata(coords,es,fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new(name,me);sc.collection.objects.link(ob);me.materials.append(clay)
    for p in me.polygons:p.use_smooth=True
    return ob
cloth=mesh('Fabric_Panels_With_Sewing',vs,faces,edges)
uv=cloth.data.uv_layers.new(name='Metric_Pattern_UV')
for p in cloth.data.polygons:
    for li in p.loop_indices:uv.data[li].uv=uvs[cloth.data.loops[li].vertex_index]
pg=cloth.vertex_groups.new(name='Neck_Anchors_Only')
for k,w in pins.items():pg.add([k],w,'REPLACE')
if TAG!='trial1':
    # Sparse top/cuff support targets, moved by the study armature. The shoulder
    # surface is NOT fully pinned. These are authoring constraints, not cloth CAD.
    groups={n:cloth.vertex_groups.new(name=n) for n in ['J_Bip_C_UpperChest','J_Bip_L_UpperArm']}
    for i in range(len(vs)):groups['J_Bip_C_UpperChest'].add([i],1,'REPLACE')
    for ids in ([F[0]] if TAG=='trial3' else [F[0],B[0]]):
        for j in [2,S-1]:
            k=ids[j];groups['J_Bip_C_UpperChest'].remove([k]);groups['J_Bip_L_UpperArm'].add([k],1,'REPLACE');pg.add([k],.75,'REPLACE')
    am=cloth.modifiers.new('Animated_Sparse_Support_Targets','ARMATURE');am.object=arm
mod=cloth.modifiers.new('Native_Cloth_Real_Sewing','CLOTH');st=mod.settings
st.quality=6;st.mass=.18;st.tension_stiffness=35;st.compression_stiffness=35;st.shear_stiffness=18;st.bending_stiffness=.12
st.tension_damping=10;st.compression_damping=10;st.shear_damping=8;st.bending_damping=1
st.use_sewing_springs=True;st.sewing_force_max=2;st.vertex_group_mass=pg.name
if TAG!='trial1':st.quality=12;st.sewing_force_max=15;st.bending_stiffness=.35
if TAG=='trial3':st.sewing_force_max=30;st.bending_stiffness=.18
cs=mod.collision_settings;cs.use_collision=True;cs.distance_min=.003;cs.collision_quality=5
cs.use_self_collision=True;cs.self_distance_min=.002;cs.self_friction=5
mod.point_cache.frame_start=1;mod.point_cache.frame_end=end_frame
sc.frame_start=1;sc.frame_end=end_frame;sc.render.fps=24
cloth['construction']='Metric cut panels + loose edge sewing; no old garment data'
cloth['source_character_sha256']=source_sha
pattern_col=bpy.data.collections.new('2D_PATTERNS_SOURCE_ONLY');sc.collection.children.link(pattern_col)
for name,pat in patterns.items():
    coords=[(q[0]+pat['layout_offset'],q[1],0) for row in pat['metric_2d_m'] for q in row]
    rows=len(pat['grid']);cols=len(pat['grid'][0]);ff=[]
    for i in range(rows-1):
        for j in range(cols-1):a=i*cols+j;ff.append((a,a+1,a+1+cols,a+cols))
    o=mesh('2D_'+name,coords,ff);sc.collection.objects.unlink(o);pattern_col.objects.link(o)
pattern_col.hide_render=True;pattern_col.hide_viewport=True
dump(REPORT/'patterns_and_seams.json',{'units':'meters','pieces':patterns,'seams':seams,'pin_vertex_ids':pins,'placed_vertices':vs,'faces':faces,'sewing_loose_edges':edges,'collar':'post-drape metric finishing band, attached to the front cut edges'})
bpy.ops.wm.save_as_mainfile(filepath=str(SETUP))
setup_sha=sha(SETUP)
frames=[];snapshots={};start=time.perf_counter();previous=None
for frame in range(1,end_frame+1):
    sc.frame_set(frame);bpy.context.view_layer.update()
    ev=cloth.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();co=[v.co.copy() for v in me.vertices];ev.to_mesh_clear()
    assert len(co)==len(vs) and all(math.isfinite(x) for p in co for x in p)
    if frame==1 or frame%30==0 or frame in snap_frames:
        gap=[(co[a]-co[b]).length for a,b in edges]
        row={'frame':frame,'elapsed_s':time.perf_counter()-start,'mean_seam_gap_m':sum(gap)/len(gap),'max_seam_gap_m':max(gap),'bounds':[[min(p[k] for p in co),max(p[k] for p in co)] for k in range(3)]}
        if previous:row['rms_change_from_previous_sample_m']=math.sqrt(sum((p-q).length_squared for p,q in zip(co,previous))/len(co))
        frames.append(row);previous=co;print('SEW_FRAME',frame,'elapsed',round(row['elapsed_s'],2),'gap',round(row['max_seam_gap_m'],4),flush=True)
    if frame in snap_frames:snapshots[snap_frames[frame]]=co
dump(REPORT/'simulation.json',{'source_sha256':source_sha,'setup_sha256':setup_sha,'frames':frames,'wall_seconds':time.perf_counter()-start,'topology_changed':False,'solver':'Blender 4.2 sequential Cloth + collision/self collision + sewing springs','cache_warning':'Source scene contains solver setup; rerun script to regenerate cache. Frozen output is independent of transient cache.'})
# Freeze three actual simulated meshes, with exactly the same vertex order.
cloth.modifiers.remove(mod);cloth.hide_render=True;cloth.hide_set(True)
cloth.name='ARCHIVE_Placed_Sewing_Panels';cloth.hide_viewport=True
pattern_col.hide_viewport=True
arm.animation_data_clear();sc.frame_set(1);pose(-68)

def collar_coords(co):
    coords=[];ff=[];cu=[]
    # Broad folded finishing strips share the draped front-panel boundary.
    # Outer leaf on positive X; seam edge is j=3 and open neckline is j=0.
    for side in [-1,1]:
        grid=front[side];start=len(coords)
        for i in range(H+1):
            for j in range(5):
                t=j/4;edge=co[grid[i][0]];inside=co[grid[i][3]]
                p=edge.lerp(inside,t);p.y-=.003+.0015*math.sin(math.pi*t)
                coords.append(p);cu.append((t*.036,i/H*.32))
        for i in range(H):
            for j in range(4):a=start+i*5+j;ff.append((a,a+1,a+6,a+5))
    # Inferred smooth nape extension; two front ends linked by an elliptical
    # strip cut, not an extra bridge plate. Continuous row direction.
    start=len(coords)
    for i in range(25):
        ang=math.pi*i/24;p=Vector((.048*math.cos(ang),.012+.059*math.sin(ang),1.265))
        for j in range(5):
            u=j/4;rad=Vector((math.cos(ang),math.sin(ang),0))
            q=p+rad*(.015*u);q.z-=.029*u
            if TAG=='trial3':
                # Endpoint rows are the front collar's actual seam rows. Blend
                # over the neck quarter-turn to retain a continuous band.
                if i<=6:
                    end=coords[115+j];q=end.lerp(q,min(1,i/6))
                elif i>=18:
                    end=coords[j];q=end.lerp(q,min(1,(24-i)/6))
            coords.append(q);cu.append((u*.030,.35+ang*.052))
    for i in range(24):
        for j in range(4):a=start+i*5+j;ff.append((a,a+1,a+6,a+5))
    return coords,ff,cu

objects={};cols={}
for label,co in snapshots.items():
    ob=mesh('Simulated_'+label,co,faces)
    uv=ob.data.uv_layers.new(name='Metric_Pattern_UV')
    for p in ob.data.polygons:
        for li in p.loop_indices:uv.data[li].uv=uvs[ob.data.loops[li].vertex_index]
    # Welding ONLY defined seam pairs, averaging at finite seam spacing.
    bm=bmesh.new();bm.from_mesh(ob.data);bm.verts.ensure_lookup_table()
    parent=list(range(len(co)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for a,b in edges:parent[find(b)]=find(a)
    groups={}
    for i in range(len(co)):groups.setdefault(find(i),[]).append(i)
    mapping={}
    for group in groups.values():
        if len(group)>1:
            v=bm.verts[group[0]];v.co=sum((co[i] for i in group),Vector())/len(group)
            for i in group[1:]:mapping[bm.verts[i]]=v
    bmesh.ops.weld_verts(bm,targetmap=mapping)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    cc,ff,cu=collar_coords(co);c=mesh('Collar_'+label,cc,ff)
    uv=c.data.uv_layers.new(name='Collar_Metric_UV')
    for p in c.data.polygons:
        for li in p.loop_indices:uv.data[li].uv=cu[c.data.loops[li].vertex_index]
    if TAG=='trial3':
        bm=bmesh.new();bm.from_mesh(c.data);bm.verts.ensure_lookup_table()
        # Two exact endpoint seam welds, not a tolerance merge across overlap.
        bmesh.ops.weld_verts(bm,targetmap={**{bm.verts[230+j]:bm.verts[115+j] for j in range(5)},**{bm.verts[350+j]:bm.verts[j] for j in range(5)}})
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(c.data);bm.free()
    for o in [ob,c]:
        m=o.modifiers.new('Fabric_Thickness_1_6mm','SOLIDIFY');m.thickness=.0016;m.offset=0
        o['prototype_only']=True;o['simulation_snapshot']=label;o['deformation_role']='static simulated snapshot, not skinning'
    objects[label]=ob;cols[label]=c
    for o in [ob,c]:o.hide_render=True;o.hide_set(True)
# Ordinary rig-only clone, with a smooth source-pattern-area binding heuristic.
rig=objects['neutral'].copy();rig.data=objects['neutral'].data.copy();sc.collection.objects.link(rig);rig.name='Rig_Only_Neutral_Drape'
rig.hide_viewport=False;rig.hide_set(False);rig.hide_render=True
weights=[]
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
for v in rig.data.vertices:
    p=v.co;u=smooth((p.x-.095)/.13);lower=smooth((1.10-p.z)/.2)*smooth((p.x-.17)/.12)*.25
    w={'J_Bip_C_UpperChest':1-u,'J_Bip_L_UpperArm':u*(1-lower),'J_Bip_L_LowerArm':u*lower}
    if p.x<.09:w={'J_Bip_C_UpperChest':1}
    weights.append(w)
gn={n:rig.vertex_groups.new(name=n) for n in {n for w in weights for n in w}}
mat={b.name:b.matrix@arm.data.bones[b.name].matrix_local.inverted() for b in arm.pose.bones}
for v,w in zip(rig.data.vertices,weights):
    m=Matrix(((0,0,0,0),)*4)
    for n,x in w.items():
        if x:gn[n].add([v.index],x,'REPLACE');m+=mat[n]*x
    v.co=m.inverted()@v.co
am=rig.modifiers.new('Ordinary_Armature_Diagnostic','ARMATURE');am.object=arm
rig.modifiers.move(len(rig.modifiers)-1,0);rig['deformation_role']='cloth';rig['binding_status']='heuristic preview, not production weights'
# Production diagnostic has no corrective keys or extra bones.
for o in [objects['neutral'],cols['neutral']]:o.hide_render=False;o.hide_set(False)
sc['study_version']=f'pattern-sewing-feasibility-{TAG}';sc['source_character_sha256']=source_sha;sc['artistic_approval']='NOT_APPROVED'
sc.world=bpy.data.worlds.new('Study_World');sc.world.color=(.15,.15,.15)
camdata=bpy.data.cameras.new('Matched_Recovery_Camera');cam=bpy.data.objects.new('Matched_Recovery_Camera',camdata);sc.collection.objects.link(cam);sc.camera=cam
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=sc.render.resolution_y=1000;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
sh=sc.display.shading;sh.light='STUDIO';sh.color_type='SINGLE';sh.single_color=(.62,.62,.62);sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='WORLD';sh.cavity_ridge_factor=sh.cavity_valley_factor=.5;sh.show_specular_highlight=False;sh.background_type='WORLD'
manifest=json.loads((ROOT/'outputs/reports/garment_recovery_v2/render_manifest.json').read_text())
rows={r['view']:r for r in manifest['renders']}
def camera(row):camdata.type='ORTHO';cam.location=row['camera_location'];cam.rotation_euler=row['camera_rotation'];camdata.ortho_scale=row['ortho_scale']
camera(rows['front'])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));outsha=sha(OUT)
records=[]
def show(label,mode):
    for o in list(objects.values())+list(cols.values())+[rig]:o.hide_render=True;o.hide_set(True)
    ob=rig if mode=='rig_only' else objects[label]
    for o in [ob,cols[label if mode=='simulation' else 'neutral']]:o.hide_render=False;o.hide_set(False)
    pose({'neutral':-68,'raised30':-38,'horizontal':0}[label])
for label in ['neutral','raised30','horizontal']:
    for view in ['front','three_quarter','side','back']:
        show(label,'simulation');row=rows[view].copy()
        if label!='neutral':row['ortho_scale']=rows['arm_horizontal' if label=='horizontal' else 'arm_raised']['ortho_scale']
        camera(row);img=PRE/f'{label}_{view}_clay.png';sc.render.filepath=str(img);bpy.ops.render.render(write_still=True)
        records.append({'path':img.relative_to(ROOT).as_posix(),'sha256':sha(img),'view':view,'pose':label,'deformation':'ACTUAL_SEQUENTIAL_CLOTH_SNAPSHOT','camera':{k:row[k] for k in ['camera_location','camera_rotation','ortho_scale']},'upper_arm_pose':{s:list(arm.pose.bones['J_Bip_'+s+'_UpperArm'].rotation_euler) for s in ['L','R']},'artifact_sha256':outsha})
for label in ['raised30','horizontal']:
    show(label,'rig_only');row=rows['arm_horizontal' if label=='horizontal' else 'arm_raised'];camera(row)
    img=PRE/f'rig_only_{label}_front_clay.png';sc.render.filepath=str(img);bpy.ops.render.render(write_still=True)
    records.append({'path':img.relative_to(ROOT).as_posix(),'sha256':sha(img),'view':'front','pose':label,'deformation':'ORDINARY_ARMATURE_NO_CLOTH_NO_CORRECTIVES','camera':{k:row[k] for k in ['camera_location','camera_rotation','ortho_scale']},'upper_arm_pose':{s:list(arm.pose.bones['J_Bip_'+s+'_UpperArm'].rotation_euler) for s in ['L','R']},'artifact_sha256':outsha})
assert sha(SOURCE)==source_sha and sha(OUT)==outsha
dump(REPORT/'render_manifest.json',{'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':outsha,'version':sc['study_version']},'source_setup':{'path':SETUP.relative_to(ROOT).as_posix(),'sha256':setup_sha},'source_character':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':source_sha},'renders':records,'source_preserved':True,'neutral_arm_degrees_below_horizontal':68,'raise_relative_degrees':30,'horizontal_bone_z_degrees':0,'comparison_lighting':'Exact Recovery v2 Workbench clay settings; neutral camera transforms unchanged; stress scales reused across all four views.'})
print('PATTERN_STUDY_COMPLETE',str(OUT),flush=True)
