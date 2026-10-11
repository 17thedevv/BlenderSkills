"""Publish full-avatar WIP evidence. Human approval is never inferred from construction."""
from pathlib import Path
import hashlib, json, html

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'outputs/reports/full_concept_v3'; P=ROOT/'outputs/previews/full_concept_v3'
load=lambda p: json.loads(p.read_text(encoding='utf-8'))
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
m=load(R/'render_manifest.json'); t=load(R/'technical_verification.json'); a=load(R/'geometry_audit.json')
c=load(R/'comparison_manifest.json'); color=load(R/'color_manifest.json')
candidate=m['candidate']; digest=candidate['sha256']
assert sha(ROOT/candidate['path'])==digest and t['errors']==[]
assert t['protected_data_matches_after_reload']==dict.fromkeys(['Face','Hair','Body','Armature_Rest','Armature_Saved_Pose'],True)
for group in [m,c,color]:
    for row in group['renders']:
        assert sha(ROOT/row['path'])==row['image_sha256']
assert sha(ROOT/m['baseline']['path'])==m['baseline']['sha256']
assert sha(ROOT/m['garment_input']['path'])==m['garment_input']['sha256']

authorization='''# Full Kagari integration authorization

User message: “m hay dung han nguyen model kagari theo nhung gi m chinh sua”.

This directly authorizes building the complete avatar with the revised garment method,
including the second sleeve, waist and lower robe. It supersedes the earlier mannequin-only
construction limit. It does not approve the finished geometry, authorize software installation,
VRM delivery, new ornamentation or production material work. Skills development remains paused.

The approved action is completed as an independent .blend WIP. Existing face, hair, original
Body data, morphs, UVs, weights, rest rig and saved pose are protected. A separate Body display
copy removes obsolete clothing faces; the original remains intact in a hidden archive.
'''
(R/'user_authorization.md').write_text(authorization,encoding='utf-8')
issues=[
 {'id':'waist_overlap','region':'Top corners of front sash; side and rear waist','severity':'HIGH','inherited':False,'evidence':['front_existing_color.png','three_quarter_existing_color.png','back_clay.png'],'observation':'Cream torso surface visibly occludes/cuts into burgundy sash at both upper corners. Rear seam also has angular breaks. Earlier legacy skirt sawtooth was reduced, but waist overlap is not resolved.','next_action':'Reconcile torso/sash cross-sections and inspect front, side and back with color plus clay before any approval.'},
 {'id':'hair_scalp','region':'Temple and crown on character left; side/back head','severity':'HARD_REJECT','inherited':True,'evidence':['three_quarter_existing_color.png','side_clay.png','back_clay.png'],'observation':'Exposed dark scalp cap and detached/angular hair strips remain exactly as in Cycle03. Hair geometry was preserved, not repaired by garment integration.','next_action':'Separate scoped hair/scalp repair against reference with mesh and shape-key protection.'},
 {'id':'nape_yoke','region':'Back collar and top shoulder','severity':'MEDIUM','inherited':False,'evidence':['side_clay.png','three_quarter_clay.png'],'observation':'Collar nape projects as a stiff small shelf; shoulder has rounded bulges and limited cloth tension detail.','next_action':'Review nape fit and motivated shoulder folds on full avatar.'},
 {'id':'folds','region':'Sleeves, lower robe and back','severity':'MEDIUM','inherited':False,'evidence':['front_clay.png','arm_horizontal_clay.png','full_three_quarter_clay.png','back_clay.png'],'observation':'Long sleeves are hollow and continuous but very smooth at rest. Raised underarm forms broad rounded bags; folds do not recompute under gravity. Back and long skirt still have large nearly flat areas.','next_action':'Refine a few folds driven by seam, gravity and pose; retain silhouette and test motion.'},
 {'id':'concept_limits','region':'Outfit layers, full lower body, footwear','severity':'MEDIUM','inherited':False,'evidence':['full_front_existing_color.png'],'observation':'Cream/burgundy palette and long wide sleeves are readable. Separate long haori lapels and other concept motifs are not complete. Lower A-line robe is inferred from an upper-body-only reference; existing sneaker shoes are retained. This is not a faithful finished concept recreation.','next_action':'Human review of full silhouette and inferred lower design before accessories/material development.'}
]
review={
 'candidate':candidate,'decision':'REQUIRES_HUMAN_ART_REVIEW','agent_visual_review':'FAIL_FULL_AVATAR_ART_GATE_WITH_GARMENT_IMPROVEMENTS',
 'human_approval':'NOT_APPROVED','render_inspection':'Actual 9 final clay renders, 4 existing-color Eevee renders and 9 matching Cycle03 clay renders visually inspected.',
 'scores':{'garment_silhouette':1,'collar_construction':1,'sleeves_and_shoulders':2,'cloth_folds':1,'hair_silhouette':0,'reference_identity':1,'deformation':1},
 'score_semantics':'0 reject, 1 revise, 2 candidate; judgments from actual images, not automatic approval.',
 'hard_rejects':['Visible exposed scalp inherited from baseline'],
 'acceptance':{'fabric_thickness_and_overlap':'PARTIAL: cuff thickness and crossed collar readable; waist overlap fails',
 'shoulder_to_sleeve_continuity':'IMPROVED: both sleeves share torso root vertices; small shoulder ridges remain',
 'wide_sleeve_silhouette':'DEMONSTRATED_IN_TESTED_VIEWS','plausible_folds_and_volume':'PARTIAL: broad cloth masses, sparse folds, frozen drape',
 'no_obvious_mesh_intersections':'FAIL: visible torso/sash overlap; hair proximity also remains',
 'basic_arm_deformation':'PARTIAL: no gross detachment/collapse in two arm tests, rounded underarm bags; no motion or collision certification'},
 'issues':issues,'reviewed_images':[r['path'] for group in [m,color,c] for r in group['renders']],
 'all_images_linked_to_artifact_sha256':True,'vrm_export':'NOT_TESTED','full_character_construction':'COMPLETED_AS_WIP'
}
dump(R/'visual_review.json',review)
baseline=load(ROOT/'outputs/reports/v03_clay_cycle03/geometry_audit.json')
assert baseline['blend_sha256']==m['baseline']['sha256']
old_names=set(m['archived_objects'])
old=[o for o in baseline['mesh_report'] if o['name'] in old_names]
complexity={
 'candidate':candidate,'baseline':m['baseline'],
 'new_garment_surfaces':{'objects':4,'vertices':sum(o['vertices'] for o in t['objects']),'raw_triangles':sum(o['raw_triangles'] for o in t['objects']),
 'viewport_evaluated_triangles':sum(o['evaluated_triangles'] for o in t['poses'][0]['objects'])},
 'cycle03_separate_garment_meshes':{'objects':len(old),'raw_triangles':sum(o['raw']['triangles'] for o in old),'viewport_evaluated_triangles':sum(o['evaluated']['triangles'] for o in old)},
 'render_enabled_inventory':{'cycle03':baseline['render_enabled_inventory'],'candidate':a['render_enabled_inventory']},
 'all_scene_including_archive':{'raw_triangles':a['raw_triangles'],'viewport_evaluated_triangles':a['evaluated_triangles']},
 'limits':'Old separate meshes omit original clothing incorporated in Body. New count includes new lower robe. Render-enabled inventory ignores collection exclusion; viewport modifiers are evaluated, not VRM export. Archived geometry must be excluded from an eventual export. No runtime/FPS claim.'}
dump(R/'mesh_complexity_comparison.json',complexity)
report=f'''# Kagari — complete avatar with revised garment construction

**Construction delivered as a complete .blend WIP. Artistic gate: FAIL / requires human review.**

The full avatar now wears the revised crossed collar, connected torso and two long wide sleeves,
a softer narrow sash and a new waist-to-ankle robe. Face, hair, original Body data, all Face morph
coordinates/values, UVs, weights, rig rest data and saved pose match the original after reload.
This is a full-avatar integration of the corrected study, not a face/hair rebuild or final VRM.

- Candidate: [kagari_full_concept_v3.blend](../../wip/kagari_full_concept_v3.blend)
- Version: `{candidate['version']}`
- SHA256: `{digest}`
- Review: [interactive comparison](../../previews/full_concept_v3/review.html)
- Source concept: [concept_option2_kagari.jpg](../../design/concept_option2_kagari.jpg)
- User scope: [full-model authorization](user_authorization.md)

## Construction method

Controlled cloth surfaces with explicit connected sleeve roots, inverse skinning into the existing
rig rest space, sparse large fold shapes and thin Solidify thickness. Both sleeve roots reuse the
torso vertices; the second sleeve mirrors only the sleeve, not a duplicate torso. The crossed
collar has ordered under/over leaves and a connected nape. This method preserves ordinary armature
deformation. It is not a sewn 2D-pattern physics simulation: drape and folds are authored, not
recomputed by a Cloth solver. The failed Cloth experiment and original Cycle03 stay untouched.

Existing cream and burgundy materials are reused for a color preview; neutral Workbench clay
is the primary construction evidence. No new embroidery, accessory, material design or software
installation. Working panel UVs exist but are not a final garment texture atlas.

The original Body includes obsolete clothing in the same mesh. It remains intact in
`ARCHIVE_Rejected_Garments_Do_Not_Export`. An independent `Body_GarmentDisplay` copy removes those
old cloth faces while retaining skin, shoes and inner upper torso. Body has no shape keys. The
new lower robe was required after the old skirt edge appeared as a sawtooth beneath the smaller
sash. Its long A-line silhouette is an inference; the reference supplies no lower/side/back views.
The archive remains in the file for recovery, not for eventual export.

## Visible comparison with Cycle03

| Region | Cycle03 | Integrated candidate |
|---|---|---|
| Sleeves | Short rigid cylindrical blocks | Long hollow flared cloth surfaces, readable cuff thickness |
| Shoulder | Detached-looking open joins | Shared root topology and continuous form on both sides |
| Collar | Pinched chest triangles and irregular crossing | Wider curved leaves with a much clearer crossing |
| Torso | Broad flat shell | Some waist/chest volume and folds; back remains too smooth |
| Waist | Large rigid cuboid band | Thinner curved band, but visible torso/sash overlap remains |
| Lower robe | Old cut cloth silhouette | Continuous new shell with a few vertical fold channels; still too smooth |
| Arm tests | Rigid raised short sleeve blocks | Continuous sleeves at raised and horizontal arms; broad frozen underarm bags |
| Hair | Scalp gaps and planar rear strips | Identical source geometry; these defects remain |

All nine clay comparisons use matching camera positions, scale, gray display and upper-arm pose.
Two arm tests are both arms raised 30 degrees from the saved pose (about 38 degrees below
horizontal), and upper arms horizontal. They are rendered armature poses, not animated cloth
or collision tests. Original saved pose is restored before preservation verification.

## Remaining defects and artistic decision

The candidate does not meet the no-visible-intersections criterion. Cream cloth cuts into the
burgundy sash near both front corners; rear waist joins have angular breaks. The nape collar is
still shelf-like, rest sleeves and lower skirt lack motivated folds, and the raised sleeve volume
looks like broad rounded bags. Side/back hair still exposes the old scalp and flat strips; the
scalp defect is a hard rejection under the visual rubric. The color preview makes the waist and
scalp defects especially clear. No artistic success or final concept fidelity is claimed.

Separate long haori lapels and the complete layer hierarchy remain incomplete; existing sneakers
also remain. Decorations were deliberately outside this construction request. Human review is
needed for the inferred full lower silhouette. This delivery stops after three integration
configurations with these defects disclosed, without declaring the avatar approved.

See [visual review](visual_review.json) for precise image evidence and next actions.

## Geometry and verification

| Scope | Raw triangles | Viewport evaluated triangles |
|---|---:|---:|
| Four new garment surfaces | 20,105 | 41,908 |
| Cycle03 five separate garment meshes | 6,880 | 17,544 |
| Candidate render-enabled inventory | 47,434 | 118,773 |
| Cycle03 render-enabled inventory | 36,741 | 96,941 |
| Candidate entire scene including hidden/archive | 86,936 | 189,019 |

The five old meshes exclude clothing embedded in Body; the four new surfaces include the lower
robe. These counts are not a like-for-like garment-only cost comparison. Render-enabled counts
use object hide_render and viewport modifiers, without simulating collection exclusion. They
are not final render/export counts, VRM triangle budgets or FPS measurements.

Each new garment surface is one connected component, with no zero-area faces or interior
nonmanifold edges. Open sheet boundaries are intentional and thickened by Solidify. All garment
vertices have normalized deform weights and no more than four influences. All armature modifiers
reference the original `Armature`. Evaluated positions are finite in saved, raised and horizontal
poses. Protected source data matches after reload. These technical checks do not prove art quality
or intersection freedom. [Technical verification](technical_verification.json),
[geometry audit](geometry_audit.json), [complexity details](mesh_complexity_comparison.json).

## VRM and rigging risks

- Hidden archived Body/old garments must be explicitly excluded from export to avoid duplicated skin/clothes.
- Skinning gives a fixed drape; no gravity response, skirt physics or full animation acceptance exists.
- New lower robe currently binds to hips/spine. Walking, leg raises and sitting are not tested;
  coat/skirt secondary bones need separate work before runtime use.
- Working UVs and inherited Blender shaders require eventual VRM/MToon validation; reused materials
  are not certified by successful Eevee rendering.
- Solidify cost, normals, export triangulation, VRM reimport, expressions and Warudo tracking remain untested.

No Skills expansion, ornamentation, material production or VRM export was performed. The full
construction requested by the user is delivered; the artistic acceptance gate remains unapproved.
'''
(R/'report.md').write_text(report,encoding='utf-8')
labels={'front':'Chính diện','three_quarter':'Góc 3/4','side':'Nghiêng','back':'Phía sau','arm_raised':'Giơ hai tay','arm_horizontal':'Tay ngang','full_front':'Toàn thân trước','full_three_quarter':'Toàn thân 3/4','portrait':'Cận mặt'}
buttons=''.join(f'<button type="button" data-view="{v}">{html.escape(labels[v])}</button>' for v in labels)
rows=''.join(f'<option value="{r["view"]}">{html.escape(labels[r["view"]])}</option>' for r in color['renders'])
page='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kagari — model đầy đủ với trang phục mới</title>
<style>body{margin:0;background:#16161b;color:#eeedf2;font:16px/1.6 system-ui}main{max-width:1240px;margin:auto;padding:32px 24px}h1{font-size:36px;line-height:1.15;margin:10px 0}h2{font-size:22px}p{max-width:900px;color:#c8c5cf}a{color:#ecc0ce}nav{display:flex;gap:10px;flex-wrap:wrap}button,select{background:#292630;color:inherit;border:1px solid #504752;border-radius:8px;padding:10px;cursor:pointer;font:inherit}button[aria-pressed=true]{background:#694055;border-color:#c891ad}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;display:block;background:#333;border-radius:12px}figcaption{padding:8px 0;color:#c8c5cf}.tag{display:inline-block;background:#613c49;padding:4px 12px;border-radius:30px;font-size:13px}.note{border-left:3px solid #d6a1b6;padding:4px 20px;margin:24px 0}section{margin-top:38px}.links{margin:18px 0}.reference{max-width:480px}.meta{font-size:12px;overflow-wrap:anywhere} @media(max-width:650px){.grid{grid-template-columns:1fr}h1{font-size:28px}main{padding:22px 16px}}</style>
<main><span class="tag">Bản dựng đầy đủ · Chưa đạt duyệt mỹ thuật</span><h1>Kagari: trang phục mới trên toàn bộ model</h1>
<p>Cổ áo chồng lớp, hai tay áo rộng nối liền thân áo, đai eo và váy mới. Mặt, tóc, morph và rig gốc được giữ nguyên. Đây là bản WIP để xem trực tiếp, chưa phải avatar hoàn thiện.</p>
<div class="links"><a href="../../wip/kagari_full_concept_v3.blend">File Blender</a> · <a href="../../reports/full_concept_v3/report.md">Báo cáo</a> · <a href="../../reports/full_concept_v3/visual_review.json">Lỗi còn lại</a></div>
<div class="note"><strong>Lỗi cần thấy trước khi duyệt:</strong><p>Mép thân áo giao nhau với đai eo ở hai bên; cổ sau còn cứng. Tóc gốc vẫn hở da đầu ở góc nghiêng và quá phẳng phía sau. Nếp rủ và biến dạng mới chỉ đạt một phần.</p></div>
<section><h2>Ảnh màu với vật liệu sẵn có</h2><label for="color-view">Góc nhìn </label><select id="color-view">OPTIONS</select><p>Màu kem/burgundy dùng lại từ bản gốc. Không thêm shader, trang trí hay phụ kiện mới.</p><figure style="max-width:780px"><img id="color-img" src="full_front_existing_color.png" alt="Kagari toàn thân, vật liệu sẵn có"><figcaption id="color-caption">Toàn thân trước</figcaption></figure></section>
<section><h2>So sánh clay cùng góc máy</h2><p>Trái: Cycle 03 bị từ chối. Phải: bản tích hợp mới. Tư thế giơ tay dùng rig thông thường; không phải mô phỏng vải động.</p><nav aria-label="Chọn góc clay">BUTTONS</nav><div class="grid" style="margin-top:18px"><figure><img id="old" src="cycle03_front_clay.png" alt="Cycle 03 — chính diện"><figcaption>Cycle 03</figcaption></figure><figure><img id="new" src="front_clay.png" alt="Bản tích hợp — chính diện"><figcaption id="view-caption">Bản tích hợp · Chính diện</figcaption></figure></div></section>
<section><h2>Concept dùng để dựng</h2><p>Ảnh Kagari hiện có trong dự án. Phần váy toàn thân và mặt sau được suy luận vì concept không thể hiện các vùng này. Chưa tái hiện đầy đủ các lớp haori và chi tiết thiết kế.</p><img class="reference" src="../../design/concept_option2_kagari.jpg" alt="Concept Kagari trong dự án"></section>
<section><h2>Kiểm tra đã thực hiện</h2><p>Đã xem 9 ảnh clay, 4 ảnh màu và 9 ảnh clay đối chiếu. Dữ liệu bảo vệ khớp sau khi mở lại file; bốn bề mặt trang phục có weights chuẩn hóa và dùng rig gốc. Các kiểm tra đó không thay thế duyệt mỹ thuật.</p><p>Chưa kiểm tra bước đi/váy, xuất VRM hay Warudo. Bản gốc và mẫu một tay áo vẫn được lưu riêng.</p><p class="meta">VERSION · SHA256: DIGEST</p></section></main>
<script>const labels=LABELS;const views=document.querySelectorAll('[data-view]');for(const b of views){b.addEventListener('click',()=>{for(const q of views)q.setAttribute('aria-pressed',String(q===b));const v=b.dataset.view;document.getElementById('old').src='cycle03_'+v+'_clay.png';document.getElementById('new').src=v+'_clay.png';document.getElementById('old').alt='Cycle 03 — '+labels[v];document.getElementById('new').alt='Bản tích hợp — '+labels[v];document.getElementById('view-caption').textContent='Bản tích hợp · '+labels[v]})}views[0].click();const sel=document.getElementById('color-view');sel.value='full_front';sel.addEventListener('change',()=>{document.getElementById('color-img').src=sel.value+'_existing_color.png';document.getElementById('color-img').alt='Kagari — '+labels[sel.value];document.getElementById('color-caption').textContent=labels[sel.value]});</script></html>'''
page=page.replace('BUTTONS',buttons).replace('OPTIONS',rows).replace('LABELS',json.dumps(labels,ensure_ascii=False)).replace('VERSION',candidate['version']).replace('DIGEST',digest)
(P/'review.html').write_text(page,encoding='utf-8')

state_path=ROOT/'config/project_state.json'; state=load(state_path)
previous=state['current_candidate']; state['previous_candidate']=previous
state['current_candidate']=candidate; state['current_character_source']=candidate.copy()
state['current_gate']='FULL_AVATAR_GARMENT_REVIEW_PENDING'
state['current_candidate_role']='FULL_KAGARI_AVATAR_WITH_CONCEPT_GARMENT_WIP'
state['decision']='REQUIRES_HUMAN_ART_REVIEW'
state['agent_visual_review']=review['agent_visual_review']
state['construction_authorization']={'evidence':(R/'user_authorization.md').relative_to(ROOT).as_posix(),'scope':'Full avatar integration including both sleeves, collar, torso, sash and lower robe; preserve original face/hair/Body data/rig','approval_of_result':False}
state['full_model_construction']='COMPLETED_AS_WIP'
state['blocking_issues']=[i['observation'] for i in issues]+['Human full-avatar artistic review pending','VRM export/reimport, lower body motion and runtime not tested']
state['updated_by']='report_full_kagari.py; full construction authorized by user, no artistic approval inferred'
state['body_render_surface']={'active':'Body_GarmentDisplay','original':'Body','original_data_intact':True,'archived_original_must_be_excluded_from_export':True}
for gate in ['garment_clay','full_avatar']:
    state['approvals'][gate]={'status':'NOT_APPROVED','evidence':None}
new_paths=[p for p in R.iterdir() if p.suffix in ['.json','.md']]+list(P.glob('*.png'))+[P/'review.html']
new_paths += [ROOT/f'outputs/wip/kagari_full_concept_v{i}.blend' for i in [1,2,3]]
new_paths += [ROOT/'outputs/reports/full_concept_v1/construction_plan.md',ROOT/'outputs/reports/full_concept_v1/source_inventory.json']
for p in new_paths:
    rel=p.relative_to(ROOT).as_posix()
    if rel not in state['evidence']: state['evidence'].append(rel)
    record={'path':rel,'sha256':sha(p)}
    state['artifact_records']=[r for r in state['artifact_records'] if r['path']!=rel]+[record]
dump(state_path,state)
block={'candidate_path':candidate['path'],'candidate_sha256':digest,'candidate_version':candidate['version'],'decision':state['decision']}
delivery=f'''# Kagari — current review artifact

Complete avatar WIP with revised crossed collar, connected torso and both long wide sleeves,
curved sash and inferred lower robe. **Artistic acceptance remains FAIL / requires human review.**
Original face/hair/Body data, morphs, UVs, weights, rest rig and saved pose match after reload.
Original Body/old garments are archived; the active Body display copy omits obsolete cloth.

- [Current full avatar Blender file](wip/kagari_full_concept_v3.blend)
- [Review gallery: clay, existing-color and matching Cycle03](previews/full_concept_v3/review.html)
- [Report and remaining defects](reports/full_concept_v3/report.md)
- [Technical verification](reports/full_concept_v3/technical_verification.json)
- [Geometry audit](reports/full_concept_v3/geometry_audit.json)
- [Visual review](reports/full_concept_v3/visual_review.json)
- [Explicit full-model construction scope](reports/full_concept_v3/user_authorization.md)
- [Preserved rejected Cycle03 baseline](wip/kagari_v03_clay_03.blend)
- [Preserved one-sleeve study](wip/kagari_concept_garment_v3.blend)

Visible waist intersections, a stiff nape, insufficient folds and inherited scalp/rear-hair defects
remain. 9 final clay views and 4 color previews were inspected. Two basic armature poses are
demonstrated; cloth dynamics, lower-body motion, VRM and Warudo are untested. No human approvals
were inferred, no new decorations/material design/software installation and no Skills development.

Four new garment surfaces: 20,105 raw / 41,908 viewport-evaluated triangles.
Render-enabled inventory: 47,434 raw / 118,773 viewport-evaluated triangles, not exported VRM/FPS.
The hidden archive must be excluded from an eventual export.

<!-- PROJECT_STATE_BEGIN -->
```json
{json.dumps(block,indent=2)}
```
<!-- PROJECT_STATE_END -->
'''
(ROOT/'outputs/DELIVERY.md').write_text(delivery,encoding='utf-8')
print('FULL_KAGARI_REPORT_WRITTEN',digest)
