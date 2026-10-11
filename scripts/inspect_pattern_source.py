import bpy,json
from pathlib import Path
p=Path('D:/Project-17/blender/outputs/wip/kagari_garment_recovery_v2.blend')
bpy.ops.wm.open_mainfile(filepath=str(p))
a=bpy.data.objects['Armature']; o=bpy.data.objects['Body_GarmentDisplay']
for s in ['L','R']:
 for n in ['UpperArm','LowerArm']:
  a.pose.bones['J_Bip_'+s+'_'+n].rotation_euler=(0,0,0)
bpy.context.view_layer.update()
e=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); m=e.to_mesh()
d={'bones':{b.name:{'head':list(b.head),'tail':list(b.tail)} for b in a.pose.bones if any(x in b.name for x in ['Chest','Shoulder','UpperArm','LowerArm','Neck'])},'slices':{}}
for z in [1.0,1.1,1.2,1.23,1.25,1.27]:
 ps=[v.co for v in m.vertices if abs(v.co.z-z)<.008 and abs(v.co.x)<.16]
 if ps:d['slices'][z]=[[min(p[k] for p in ps),max(p[k] for p in ps)] for k in range(3)]
d['materials']=[m.name for m in o.data.materials]
Path('D:/Project-17/blender/outputs/reports/pattern_feasibility/mannequin_inspection.json').write_text(json.dumps(d,indent=2))
print(json.dumps(d))
