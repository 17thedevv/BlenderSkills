import bpy,json,hashlib
from pathlib import Path
ROOT=Path('D:/Project-17/blender'); OUT=ROOT/'outputs/reports/full_concept_v1'; OUT.mkdir(parents=True,exist_ok=True)
items=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH': continue
    items.append({'name':o.name,'hidden':o.hide_render,'vertices':len(o.data.vertices),'materials':[m.name if m else None for m in o.data.materials],
        'bounds':[[min(v.co[k] for v in o.data.vertices),max(v.co[k] for v in o.data.vertices)] for k in range(3)] if o.data.vertices else [],
        'shape_keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [],
        'modifiers':[(m.name,m.type) for m in o.modifiers]})
body=bpy.data.objects['Body']; zones=[]
for i,m in enumerate(body.data.materials):
    ids={v for p in body.data.polygons if p.material_index==i for v in p.vertices}
    zones.append({'slot':i,'material':m.name if m else None,'faces':sum(p.material_index==i for p in body.data.polygons),
        'bounds':[[min(body.data.vertices[j].co[k] for j in ids),max(body.data.vertices[j].co[k] for j in ids)] for k in range(3)] if ids else []})
payload={'objects':items,'body_zones':zones,'materials':{m.name:list(m.diffuse_color) for m in bpy.data.materials},
    'arm_pose':{b.name:list(b.rotation_euler) for b in bpy.data.objects['Armature'].pose.bones if any(x in b.name for x in ['UpperArm','LowerArm'])}}
(OUT/'source_inventory.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps({'visible':[(o['name'],o['bounds'],o['materials']) for o in items if not o['hidden']],'body_zones':zones,'arm_pose':payload['arm_pose']}))
