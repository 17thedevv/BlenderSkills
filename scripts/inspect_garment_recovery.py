"""Read-only posed surface diagnosis of full concept v3."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'outputs/reports/garment_recovery_v1'
arm=bpy.data.objects['Armature']
def skin(o,v):
    m=Matrix(((0,0,0,0),)*4)
    for g in v.groups:
        n=o.vertex_groups[g.group].name
        if n in arm.pose.bones:m+=(arm.pose.bones[n].matrix@arm.data.bones[n].matrix_local.inverted())*g.weight
    return o.matrix_world@(m@v.co)
dep=bpy.context.evaluated_depsgraph_get(); surface={}
for name in ['Kagari_Concept_Robe_Two_Sleeves','Kagari_Concept_Crossed_Collar','Kagari_Concept_Soft_Waist_Sash','Kagari_Concept_Lower_Robe','Body_GarmentDisplay']:
    o=bpy.data.objects[name]; coords=[skin(o,v) for v in o.data.vertices]
    ev=o.evaluated_get(dep); me=ev.to_mesh(); verts=[ev.matrix_world@v.co for v in me.vertices]
    bvh=BVHTree.FromPolygons(verts,[list(p.vertices) for p in me.polygons])
    rays={}
    for z in [.94,.96,.975,.985,1.03,1.19,1.22,1.245,1.26,1.275,1.285]:
        for x in [0,.04,.07,.10,.13,.15]:
            front=bvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)
            back=bvh.ray_cast(Vector((x,.5,z)),Vector((0,-1,0)),1)
            rays[f'{x:.3f},{z:.3f}']={'front_y':front[0].y if front[0] is not None else None,'back_y':back[0].y if back[0] is not None else None,
                'front_face':front[2],'back_face':back[2],
                'front_vertex_ids':list(me.polygons[front[2]].vertices) if front[2] is not None else [],
                'back_vertex_ids':list(me.polygons[back[2]].vertices) if back[2] is not None else []}
    surface[name]={'vertices':len(coords),'faces':len(o.data.polygons),'matrix_world':[list(r) for r in o.matrix_world],
      'modifiers':[{'name':m.name,'type':m.type,'thickness':m.thickness if m.type=='SOLIDIFY' else None} for m in o.modifiers],
      'ray_sections':rays,'posed_coordinates':[list(p) for p in coords]}
    ev.to_mesh_clear()
(R/'source_mesh_diagnosis.json').write_text(json.dumps(surface,indent=2),encoding='utf-8')
for n,s in surface.items():
    print(n,s['vertices'],s['faces'])
    for k in ['0.100,0.960','0.130,0.975','0.040,1.260','0.040,1.275','0.070,1.245','0.100,1.245']:
        print(k,s['ray_sections'][k])
print('RECOVERY_INSPECTION_COMPLETE')
