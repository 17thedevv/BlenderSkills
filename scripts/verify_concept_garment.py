"""Read saved candidate: geometry, weights and actual three-pose evaluation."""
import bpy, bmesh, json, math, hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
ROOT=Path('D:/Project-17/blender'); REPORT=ROOT/'outputs/reports/concept_garment_v3'
candidate=Path(bpy.data.filepath)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
arm=bpy.data.objects['Study_Duplicate_Armature']; body=bpy.data.objects['Study_Duplicate_Mannequin']
garments=[bpy.data.objects[n] for n in ['Concept_Torso_One_Long_Sleeve','Concept_Continuous_Crossed_Collar']]
results=[]
for o in garments:
    bm=bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    deform={g.index for g in o.vertex_groups if g.name in arm.data.bones and arm.data.bones[g.name].use_deform}
    missing=[]; bad=[]; excess=[]
    for v in o.data.vertices:
        weights=[g.weight for g in v.groups if g.group in deform and g.weight>1e-8]
        if not weights: missing.append(v.index)
        if abs(sum(weights)-1)>.001: bad.append(v.index)
        if len(weights)>4: excess.append(v.index)
    components=0; todo=set(v.index for v in bm.verts)
    while todo:
        components+=1; queue=[todo.pop()]
        while queue:
            k=queue.pop()
            for e in bm.verts[k].link_edges:
                n=e.other_vert(bm.verts[k]).index
                if n in todo: todo.remove(n); queue.append(n)
    results.append({'object':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),
        'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
        'surface_components':components,'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),
        'boundary_edges':sum(e.is_boundary for e in bm.edges),'interior_nonmanifold_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
        'missing_weights':missing,'non_normalized_weights':bad,'over_four_influences':excess,
        'modifier_types':[m.type for m in o.modifiers]})
    bm.free()
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}; poses=[]
for label,angle in [('concept_neutral_60_down',0),('moderate_raise_30',30),('horizontal_stress_60',60)]:
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(angle)
    bpy.context.view_layer.update(); dep=bpy.context.evaluated_depsgraph_get()
    bev=body.evaluated_get(dep); bme=bev.to_mesh()
    bvh=BVHTree.FromPolygons([v.co.copy() for v in bme.vertices],[list(p.vertices) for p in bme.polygons]); bev.to_mesh_clear()
    item={'pose':label,'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler),'objects':[]}
    for o in garments:
        ev=o.evaluated_get(dep); me=ev.to_mesh(); finite=all(math.isfinite(x) for v in me.vertices for x in v.co)
        risks=[]
        for v in me.vertices:
            near=bvh.find_nearest(v.co)
            if near and near[0] is not None and near[3]<.025 and v.co.z>.98:
                signed=(v.co-near[0]).dot(near[1])
                if signed<-.002: risks.append({'vertex':v.index,'signed_nearest_distance':signed})
        item['objects'].append({'object':o.name,'finite_coordinates':finite,
            'evaluated_triangles':sum(len(p.vertices)-2 for p in me.polygons),
            'bounds':[[min(v.co[k] for v in me.vertices),max(v.co[k] for v in me.vertices)] for k in range(3)],
            'body_proximity_risk_samples':len(risks),'risk_examples':risks[:10]})
        ev.to_mesh_clear()
    poses.append(item)
for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
technical_errors=[]
for o in results:
    if any(o[x] for x in ['missing_weights','non_normalized_weights','over_four_influences','zero_area_faces','interior_nonmanifold_edges']): technical_errors.append(o['object'])
if not all(x['finite_coordinates'] for p in poses for x in p['objects']): technical_errors.append('non_finite_pose')
report={'candidate':str(candidate),'candidate_sha256':sha(candidate),'objects':results,'poses':poses,
    'source_unchanged':sha(ROOT/'outputs/wip/kagari_v03_clay_03.blend')=='4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051',
    'technical_status':'FAIL' if technical_errors else 'GEOMETRY_WEIGHTS_FINITE_POSES_CHECKED','technical_errors':technical_errors,
    'body_proximity_method':'Nearest-normal signed distance on cropped mannequin, evaluated thickness vertices, only z>.98 and distance<25mm; not a robust intersection test or whole-sleeve certificate.',
    'self_intersections':'NOT_CERTIFIED','vrm_export':'NOT_TESTED','runtime':'NOT_TESTED','art_approval':'NOT_APPROVED'}
(REPORT/'technical_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CONCEPT_TECHNICAL_RESULTS',json.dumps({'errors':technical_errors,'objects':results,'pose_risk_counts':[[x['body_proximity_risk_samples'] for x in p['objects']] for p in poses]}))
if technical_errors: raise RuntimeError('Technical checks failed; inspect report')
