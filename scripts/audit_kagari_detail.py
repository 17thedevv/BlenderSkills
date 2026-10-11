import bpy
import json
from pathlib import Path
from mathutils import Vector

root = Path('D:/Project-17/blender')
bpy.ops.wm.open_mainfile(filepath=str(root / 'outputs/wip/kagari_vroid_master.blend'))
result = {'objects': [], 'bones': []}
for obj in bpy.data.objects:
    item = {'name': obj.name, 'type': obj.type, 'location': list(obj.location)}
    if obj.type == 'MESH':
        item['bounds'] = [list(obj.matrix_world @ Vector(p)) for p in obj.bound_box]
        item['materials'] = [m.name if m else None for m in obj.data.materials]
        item['vertices'] = len(obj.data.vertices)
        item['shape_keys'] = list(obj.data.shape_keys.key_blocks.keys()) if obj.data.shape_keys else []
        item['material_bounds'] = []
        for idx, mat in enumerate(obj.data.materials):
            indices = {i for p in obj.data.polygons if p.material_index == idx for i in p.vertices}
            coords = [obj.matrix_world @ obj.data.vertices[i].co for i in indices]
            if coords:
                item['material_bounds'].append({'slot': idx, 'name': mat.name if mat else None, 'count': len(indices), 'min': [min(p[a] for p in coords) for a in range(3)], 'max': [max(p[a] for p in coords) for a in range(3)]})
    if obj.type == 'ARMATURE':
        result['bones'] = [{'name': b.name, 'head': list(b.head_local), 'tail': list(b.tail_local)} for b in obj.data.bones]
    result['objects'].append(item)
(root / 'outputs/reports/kagari_detail_scene.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('Audit saved:', root / 'outputs/reports/kagari_detail_scene.json')
