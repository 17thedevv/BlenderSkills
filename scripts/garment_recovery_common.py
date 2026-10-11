"""Evidence helpers for the two bounded geometry recovery iterations."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Matrix
from kagari_invariants import snapshot,digest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'outputs/wip/kagari_full_concept_v3.blend'
SOURCE_SHA='ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16'
EDITABLE={'Kagari_Concept_Robe_Two_Sleeves','Kagari_Concept_Crossed_Collar','Kagari_Concept_Soft_Waist_Sash'}
FULL_MANIFEST=json.loads((ROOT/'outputs/reports/full_concept_v3/render_manifest.json').read_text())
COLOR_MANIFEST=json.loads((ROOT/'outputs/reports/full_concept_v3/color_manifest.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
def untouched():
    out={}
    for o in bpy.data.objects:
        if o.type!='MESH' or o.name in EDITABLE:continue
        out[o.name]=digest({'coords':[list(v.co) for v in o.data.vertices],
          'faces':[(list(p.vertices),p.material_index) for p in o.data.polygons],
          'keys':{k.name:[list(p.co) for p in k.data] for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},
          'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
          'groups':[g.name for g in o.vertex_groups],
          'uvs':{u.name:[list(v.uv) for v in u.data] for u in o.data.uv_layers},
          'materials':[m.name if m else None for m in o.data.materials],
          'matrix':[list(r) for r in o.matrix_world],
          'parent':o.parent.name if o.parent else None,'hide_render':o.hide_render})
    return out
def weighted_matrix(o,v,arm):
    mat=Matrix(((0,0,0,0),)*4)
    for g in v.groups:
        name=o.vertex_groups[g.group].name
        if name in arm.pose.bones and g.weight>0:
            mat+=(arm.pose.bones[name].matrix@arm.data.bones[name].matrix_local.inverted())*g.weight
    return mat
def posed_coords(o):
    arm=bpy.data.objects['Armature']
    return [o.matrix_world@(weighted_matrix(o,v,arm)@v.co) for v in o.data.vertices]
def set_posed(o,coords):
    arm=bpy.data.objects['Armature']; inv=o.matrix_world.inverted()
    for v,p in zip(o.data.vertices,coords):v.co=weighted_matrix(o,v,arm).inverted()@(inv@p)
    o.data.update()
def configure_clay():
    s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH'
    s.render.resolution_x=s.render.resolution_y=1000;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    sh=s.display.shading;sh.light='STUDIO';sh.color_type='SINGLE';sh.single_color=(.62,.62,.62)
    sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='WORLD';sh.cavity_ridge_factor=sh.cavity_valley_factor=.5
    sh.show_specular_highlight=False;sh.background_type='WORLD';s.world.color=(.15,.15,.15)
    s.view_settings.view_transform='Standard';s.view_settings.look='None'
def camera(row):
    cam=bpy.context.scene.camera;cam.data.type='ORTHO';cam.location=row['camera_location']
    cam.rotation_euler=row['camera_rotation'];cam.data.ortho_scale=row['ortho_scale']
def render_evidence(candidate,report,preview):
    scene=bpy.context.scene;arm=bpy.data.objects['Armature'];path=ROOT/candidate['path']
    protected=snapshot();unt=untouched(); neutral={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
    records=[]
    def restore():
        for n,m in neutral.items():arm.pose.bones[n].matrix_basis=m.copy()
        bpy.context.view_layer.update()
    configure_clay()
    for row in FULL_MANIFEST['renders']:
        restore()
        for side,values in row['upper_arm_pose'].items():arm.pose.bones['J_Bip_'+side+'_UpperArm'].rotation_euler=values
        bpy.context.view_layer.update();camera(row)
        img=preview/(row['view']+'_clay.png');scene.render.filepath=str(img);bpy.ops.render.render(write_still=True)
        records.append({**row,'path':img.relative_to(ROOT).as_posix(),'image_sha256':sha(img),'artifact_sha256':candidate['sha256']})
    restore();scene.render.engine='BLENDER_EEVEE_NEXT';scene.view_settings.exposure=0
    colors=[]
    for row in COLOR_MANIFEST['renders']:
        camera(row);img=preview/(row['view']+'_existing_color.png');scene.render.filepath=str(img)
        bpy.ops.render.render(write_still=True)
        colors.append({**row,'path':img.relative_to(ROOT).as_posix(),'image_sha256':sha(img),'artifact_sha256':candidate['sha256']})
    restore();assert protected==snapshot() and unt==untouched()
    assert sha(path)==candidate['sha256'] and sha(SOURCE)==SOURCE_SHA
    dump(report/'render_manifest.json',{'candidate':candidate,'comparison_source':FULL_MANIFEST['candidate'],
      'renders':records,'new_objects':FULL_MANIFEST['new_objects'],'color_renders':colors,
      'camera_and_lighting':'Existing full_concept_v3 settings, unchanged source lighting/materials; gray Workbench and existing Eevee color.',
      'rendered_without_resaving_candidate':True,'human_approval':'NOT_APPROVED'})
