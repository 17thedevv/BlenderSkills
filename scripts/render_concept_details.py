import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Project-17/blender'); PRE=ROOT/'outputs/previews/concept_garment_v3'; REPORT=ROOT/'outputs/reports/concept_garment_v3'
candidate=Path(bpy.data.filepath)
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
digest=sha(candidate); scene=bpy.context.scene; cam=scene.camera; records=[]
for name,pos,target,scale in [('front_detail',(0,-2,1.17),(.035,0,1.17),.52),('three_quarter_detail',(1.2,-1.7,1.19),(.035,0,1.17),.52)]:
    cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=scale
    scene.render.filepath=str(PRE/(name+'_clay.png')); bpy.ops.render.render(write_still=True)
    records.append({'name':name,'path':Path(scene.render.filepath).relative_to(ROOT).as_posix(),'image_sha256':sha(Path(scene.render.filepath)),
        'artifact_sha256':digest,'camera_location':list(pos),'camera_target':list(target),'ortho_scale':scale,
        'note':'Additional construction close-up; sleeve cropped. Full silhouette and pose views remain in render_manifest.json.'})
assert sha(candidate)==digest
(REPORT/'detail_manifest.json').write_text(json.dumps({'candidate_sha256':digest,'renders':records},indent=2),encoding='utf-8')
print('CONCEPT_DETAILS_RENDERED')
