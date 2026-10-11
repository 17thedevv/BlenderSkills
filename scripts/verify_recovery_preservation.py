"""Compare topology, weights, UV assignment and modifier settings against exact full v3."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from garment_recovery_common import *
R=ROOT/'outputs/reports/garment_recovery_v2';manifest=json.loads((R/'render_manifest.json').read_text())
def value(v):
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    try:return list(v)
    except TypeError:return str(v)
def material_inventory():
    result={}
    for m in bpy.data.materials:
        nodes=[];links=[]
        if m.use_nodes and m.node_tree:
            for n in m.node_tree.nodes:
                nodes.append((n.name,n.bl_idname,[(i.name,value(i.default_value)) for i in n.inputs if hasattr(i,'default_value')],
                              n.image.name if hasattr(n,'image') and n.image else None))
            links=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]
        result[m.name]={'diffuse':list(m.diffuse_color),'nodes':sorted(nodes,key=lambda n:n[0]),'links':sorted(links)}
    return result
def garment_metadata():
    results={}
    for name in FULL_MANIFEST['new_objects']:
        o=bpy.data.objects[name];uv={}
        for layer in o.data.uv_layers:
            per_vertex={}
            for p in o.data.polygons:
                for li in p.loop_indices:
                    idx=o.data.loops[li].vertex_index
                    per_vertex.setdefault(idx,set()).add(tuple(layer.data[li].uv))
            uv[layer.name]=sorted((idx,sorted(vals)) for idx,vals in per_vertex.items())
        results[name]={
          'connectivity':digest(sorted(tuple(sorted(p.vertices)) for p in o.data.polygons)),
          'weights':digest([[(g.group,g.weight) for g in v.groups] for v in o.data.vertices]),
          'group_names':digest([g.name for g in o.vertex_groups]),'uv_assignment':digest(uv),
          'modifier_settings':digest([(m.name,m.type,m.object.name if m.type=='ARMATURE' and m.object else None,
              m.thickness if m.type=='SOLIDIFY' else None,m.offset if m.type=='SOLIDIFY' else None,m.show_render,m.show_viewport) for m in o.modifiers]),
          'material_names':digest([m.name if m else None for m in o.data.materials]),
          'parent':o.parent.name if o.parent else None}
    return results
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));source=garment_metadata();materials=material_inventory()
bound_materials={m.name for o in bpy.data.objects if o.type=='MESH' for m in o.data.materials if m}
bpy.ops.wm.open_mainfile(filepath=str(ROOT/manifest['candidate']['path']));target=garment_metadata();target_materials=material_inventory()
checks={n:{k:source[n][k]==target[n][k] for k in source[n]} for n in source}
used_materials_match=all(materials[n]==target_materials.get(n) for n in bound_materials)
new_materials=set(target_materials)-set(materials)
ok=all(v for row in checks.values() for v in row.values()) and used_materials_match and not new_materials
assert sha(SOURCE)==SOURCE_SHA and sha(ROOT/manifest['candidate']['path'])==manifest['candidate']['sha256']
dump(R/'preservation_details.json',{'candidate':manifest['candidate'],'comparison_source':FULL_MANIFEST['candidate'],
 'garment_metadata_matches':checks,'bound_material_node_defaults_links_and_images_unchanged':used_materials_match,
 'new_materials':sorted(new_materials),'unbound_material_datablocks_removed_on_save':sorted(set(materials)-set(target_materials)-bound_materials),
 'material_check_limits':'Node tree structure/default inputs and image datablock names; external image pixel files and every specialized node property not exhaustively hashed.',
 'material_differences':{n:{'source':materials.get(n),'candidate':target_materials.get(n)} for n in materials.keys()|target_materials.keys() if materials.get(n)!=target_materials.get(n)},
 'status':'PASS' if ok else 'FAIL','scope':'Data preservation only, not aesthetic approval'})
print('RECOVERY_PRESERVATION_DETAILS',ok)
if not ok:raise RuntimeError('Garment metadata/material preservation mismatch')
