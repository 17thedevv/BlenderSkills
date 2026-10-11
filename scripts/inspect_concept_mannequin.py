import bpy, json, math
arm=bpy.data.objects['Study_Duplicate_Armature']
for side,angle in [('L',-60),('R',60)]:
    arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler.z=math.radians(angle)
bpy.context.view_layer.update()
ob=bpy.data.objects['Study_Duplicate_Mannequin']
ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
data={'bones':{b.name:{'head':list(b.head),'tail':list(b.tail)} for b in arm.pose.bones if any(x in b.name for x in ['Chest','Shoulder','UpperArm','LowerArm','Neck'])},'slices':{}}
for z in [1.00,1.05,1.10,1.15,1.20,1.23,1.25,1.27]:
    ps=[v.co for v in me.vertices if abs(v.co.z-z)<.012 and abs(v.co.x)<.18]
    if ps: data['slices'][str(z)]=[[min(p[k] for p in ps),max(p[k] for p in ps)] for k in range(3)]
print('CONCEPT_MANNEQUIN_DATA',json.dumps(data))
ev.to_mesh_clear()
