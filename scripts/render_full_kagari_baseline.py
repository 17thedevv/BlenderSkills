"""Render the unchanged Cycle03 avatar using full-integration review cameras. No save."""
import bpy, hashlib, json, sys
from pathlib import Path
from mathutils import Euler

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'outputs/reports/full_concept_v3'
PRE=ROOT/'outputs/previews/full_concept_v3'
manifest=json.loads((REPORT/'render_manifest.json').read_text())
source=ROOT/manifest['baseline']['path']
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==manifest['baseline']['sha256']
bpy.ops.wm.open_mainfile(filepath=str(source))
scene=bpy.context.scene; arm=bpy.data.objects['Armature']; cam=scene.camera
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
shade=scene.display.shading; shade.light='STUDIO'; shade.color_type='SINGLE'; shade.single_color=(.62,.62,.62)
shade.show_shadows=True; shade.show_cavity=True; shade.cavity_type='WORLD'
shade.cavity_ridge_factor=shade.cavity_valley_factor=.5; shade.show_specular_highlight=False
shade.background_type='WORLD'; scene.world.color=(.15,.15,.15)
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
cam.data.type='ORTHO'; neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
records=[]
for row in manifest['renders']:
    for name,matrix in neutral.items(): arm.pose.bones[name].matrix_basis=matrix.copy()
    for side,values in row['upper_arm_pose'].items(): arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler=Euler(values,'XYZ')
    bpy.context.view_layer.update()
    cam.location=row['camera_location']; cam.rotation_euler=row['camera_rotation']; cam.data.ortho_scale=row['ortho_scale']
    image=PRE/('cycle03_'+row['view']+'_clay.png'); scene.render.filepath=str(image)
    bpy.ops.render.render(write_still=True)
    records.append({**row,'path':image.relative_to(ROOT).as_posix(),'image_sha256':sha(image),'artifact_sha256':manifest['baseline']['sha256']})
assert sha(source)==manifest['baseline']['sha256']
(REPORT/'comparison_manifest.json').write_text(json.dumps({'baseline':manifest['baseline'],'candidate':manifest['candidate'],'matching':'Same camera, clay settings and upper arm pose; source avatar and its saved lower arm pose unchanged.','baseline_unchanged':True,'renders':records},indent=2),encoding='utf-8')
print('FULL_KAGARI_BASELINE_RENDERED',flush=True)
