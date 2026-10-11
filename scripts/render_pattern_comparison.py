"""Read-only Recovery v2 comparison on exactly the prototype mannequin.
Usage: blender -b --python scripts/render_pattern_comparison.py -- trial2
Only the comparison copy is cropped; it is never a modeling foundation.
"""
import bpy,bmesh,json,sys,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TAG=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'trial2'
REPORT=ROOT/'outputs/reports/pattern_feasibility';PRE=ROOT/'outputs/previews/pattern_feasibility/comparison';PRE.mkdir(exist_ok=True)
SOURCE=ROOT/'outputs/wip/kagari_garment_recovery_v2.blend'
PROTO=ROOT/f'outputs/wip/kagari_pattern_{TAG}_prototype.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_sha=sha(SOURCE);proto_sha=sha(PROTO)
bpy.ops.wm.open_mainfile(filepath=str(PROTO))
sc=bpy.context.scene;arm=bpy.data.objects['Pattern_Study_Armature']
for o in sc.objects:
    if o.type=='MESH' and o.name not in ['Pattern_Duplicate_Upper_Mannequin','Plain_Mannequin_Head']:o.hide_render=True
with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):
    dst.objects=['Kagari_Concept_Robe_Two_Sleeves','Kagari_Concept_Crossed_Collar']
garments=dst.objects
crop_records=[]
for o in garments:
    sc.collection.objects.link(o);o.hide_render=False;o.hide_set(False);o.hide_viewport=False;o.parent=arm
    for m in o.modifiers:
        if m.type=='ARMATURE':m.object=arm
    bm=bmesh.new();bm.from_mesh(o.data);before=len(bm.faces)
    # Remove opposite sleeve and below-support geometry in the independent
    # comparison copy. Cut boundaries are diagnostic, not claimed improvements.
    remove=[f for f in bm.faces if f.calc_center_median().z<.98 or (o.name.endswith('Sleeves') and f.calc_center_median().x<-.14)]
    bmesh.ops.delete(bm,geom=remove,context='FACES_ONLY');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(o.data);bm.free();o.data.update()
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh()
    crop_records.append({'name':o.name,'original_raw_faces':before,'comparison_raw_faces':len(o.data.polygons),'raw_triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'evaluated_triangles_neutral':sum(len(p.vertices)-2 for p in em.polygons),'crop':'rest-space below z=.98; robe opposite sleeve x<-.14 only'})
    ev.to_mesh_clear()
man=json.loads((ROOT/'outputs/reports/pattern_feasibility'/TAG/'render_manifest.json').read_text());records=[]
for r in man['renders']:
    if r['deformation']!='ACTUAL_SEQUENTIAL_CLOTH_SNAPSHOT':continue
    angle={'neutral':-68,'raised30':-38,'horizontal':0}[r['pose']]
    arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z=math.radians(angle)
    bpy.context.view_layer.update();cam=sc.camera;row=r['camera'];cam.location=row['camera_location'];cam.rotation_euler=row['camera_rotation'];cam.data.ortho_scale=row['ortho_scale']
    p=PRE/f'recovery2_{r["pose"]}_{r["view"]}_clay.png';sc.render.filepath=str(p);bpy.ops.render.render(write_still=True)
    records.append({**r,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'deformation':'RECOVERY_V2_ORDINARY_ARMATURE','artifact_sha256':source_sha,'source_sha256':source_sha,'reference_prototype_sha256':proto_sha})
assert sha(SOURCE)==source_sha and sha(PROTO)==proto_sha
(REPORT/'comparison_manifest.json').write_text(json.dumps({'source_sha256':source_sha,'prototype_sha256':proto_sha,'render_settings':'Inherited exactly from prototype; same mannequin, camera, clay/shadows/cavity. Source sleeve cropped in comparison only. Raw original Recovery v2 gallery remains linked in report.','crop_records':crop_records,'renders':records},indent=2),encoding='utf8')
print('MATCHED_COMPARISON_COMPLETE')
