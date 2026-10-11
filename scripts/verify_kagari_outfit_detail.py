import bpy
import json
from pathlib import Path

ROOT=Path('D:/Project-17/blender')
def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    result={}
    for name in ['Face','Hair']:
        ob=bpy.data.objects[name]
        result[name]={
            'vertices':[tuple(v.co) for v in ob.data.vertices],
            'polygons':[(tuple(p.vertices),p.material_index) for p in ob.data.polygons],
            'keys':{k.name:[tuple(v.co) for v in k.data] for k in ob.data.shape_keys.key_blocks} if ob.data.shape_keys else {},
        }
    arm=bpy.data.objects['Armature']
    result['bones']=[(b.name,b.parent.name if b.parent else None,tuple(b.head_local),tuple(b.tail_local)) for b in arm.data.bones]
    return result

source=snapshot(ROOT/'outputs/wip/kagari_vroid_master.blend')
target=snapshot(ROOT/'outputs/wip/kagari_outfit_detail_v1.blend')
report={
    'face_mesh_and_all_shape_keys_unchanged':source['Face']==target['Face'],
    'hair_mesh_unchanged':source['Hair']==target['Hair'],
    'original_bone_hierarchy_and_rest_positions_unchanged':source['bones']==target['bones'],
    'new_accessories_attached_to_existing_bones':True,
    'unpacked_images':[],
    'added_geometry_triangles_evaluated':0,
    'all_geometry_triangles_evaluated':0,
    'human_visual_approval':'PENDING',
    'cloth_deformation_and_vrm_export':'NOT_TESTED',
}
deps=bpy.context.evaluated_depsgraph_get()
for ob in bpy.data.objects:
    if ob.type!='MESH':
        continue
    ev=ob.evaluated_get(deps)
    me=ev.to_mesh()
    me.calc_loop_triangles()
    report['all_geometry_triangles_evaluated']+=len(me.loop_triangles)
    if ob.get('detail_pass'):
        report['added_geometry_triangles_evaluated']+=len(me.loop_triangles)
        if not any(m.type=='ARMATURE' and m.object for m in ob.modifiers):
            report['new_accessories_attached_to_existing_bones']=False
    ev.to_mesh_clear()
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        report['unpacked_images'].append(im.name)
report['preview_files']={p.name:p.stat().st_size for p in (ROOT/'outputs/previews/outfit_detail_v1').glob('*.png')}
(ROOT/'outputs/reports/kagari_outfit_detail_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert report['face_mesh_and_all_shape_keys_unchanged']
assert report['hair_mesh_unchanged']
assert report['original_bone_hierarchy_and_rest_positions_unchanged']
assert report['new_accessories_attached_to_existing_bones']
