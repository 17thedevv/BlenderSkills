"""Protected geometry/morph/UV/material/rig fingerprints, independent of renders."""
import bpy,hashlib,json
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def snapshot():
    result={}
    for name in ['Face','Hair','Body']:
        o=bpy.data.objects[name]
        result[name]=digest({'verts':[list(v.co) for v in o.data.vertices],
            'polys':[(list(p.vertices),p.material_index) for p in o.data.polygons],
            'keys':{k.name:[list(v.co) for v in k.data] for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},
            'key_values':{k.name:k.value for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},
            'uvs':{uv.name:[list(v.uv) for v in uv.data] for uv in o.data.uv_layers},
            'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
            'groups':[g.name for g in o.vertex_groups],'materials':[m.name if m else None for m in o.data.materials],
            'parent':o.parent.name if o.parent else None,'parent_type':o.parent_type,
            'matrix':[list(row) for row in o.matrix_world],
            'modifiers':[(m.name,m.type,m.object.name if m.type=='ARMATURE' and m.object else None) for m in o.modifiers]})
    arm=bpy.data.objects['Armature']
    result['Armature_Rest']=digest({'bones':[(b.name,b.parent.name if b.parent else None,list(b.head_local),list(b.tail_local),[list(r) for r in b.matrix_local],b.use_deform) for b in arm.data.bones],
        'matrix':[list(r) for r in arm.matrix_world]})
    result['Armature_Saved_Pose']=digest([(b.name,b.rotation_mode,[list(r) for r in b.matrix_basis]) for b in arm.pose.bones])
    return result
