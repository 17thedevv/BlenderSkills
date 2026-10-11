"""Second/final controlled repair: local contact constraints across existing arm poses."""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils import Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from garment_recovery_common import *
SOURCE1=ROOT/'outputs/wip/kagari_garment_recovery_v1.blend'
SOURCE1_SHA='61df33536b9b8caebe9d2bccaa2d7599bb917f10476bb6c67fcc0dab318f61e4'
assert sha(SOURCE)==SOURCE_SHA and sha(SOURCE1)==SOURCE1_SHA
bpy.ops.wm.open_mainfile(filepath=str(SOURCE1));bpy.context.view_layer.update()
R=ROOT/'outputs/reports/garment_recovery_v2';P=ROOT/'outputs/previews/garment_recovery_v2'
R.mkdir(parents=True,exist_ok=True);P.mkdir(parents=True,exist_ok=True)
before=snapshot();protect=untouched();arm=bpy.data.objects['Armature']
robe=bpy.data.objects['Kagari_Concept_Robe_Two_Sleeves'];collar=bpy.data.objects['Kagari_Concept_Crossed_Collar'];body=bpy.data.objects['Body_GarmentDisplay']
orig={o.name:[v.co.copy() for v in o.data.vertices] for o in [robe,collar]}
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
def pose(mode):
    for name,matrix in neutral.items():arm.pose.bones[name].matrix_basis=matrix.copy()
    if mode=='raise':
        for side,delta in [('L',30),('R',-30)]:arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z+=math.radians(delta)
    if mode=='horizontal':
        for side in ['L','R']:arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z=0
    bpy.context.view_layer.update()
def evaluated_bvh(ob):
    dep=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(dep);me=ev.to_mesh();me.calc_loop_triangles()
    verts=[ev.matrix_world@v.co for v in me.vertices];tri=[tuple(t.vertices) for t in me.loop_triangles]
    bvh=BVHTree.FromPolygons(verts,tri,all_triangles=True);ev.to_mesh_clear();return bvh
pose_bvhs={};mats={};invs={}
for mode in ['neutral','raise','horizontal']:
    pose(mode);pose_bvhs[mode]=evaluated_bvh(body)
    mats[mode]=[weighted_matrix(robe,v,arm) for v in robe.data.vertices]
    invs[mode]=[m.inverted() for m in mats[mode]]
pose('neutral')
# All solves stay inside this single geometry configuration. No added corrective/rig data.
passes=[]
for cycle in range(8):
    moved=0;largest=0
    for mode in ['horizontal','raise','neutral']:
        bvh=pose_bvhs[mode]
        for i,v in enumerate(robe.data.vertices):
            p=mats[mode][i]@v.co
            if not .90<p.z<1.292:continue
            q,n,face,d=bvh.find_nearest(p)
            if q is None or d>.026:continue
            signed=(p-q).dot(n);gap=.0045
            if signed<gap:
                change=min(.012,gap-signed)
                v.co=invs[mode][i]@(p+n*change);moved+=1;largest=max(largest,change)
    robe.data.update();passes.append({'constraint_sweep':cycle+1,'vertex_projections':moved,'largest_projection':largest})
    if not moved:break
pose('neutral');bpy.context.view_layer.update()
# Separate nape/leaf transition from actual solidified robe support without widening collar.
collar_passes=[]
for sweep in range(4):
    bvh=evaluated_bvh(robe);coords=posed_coords(collar);moved=0
    for i,p in enumerate(coords):
        if p.z<1.232:continue
        q,n,face,d=bvh.find_nearest(p)
        if q is not None and d<.013:
            signed=(p-q).dot(n);gap=.003
            if signed<gap:coords[i]=p+n*min(.009,gap-signed);moved+=1
    set_posed(collar,coords);collar_passes.append({'sweep':sweep+1,'vertex_projections':moved})
    if not moved:break
for o in [robe,collar]:
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
pose('neutral');assert before==snapshot() and protect==untouched()
configure_clay();camera(next(row for row in FULL_MANIFEST['renders'] if row['view']=='three_quarter'))
out=ROOT/'outputs/wip/kagari_garment_recovery_v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out))
candidate={'path':out.relative_to(ROOT).as_posix(),'sha256':sha(out),'version':'garment-geometry-recovery-v2'}
dump(R/'protected_invariants.json',{'before':before,'after':snapshot(),'untouched_meshes_before':protect,'untouched_meshes_after':untouched(),'identical':True,'candidate':candidate})
dump(R/'edit_log.json',{'candidate':candidate,'source':FULL_MANIFEST['candidate'],'input_iteration':{'path':SOURCE1.relative_to(ROOT).as_posix(),'sha256':SOURCE1_SHA},
 'iteration':2,'iteration_limit':2,'no_further_repair_iterations':True,'editable_objects':sorted(EDITABLE),
 'constraint_sweeps':passes,'collar_support_sweeps':collar_passes,'garment_weights_unchanged':True,'topology_unchanged':True,'new_materials':False,
 'rest_vertex_displacement_max_from_iteration1':{o.name:max((v.co-p).length for v,p in zip(o.data.vertices,orig[o.name])) for o in [robe,collar]},
 'method_limits':'Local geometric clearance constraints on fixed skinning; no physical cloth drape or all-pose guarantee.'})
render_evidence(candidate,R,P)
assert sha(SOURCE1)==SOURCE1_SHA
print('GARMENT_RECOVERY_V2_SAVED',candidate['sha256'],flush=True)
