"""Reloaded full-avatar verification: protected data and new garment geometry."""
import bpy,bmesh,json,math,hashlib,sys
from pathlib import Path
ROOT=Path('D:/Project-17/blender'); sys.path.insert(0,str(ROOT/'scripts'))
from kagari_invariants import snapshot
REPORT=ROOT/'outputs/reports/full_concept_v3'; manifest=json.loads((REPORT/'render_manifest.json').read_text())
prior=json.loads((REPORT/'protected_invariants.json').read_text())
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
saved=snapshot(); invariant_matches={n:saved[n]==prior['before'][n] for n in saved}; assert all(invariant_matches.values())
arm=bpy.data.objects['Armature']; garments=[bpy.data.objects[n] for n in manifest['new_objects']]
errors=[]; objects=[]
for o in garments:
    bm=bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    deform={g.index for g in o.vertex_groups if g.name in arm.data.bones and arm.data.bones[g.name].use_deform}
    missing=[]; bad=[]; too_many=[]
    for v in o.data.vertices:
        vals=[g.weight for g in v.groups if g.group in deform and g.weight>1e-8]
        if not vals: missing.append(v.index)
        if abs(sum(vals)-1)>.001: bad.append(v.index)
        if len(vals)>4: too_many.append(v.index)
    todo=set(v.index for v in bm.verts); components=0
    while todo:
        components+=1; queue=[todo.pop()]
        while queue:
            k=queue.pop()
            for e in bm.verts[k].link_edges:
                n=e.other_vert(bm.verts[k]).index
                if n in todo: todo.remove(n); queue.append(n)
    item={'object':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
        'surface_components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),
        'interior_nonmanifold_edges':sum(not e.is_boundary and not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),
        'missing_weights':missing,'non_normalized_weights':bad,'over_four_influences':too_many,
        'armature_references':[m.object.name if m.object else None for m in o.modifiers if m.type=='ARMATURE'],
        'uvs':[uv.name for uv in o.data.uv_layers],'materials':[m.name for m in o.data.materials],'modifiers':[m.type for m in o.modifiers]}
    bm.free()
    if any(item[k] for k in ['interior_nonmanifold_edges','zero_area_faces','missing_weights','non_normalized_weights','over_four_influences']) or components!=1: errors.append(o.name)
    objects.append(item)
neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}; poses=[]
for label,mode in [('saved_original_neutral','neutral'),('both_arms_raise_30','raise'),('both_arms_horizontal','horizontal')]:
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    if mode=='raise':
        for side,delta in [('L',30),('R',-30)]: arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z+=math.radians(delta)
    if mode=='horizontal':
        for side in ['L','R']: arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z=0
    bpy.context.view_layer.update(); dep=bpy.context.evaluated_depsgraph_get(); item={'pose':label,'objects':[]}
    for o in garments:
        ev=o.evaluated_get(dep); me=ev.to_mesh(); finite=all(math.isfinite(x) for v in me.vertices for x in v.co)
        item['objects'].append({'object':o.name,'evaluated_triangles':sum(len(p.vertices)-2 for p in me.polygons),'finite':finite,
            'bounds':[[min(v.co[k] for v in me.vertices),max(v.co[k] for v in me.vertices)] for k in range(3)]})
        if not finite: errors.append(o.name+' '+label+' nonfinite')
        ev.to_mesh_clear()
    poses.append(item)
for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
bpy.context.view_layer.update(); assert snapshot()==saved
path=Path(bpy.data.filepath); digest=sha(path); assert digest==manifest['candidate']['sha256']
assert sha(ROOT/manifest['baseline']['path'])==manifest['baseline']['sha256']
display=bpy.data.objects['Body_GarmentDisplay']
payload={'candidate':manifest['candidate'],'technical_status':'FAIL' if errors else 'PROTECTED_DATA_AND_GARMENT_CHECKS_VERIFIED',
    'protected_data_matches_after_reload':invariant_matches,'errors':errors,'objects':objects,'poses':poses,
    'body_display_copy':{'vertices':len(display.data.vertices),'faces':len(display.data.polygons),'source_body_preserved':True,'original_body_has_shape_keys':bool(bpy.data.objects['Body'].data.shape_keys)},
    'archive_excluded_from_render':bpy.data.collections['ARCHIVE_Rejected_Garments_Do_Not_Export'].hide_render,
    'active_scene_armatures':[o.name for o in bpy.context.scene.objects if o.type=='ARMATURE'],
    'intersection_free':'NOT_CERTIFIED','lower_body_walk_pose':'NOT_TESTED','vrm_export':'NOT_TESTED','warudo':'NOT_TESTED','human_art_approval':'NOT_APPROVED'}
(REPORT/'technical_verification.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('FULL_KAGARI_TECHNICAL_CHECKS',json.dumps({'errors':errors,'protected':invariant_matches,'objects':objects}))
if errors: raise RuntimeError('Full garment checks failed; read report')
