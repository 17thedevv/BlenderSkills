"""Complete nape seam of the new panel collar, preserving frozen drape."""
import bpy, bmesh, math, json, hashlib, argparse, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Project-17/blender')
parser=argparse.ArgumentParser()
parser.add_argument('--drape-report',default='outputs/reports/garment_reset_v02')
parser.add_argument('--out',default='outputs/wip/kagari_panel_drape_02_sewn.blend')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
REPORT=ROOT/'outputs/reports/garment_reset_final'
PRE=ROOT/'outputs/previews/garment_reset_final'
for p in [REPORT,PRE]: p.mkdir(parents=True,exist_ok=True)
INPUT=Path(bpy.data.filepath); OUT=ROOT/args.out
drape=json.loads((ROOT/args.drape_report/'drape_execution.json').read_text())
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
ob=bpy.data.objects['Sewn_Overlapping_Collar']; arm=bpy.data.objects['Study_Duplicate_Armature']
old=ob.data
# Retain the two actual panel-contact collar leaves (25 rows, five columns each).
coords=[v.co.copy() for v in old.vertices[:250]]
weights=[]
for v in old.vertices[:250]:
    weights.append({ob.vertex_groups[g.group].name:g.weight for g in v.groups})
faces=[tuple(p.vertices) for p in old.polygons if all(k<250 for k in p.vertices)]
left=[125+k for k in range(5)]; right=list(range(5))
ctrl=[coords[left[0]],Vector((.050,.022,1.264)),Vector((.037,.072,1.266)),Vector((0,.086,1.263)),Vector((-.037,.072,1.266)),Vector((-.050,.022,1.264)),coords[right[0]]]
def catmull(t):
    p=t*(len(ctrl)-1); i=min(len(ctrl)-2,int(p)); u=p-i
    a=ctrl[max(0,i-1)]; b=ctrl[i]; c=ctrl[i+1]; d=ctrl[min(len(ctrl)-1,i+2)]
    return .5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
startvec=coords[left[-1]]-coords[left[0]]; endvec=coords[right[-1]]-coords[right[0]]
rows=[left]
def smooth(t): t=max(0,min(1,t)); return t*t*(3-2*t)
for i in range(1,48):
    t=i/48; p=catmull(t)
    radial=Vector((p.x,p.y-.022,0)).normalized()
    vec=Vector((0,0,-.027))+radial*.007
    if t<.22: vec=startvec.lerp(vec,smooth(t/.22))
    elif t>.78: vec=vec.lerp(endvec,smooth((t-.78)/.22))
    row=[]
    for j in range(5):
        u=j/4; q=p+vec*u+radial*.001*math.sin(math.pi*u)
        row.append(len(coords)); coords.append(q); weights.append({'J_Bip_C_UpperChest':1})
    rows.append(row)
rows.append(right)
for a,b in zip(rows,rows[1:]):
    for j in range(4): faces.append((a[j],a[j+1],b[j+1],b[j]))
me=bpy.data.meshes.new('Continuous_Sewn_Collar_Surface'); me.from_pydata(coords,[],faces); me.update()
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
for m in old.materials: me.materials.append(m)
ob.data=me
for group in list(ob.vertex_groups): ob.vertex_groups.remove(group)
groups={n:ob.vertex_groups.new(name=n) for n in {n for w in weights for n in w}}
for i,w in enumerate(weights):
    total=sum(w.values())
    for n,v in w.items(): groups[n].add([i],v/total,'REPLACE')
for p in me.polygons: p.use_smooth=True
ob['seam_status']='Nape bridge shares vertex indices with both front lapel leaves; one connected collar surface.'
scene=bpy.context.scene; cam=scene.camera; target=Vector((.07,0,1.16))
cam.data.ortho_scale=1.0  # include the complete wide sleeve in the raised pose
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
views={'front':(0,-2,1.16),'three_quarter':(1.20,-1.7,1.20),'side':(2,0,1.16),'back':(0,2,1.16),'arm_raised':(0,-2,1.16)}
def pose(raised=False):
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    if raised: arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(30)
    bpy.context.view_layer.update()
def camera(n):
    cam.location=views[n]; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
pose(); camera('front'); bpy.ops.wm.save_as_mainfile(filepath=str(OUT)); digest=sha(OUT)
renders=[]
for n in views:
    pose(n=='arm_raised'); camera(n)
    scene.render.filepath=str(PRE/('prototype_'+n+'_clay.png')); bpy.ops.render.render(write_still=True)
    renders.append({'view':n,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
      'artifact_sha256':digest,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,
      'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler),'pose_type':'ORDINARY_ARMATURE_SKINNING_ONLY'})
pose(); camera('front')
assert sha(OUT)==digest
source=ROOT/'outputs/wip/kagari_v03_clay_03.blend'; expected='4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051'
assert sha(source)==expected
manifest={'candidate':{'path':OUT.relative_to(ROOT).as_posix(),'sha256':digest,'version':'garment-reset-panel-drape-study'},
 'baseline':{'path':source.relative_to(ROOT).as_posix(),'sha256':expected},'renders':renders,
 'input_drape':{'path':INPUT.relative_to(ROOT).as_posix(),'sha256':sha(INPUT)},
 'raw_setup':drape['raw_panel_setup'], 'drape_execution_report':args.drape_report+'/drape_execution.json',
 'source_unchanged':True,'original_character_geometry_modified':False,'decision':'REQUIRES_HUMAN_ART_REVIEW',
 'mannequin_pose':'Both arms 30 degrees down from rest; left tested raised to horizontal (+30 degrees).',
 'prototype_objects':['Panel_Torso_One_Sleeve','Sewn_Overlapping_Collar'],
 'method':f"New sheet panels, explicit welded seams, {drape['simulation_steps']}-frame native cloth snapshot frozen before skinning test; no rejected garment reused.",
 'drape_equilibrium_verified':False}
(REPORT/'render_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('FINAL_SEWN_PANEL_PROTOTYPE',digest)
