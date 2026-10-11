"""Reload invariants, skinning and bounded evaluated-surface intersection probes."""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from garment_recovery_common import *
candidate_path=Path(bpy.data.filepath);iteration=candidate_path.stem.rsplit('_',1)[-1]
R=ROOT/('outputs/reports/garment_recovery_'+iteration)
manifest=json.loads((R/'render_manifest.json').read_text());inv=json.loads((R/'protected_invariants.json').read_text())
candidate=manifest['candidate'];assert sha(candidate_path)==candidate['sha256'] and sha(SOURCE)==SOURCE_SHA
protected=snapshot();matches={n:protected[n]==inv['before'][n] for n in protected}
unt=untouched();unt_matches=unt==inv['untouched_meshes_before']
errors=[]
if not all(matches.values()):errors.append('Protected original data mismatch')
if not unt_matches:errors.append('Untouched mesh data mismatch')
arm=bpy.data.objects['Armature'];objects=[]
for name in manifest['new_objects']:
    o=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table()
    deform={g.index for g in o.vertex_groups if g.name in arm.data.bones and arm.data.bones[g.name].use_deform}
    missing=[];bad=[];too_many=[]
    for v in o.data.vertices:
        weights=[g.weight for g in v.groups if g.group in deform and g.weight>1e-8]
        if not weights:missing.append(v.index)
        if abs(sum(weights)-1)>.001:bad.append(v.index)
        if len(weights)>4:too_many.append(v.index)
    todo=set(range(len(bm.verts)));components=0
    while todo:
        components+=1;queue=[todo.pop()]
        while queue:
            k=queue.pop()
            for e in bm.verts[k].link_edges:
                other=e.other_vert(bm.verts[k]).index
                if other in todo:todo.remove(other);queue.append(other)
    item={'object':name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),
      'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'surface_components':components,
      'boundary_edges':sum(e.is_boundary for e in bm.edges),'interior_nonmanifold_edges':sum(not e.is_boundary and not e.is_manifold for e in bm.edges),
      'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'missing_weights':missing,'non_normalized_weights':bad,'over_four_influences':too_many,
      'armature_references':[m.object.name if m.object else None for m in o.modifiers if m.type=='ARMATURE'],
      'uvs':[u.name for u in o.data.uv_layers],'materials':[m.name for m in o.data.materials]}
    if components!=1 or any(item[k] for k in ['interior_nonmanifold_edges','zero_area_faces','missing_weights','non_normalized_weights','over_four_influences']):errors.append(name+' mesh/skin integrity')
    if item['armature_references']!=['Armature']:errors.append(name+' armature reference')
    objects.append(item);bm.free()

def evaluated(o,dep):
    ev=o.evaluated_get(dep);me=ev.to_mesh();me.calc_loop_triangles()
    verts=[ev.matrix_world@v.co for v in me.vertices]
    tri=[tuple(t.vertices) for t in me.loop_triangles]
    edges=[(e.vertices[0],e.vertices[1]) for e in me.edges]
    payload={'verts':verts,'triangles':tri,'edges':edges,'bvh':BVHTree.FromPolygons(verts,tri,all_triangles=True)}
    ev.to_mesh_clear();return payload
def probes(a,b,zlo,zhi):
    tested=0;hits=0;samples=[];eps=2e-6
    for i,j in a['edges']:
        p,q=a['verts'][i],a['verts'][j]
        if max(p.z,q.z)<zlo or min(p.z,q.z)>zhi:continue
        vec=q-p;length=vec.length
        if length<eps*2:continue
        direction=vec/length;tested+=1
        hit=b['bvh'].ray_cast(p+direction*eps,direction,length-2*eps)
        if hit[0] is not None and zlo<=hit[0].z<=zhi:
            hits+=1
            if len(samples)<12:samples.append({'edge':[i,j],'point':list(hit[0]),'target_triangle':hit[2]})
    return {'tested_edge_segments':tested,'crossing_edge_segments':hits,'samples':samples}
pairs=[('Kagari_Concept_Robe_Two_Sleeves','Kagari_Concept_Soft_Waist_Sash',.897,.996),
       ('Kagari_Concept_Lower_Robe','Kagari_Concept_Soft_Waist_Sash',.897,.996),
       ('Kagari_Concept_Crossed_Collar','Kagari_Concept_Robe_Two_Sleeves',1.235,1.290),
       ('Kagari_Concept_Crossed_Collar','Body_GarmentDisplay',1.235,1.290),
       ('Kagari_Concept_Robe_Two_Sleeves','Body_GarmentDisplay',1.075,1.29)]
checks=[]
for label,path in [('full_v3_source',SOURCE),('recovery_candidate',candidate_path)]:
    bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.view_layer.update();arm=bpy.data.objects['Armature']
    saved=snapshot();neutral={p.name:p.matrix_basis.copy() for p in arm.pose.bones};record={'artifact':label,'sha256':sha(path),'poses':[]}
    for pose,mode in [('saved_neutral','neutral'),('raised_30','raise'),('upper_arms_horizontal','horizontal')]:
        for name,matrix in neutral.items():arm.pose.bones[name].matrix_basis=matrix.copy()
        if mode=='raise':
            for side,delta in [('L',30),('R',-30)]:arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z+=math.radians(delta)
        if mode=='horizontal':
            for side in ['L','R']:arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z=0
        bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
        meshes={n:evaluated(bpy.data.objects[n],dep) for n in {name for pair in pairs for name in pair[:2]}}
        item={'pose':pose,'finite_coordinates':all(math.isfinite(k) for data in meshes.values() for v in data['verts'] for k in v),
         'evaluated_triangles':{n:len(d['triangles']) for n,d in meshes.items()},'intersection_probes':[]}
        if not item['finite_coordinates']:errors.append(label+' '+pose+' nonfinite coordinates')
        for an,bn,zlo,zhi in pairs:
            ab=probes(meshes[an],meshes[bn],zlo,zhi);ba=probes(meshes[bn],meshes[an],zlo,zhi)
            item['intersection_probes'].append({'objects':[an,bn],'z_range':[zlo,zhi],'a_edges_against_b':ab,'b_edges_against_a':ba,
              'total_crossing_edge_segments':ab['crossing_edge_segments']+ba['crossing_edge_segments']})
        record['poses'].append(item)
        print('PROBED',label,pose,[r['total_crossing_edge_segments'] for r in item['intersection_probes']],flush=True)
    for name,matrix in neutral.items():arm.pose.bones[name].matrix_basis=matrix.copy()
    bpy.context.view_layer.update();assert snapshot()==saved
    checks.append(record)
assert protected==snapshot() and unt==untouched()
assert sha(candidate_path)==candidate['sha256'] and sha(SOURCE)==SOURCE_SHA
payload={'candidate':candidate,'comparison_source':manifest['comparison_source'],'errors':errors,
 'technical_status':'FAIL' if errors else 'PROTECTED_DATA_TOPOLOGY_SKINNING_VERIFIED',
 'protected_data_matches_after_reload':matches,'all_untouched_mesh_data_matches':unt_matches,
 'objects':objects,'surface_probes':checks,
 'probe_method':'Bidirectional evaluated mesh edge segments ray-cast against triangulated evaluated surfaces, including Solidify; restricted height ranges and three static arm poses. Positive results identify crossing segments; zero results do not certify all geometry or motion.',
 'intersection_free':'NOT_CERTIFIED','self_intersections':'NOT_EXHAUSTIVELY_TESTED','lower_body_motion':'NOT_TESTED','vrm_export':'NOT_TESTED','tracking':'NOT_TESTED','animation_readiness':'NOT_TESTED','human_approval':'NOT_APPROVED'}
dump(R/'technical_verification.json',payload)
print('GARMENT_RECOVERY_TECHNICAL_VERIFIED',json.dumps({'errors':errors,'protected':matches,'untouched':unt_matches}),flush=True)
if errors:raise RuntimeError('Recovery technical checks failed')
