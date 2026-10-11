"""Render Cycle 03 on the identical study mannequin, camera, A-pose and light."""
import bpy, json, math, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Project-17/blender')
REPORT=ROOT/'outputs/reports/garment_reset'
PRE=ROOT/'outputs/previews/garment_reset_comparison'; PRE.mkdir(parents=True,exist_ok=True)
prototype=Path(bpy.data.filepath)
arm=bpy.data.objects['Study_Duplicate_Armature']; scene=bpy.context.scene
for ob in scene.objects:
    if ob.name in ['Panel_Torso_One_Sleeve','Sewn_Overlapping_Collar']: ob.hide_render=True
src=ROOT/'outputs/wip/kagari_v03_clay_03.blend'
names=['Kagari_v03_Outer_Robe_And_Sleeves','Kagari_v03_Inner_Top','Kagari_v03_Sewn_Cross_Collar','Kagari_v03_Attached_Over_Wrap_Edge','Kagari_Obi_Woven_Band']
with bpy.data.libraries.load(str(src),link=False) as (a,b): b.objects=names
for ob in b.objects:
    scene.collection.objects.link(ob); ob.hide_render=False; ob.hide_set(False); ob.hide_viewport=False; ob.parent=arm
    for mod in ob.modifiers:
        if mod.type=='ARMATURE': mod.object=arm
neutral={p.name:p.matrix_basis.copy() for p in arm.pose.bones}
cam=scene.camera; target=Vector((.07,0,1.16))
views={'front':(0,-2,1.16),'three_quarter':(1.20,-1.7,1.20),'side':(2,0,1.16),'back':(0,2,1.16),'arm_raised':(0,-2,1.16)}
renders=[]
for name,pos in views.items():
    for n,m in neutral.items(): arm.pose.bones[n].matrix_basis=m.copy()
    if name=='arm_raised': arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler.z+=math.radians(30)
    cam.location=pos; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(PRE/('cycle03_'+name+'_clay.png'))
    bpy.context.view_layer.update(); bpy.ops.render.render(write_still=True)
    with Path(scene.render.filepath).open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    renders.append({'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':digest,'view':name,
        'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,
        'arm_L_euler':list(arm.pose.bones['J_Bip_L_UpperArm'].rotation_euler)})
(REPORT/'matched_cycle03_manifest.json').write_text(json.dumps({'source_artifact':str(src),'study_mannequin_file':str(prototype),
    'comparison_note':'Same bare mannequin/A-pose/framing as new method; original eight full-character images retained separately. Original garment uses both sleeves and obi; prototype intentionally has one sleeve and no obi.',
    'renders':renders},indent=2),encoding='utf-8')
print('MATCHED_COMPARISON_RENDERED')
