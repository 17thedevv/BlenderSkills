import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.wm.open_mainfile(filepath='D:/Project-17/blender/outputs/wip/kagari_vroid_master.blend')
body=bpy.data.objects['Body']
ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
me=ev.to_mesh()
bvh=BVHTree.FromPolygons([v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])
for z in [1.26,1.245,1.225,1.21,1.19,1.17,1.15,1.13,1.1,1.05,1.0,.95,.9]:
    hits=[]
    for x in [0,.025,.05,.075,.1,.125,.15]:
        hit,*_=bvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1.0)
        hits.append(round(hit.y,4) if hit else None)
    print('SAMPLE',z,hits)
