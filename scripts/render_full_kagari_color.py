"""Existing shaders/textures preview only; no saved material or source changes."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Project-17/blender'); REPORT=ROOT/'outputs/reports/full_concept_v3'; PRE=ROOT/'outputs/previews/full_concept_v3'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
path=Path(bpy.data.filepath); digest=sha(path); scene=bpy.context.scene; cam=scene.camera
scene.render.engine='BLENDER_EEVEE_NEXT'; scene.render.resolution_x=1000; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0
views={'front':((0,-2,1.16),(0,0,1.16),1.04),'three_quarter':((1.2,-1.7,1.20),(0,0,1.16),1.04),
    'full_front':((0,-3,.77),(0,0,.77),1.70),'portrait':((0,-2,1.30),(0,0,1.30),.67)}
records=[]
for name,(pos,target,scale) in views.items():
    cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=scale
    scene.render.filepath=str(PRE/(name+'_existing_color.png')); bpy.ops.render.render(write_still=True)
    records.append({'view':name,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
        'artifact_sha256':digest,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':scale})
assert sha(path)==digest
(REPORT/'color_manifest.json').write_text(json.dumps({'candidate_sha256':digest,'engine':scene.render.engine,'renders':records,
    'materials':'Original source shaders/textures; existing cream/burgundy assigned to new garment; no new material design or ornamentation.',
    'vrm_material_compatibility':'NOT_TESTED'},indent=2),encoding='utf-8')
print('FULL_KAGARI_EXISTING_COLOR_RENDERED',flush=True)
