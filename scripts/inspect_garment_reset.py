"""Read-only inspection of the rejected artifact and locally available tools."""
import bpy, bmesh, addon_utils, json, hashlib
from pathlib import Path
ROOT=Path('D:/Project-17/blender'); OUT=ROOT/'outputs/reports/garment_reset'
OUT.mkdir(parents=True,exist_ok=True)
src=Path(bpy.data.filepath)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
objects=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH' or not (o.name.startswith('Kagari_v03_') or 'Obi' in o.name or o.name=='Body'): continue
    bm=bmesh.new(); bm.from_mesh(o.data)
    objects.append({'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),
      'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
      'boundary_edges':sum(e.is_boundary for e in bm.edges),'loose_vertices':sum(not v.link_faces for v in bm.verts),
      'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),
      'modifiers':[(m.name,m.type) for m in o.modifiers],
      'groups':[g.name for g in o.vertex_groups],
      'max_weight':max((g.weight for v in o.data.vertices for g in v.groups),default=None),
      'materials':[m.name if m else None for m in o.data.materials],
      'bounds_local':{axis:[min(v.co[k] for v in o.data.vertices),max(v.co[k] for v in o.data.vertices)] for k,axis in enumerate(['x','y','z'])}})
    bm.free()
arm=bpy.data.objects['Armature']
bones={b.name:{'head':list(b.head),'tail':list(b.tail),'rotation_mode':b.rotation_mode,'rotation_euler':list(b.rotation_euler)}
       for b in arm.pose.bones if any(s in b.name for s in ['UpperArm','LowerArm','Shoulder','Chest','Neck'])}
addons=[{'name':m.__name__,'file':getattr(m,'__file__',None),'enabled':addon_utils.check(m.__name__)[1]} for m in addon_utils.modules()]
inventory={'artifact':str(src),'sha256':sha(src),'blender':bpy.app.version_string,'objects':objects,'bones':bones,
           'native_cloth':hasattr(bpy.types,'ClothModifier'),'native_collision':hasattr(bpy.types,'CollisionModifier'),
           'addons':addons,'scope':'Only registered local Blender addons inspected; no software installation or asset download.'}
(OUT/'artifact_and_tools.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
print(json.dumps({'bones':bones,'garment_objects':objects,'addon_names':[a['name'] for a in addons]},indent=2))
