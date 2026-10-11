"""Technical verification of frozen panel geometry and pose, not artistic PASS."""
import bpy, bmesh, math, json, hashlib
from pathlib import Path
ROOT=Path('D:/Project-17/blender'); REPORT=ROOT/'outputs/reports/garment_reset_final'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
candidate=Path(bpy.data.filepath); arm=bpy.data.objects['Study_Duplicate_Armature']
garments=[bpy.data.objects[n] for n in ['Panel_Torso_One_Sleeve','Sewn_Overlapping_Collar']]
results=[]
for o in garments:
    bm=bmesh.new(); bm.from_mesh(o.data)
    deform={g.index for g in o.vertex_groups if g.name in arm.data.bones and arm.data.bones[g.name].use_deform}
    missing=[]; bad=[]; excess=[]
    for v in o.data.vertices:
        w=[g.weight for g in v.groups if g.group in deform and g.weight>1e-8]
        if not w: missing.append(v.index)
        if abs(sum(w)-1)>.001: bad.append(v.index)
        if len(w)>4: excess.append(v.index)
    components=0; todo=set(v.index for v in bm.verts)
    bm.verts.ensure_lookup_table()
    while todo:
        components+=1; queue=[todo.pop()]
        while queue:
            k=queue.pop()
            for e in bm.verts[k].link_edges:
                n=e.other_vert(bm.verts[k]).index
                if n in todo: todo.remove(n); queue.append(n)
    results.append({'object':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),
      'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
      'boundary_edges':sum(e.is_boundary for e in bm.edges),'interior_nonmanifold_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
      'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'surface_components':components,
      'missing_deform_weights':missing,'non_normalized_weight_vertices':bad,'over_four_influences':excess,
      'cloth_solver_on_delivery_mesh':any(m.type=='CLOTH' for m in o.modifiers),
      'subdivision_modifiers':sum(m.type=='SUBSURF' for m in o.modifiers),
      'shape_keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else []})
    bm.free()
    assert not missing and not bad and not excess,'Binding failure'
    assert not any(m.type in ['CLOTH','SUBSURF'] for m in o.modifiers),'Unfrozen/dense modifier'
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
poses=[]
for label,angle in [('construction_A_pose',0),('left_raise_30_degrees',30)]:
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(angle)
    bpy.context.view_layer.update(); data={}
    for o in garments:
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
        assert all(math.isfinite(x) for v in me.vertices for x in v.co),'Non-finite pose'
        data[o.name]={'evaluated_triangles':sum(len(p.vertices)-2 for p in me.polygons),
                     'bounds':[[min(v.co[k] for v in me.vertices),max(v.co[k] for v in me.vertices)] for k in range(3)]}
        ev.to_mesh_clear()
    poses.append({'pose':label,'upper_arm_rotation':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler),'objects':data})
for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
result={'candidate':str(candidate),'candidate_sha256':sha(candidate),'source_sha256':sha(ROOT/'outputs/wip/kagari_v03_clay_03.blend'),
        'source_unchanged':sha(ROOT/'outputs/wip/kagari_v03_clay_03.blend')=='4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051',
        'objects':results,'poses':poses,'technical_status':'CHECKED_WEIGHTS_FINITE_POSES',
        'visual_status':'REQUIRES_SEPARATE_IMAGE_REVIEW','vrm_export':'NOT_TESTED','warudo':'NOT_TESTED'}
(REPORT/'technical_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('PANEL_TECHNICAL_CHECKS',[(o['object'],o['surface_components'],o['zero_area_faces']) for o in results])
