"""Temporary comparisons at identical pose/camera; does not save over any source."""
import bpy, json, math, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Project-17/blender'); REPORT=ROOT/'outputs/reports/concept_garment_v3'
PRE=ROOT/'outputs/previews/concept_garment_v3'; scene=bpy.context.scene
manifest=json.loads((REPORT/'render_manifest.json').read_text())
arm=bpy.data.objects['Study_Duplicate_Armature']; cam=scene.camera
neutral={p.name:p.matrix_basis.copy() for p in arm.pose.bones}
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
candidate=Path(bpy.data.filepath); initial_hash=sha(candidate)
for n in manifest['prototype_objects']: bpy.data.objects[n].hide_render=True
sets=[('prior_panel','outputs/wip/kagari_panel_drape_reset_final.blend',['Panel_Torso_One_Sleeve','Sewn_Overlapping_Collar']),
    ('cycle03','outputs/wip/kagari_v03_clay_03.blend',['Kagari_v03_Outer_Robe_And_Sleeves','Kagari_v03_Inner_Top','Kagari_v03_Sewn_Cross_Collar','Kagari_v03_Attached_Over_Wrap_Edge','Kagari_Obi_Woven_Band'])]
results=[]
for label,path,names in sets:
    with bpy.data.libraries.load(str(ROOT/path),link=False) as (a,b): b.objects=names
    imported=b.objects
    for o in imported:
        scene.collection.objects.link(o); o.hide_render=False; o.hide_set(False); o.hide_viewport=False; o.parent=arm
        for mod in o.modifiers:
            if mod.type=='ARMATURE': mod.object=arm
    renders=[]
    for r in manifest['renders']:
        for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
        arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler=r['arm_L_euler']
        cam.location=r['camera_location']; cam.rotation_euler=r['camera_rotation']; cam.data.ortho_scale=r['ortho_scale']
        bpy.context.view_layer.update()
        scene.render.filepath=str(PRE/(label+'_'+r['view']+'_clay.png')); bpy.ops.render.render(write_still=True)
        renders.append({'view':r['view'],'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
            'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler)})
    results.append({'label':label,'source':path,'source_sha256':sha(ROOT/path),'renders':renders})
    for o in imported: bpy.data.objects.remove(o,do_unlink=True)
assert initial_hash==sha(candidate)
(REPORT/'comparison_manifest.json').write_text(json.dumps({'candidate_sha256':initial_hash,'comparisons':results,
    'note':'Same duplicate mannequin, arms-down60 pose, camera and neutral clay. Previous panel study authored at down30; these images test its existing skinning at the new pose. Cycle03 includes two sleeves and obi, new study only one sleeve and no obi; not equal coverage.'},indent=2),encoding='utf-8')
print('CONCEPT_MATCHED_COMPARISONS_DONE')
