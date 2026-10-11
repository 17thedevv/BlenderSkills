"""Reload prototype; audit topology, source hashes and finite pose coordinates.
No intersection-free or artistic certificate is inferred from these checks.
"""
import bpy,bmesh,json,hashlib,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TAG=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'trial2'
REPORT=ROOT/'outputs/reports/pattern_feasibility'/TAG
MAN=json.loads((REPORT/'render_manifest.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/MAN['candidate']['path']))
records=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH' or not o.name.startswith(('Simulated_','Collar_','Rig_Only_')):continue
    bm=bmesh.new();bm.from_mesh(o.data)
    face_components=[];todo=set(bm.faces)
    while todo:
        stack=[todo.pop()];n=0
        while stack:
            f=stack.pop();n+=1
            for e in f.edges:
                for other in e.link_faces:
                    if other in todo:todo.remove(other);stack.append(other)
        face_components.append(n)
    row={'object':o.name,'raw_vertices':len(bm.verts),'raw_faces':len(bm.faces),'raw_triangles':sum(len(f.verts)-2 for f in bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'interior_nonmanifold_edges':sum(len(e.link_faces)>2 for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'face_component_sizes':sorted(face_components,reverse=True),'uv_layers':[u.name for u in o.data.uv_layers],'modifiers':[{'name':m.name,'type':m.type} for m in o.modifiers]}
    bm.free();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();row['evaluated_triangles']=sum(len(p.vertices)-2 for p in me.polygons);row['evaluated_finite']=all(math.isfinite(x) for v in me.vertices for x in v.co);ev.to_mesh_clear();records.append(row)
source=ROOT/MAN['source_character']['path'];backup=ROOT/'outputs/backups/pattern_feasibility_start/kagari_garment_recovery_v2.blend'
verified={'candidate_sha_matches':sha(ROOT/MAN['candidate']['path'])==MAN['candidate']['sha256'],'source_sha_matches':sha(source)==MAN['source_character']['sha256'],'backup_byte_hash_matches_source':sha(backup)==sha(source),'setup_sha_matches':sha(ROOT/MAN['source_setup']['path'])==MAN['source_setup']['sha256'],'all_images_hash_match':all(sha(ROOT/r['path'])==r['sha256'] for r in MAN['renders']),'all_evaluations_finite':all(r['evaluated_finite'] for r in records)}
(REPORT/'technical_verification.json').write_text(json.dumps({'checks':verified,'meshes':records,'result':'PASS_DATA_INTEGRITY_ONLY' if all(verified.values()) else 'FAIL','intersections':'NOT_CERTIFIED; inspect real images, solver seam residuals and visual findings','rigging':'Only Rig_Only_Neutral_Drape has preview weights; simulated snapshots are static geometry at matching body poses','VRM':'NOT_EXPORTED_NOT_RUNTIME_TESTED'},indent=2),encoding='utf8')
print('PATTERN_DATA_CHECKS',verified)
