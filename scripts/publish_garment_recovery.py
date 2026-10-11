"""Publish reviewed recovery evidence and synchronize the current candidate; never approve art."""
from pathlib import Path
import hashlib,json,html
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'outputs/reports/garment_recovery_v2';P=ROOT/'outputs/previews/garment_recovery_v2'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=load(R/'render_manifest.json');t=load(R/'technical_verification.json');a=load(R/'geometry_audit.json')
v1=load(ROOT/'outputs/reports/garment_recovery_v1/render_manifest.json')
old=load(ROOT/'outputs/reports/full_concept_v3/render_manifest.json')
old_color=load(ROOT/'outputs/reports/full_concept_v3/color_manifest.json')
candidate=m['candidate'];source=m['comparison_source']
assert sha(ROOT/candidate['path'])==candidate['sha256'] and sha(ROOT/source['path'])==source['sha256']
assert t['errors']==[] and load(R/'preservation_details.json')['status']=='PASS'
assert a['blend_sha256']==candidate['sha256']
for manifest in [m,v1,old]:
    for row in manifest['renders']+manifest.get('color_renders',[]):assert sha(ROOT/row['path'])==row['image_sha256']
for row in old_color['renders']:assert sha(ROOT/row['path'])==row['image_sha256']
for rows in [m['renders'],v1['renders']]:
    for row in rows:
        previous=next(r for r in old['renders'] if r['view']==row['view'])
        assert all(row[k]==previous[k] for k in ['camera_location','camera_rotation','ortho_scale','upper_arm_pose'])
for row in m['color_renders']:
    previous=next(r for r in old_color['renders'] if r['view']==row['view'])
    assert all(row[k]==previous[k] for k in ['camera_location','camera_rotation','ortho_scale'])
dump(R/'comparison_manifest.json',{'candidate':candidate,'source':source,'iteration1':v1['candidate'],
 'source_clay':old['renders'],'source_color':old_color['renders'],'candidate_clay':m['renders'],'candidate_color':m['color_renders'],
 'matching_camera_scale_and_arm_pose_verified':True,'lighting_materials':'Existing full-v3 scene and material setup; no new materials or framing changes.'})
issues=[
 {'id':'remaining_waist_crossings','region':'Character left inner sleeve/sash side, x=.150-.155,y=.020-.027,z=.927-.947 in saved pose','severity':'STRUCTURAL_REVIEW_REQUIRED',
  'evidence':['outputs/reports/garment_recovery_v2/technical_verification.json','outputs/previews/garment_recovery_v2/side_clay.png','outputs/previews/garment_recovery_v2/front_existing_color.png'],
  'observation':'No prominent cream triangles on inspected front/3q color; 13 evaluated crossing segments persist at side waist. No full intersection-free claim.',
  'likely_cause':'Pose-aware Body clearance moves part of the sleeve inner seam back toward the sash. This is a local point-fit construction limitation.',
  'proposed_next_action':'Reconcile seam volume and layer clearance together before another authorized construction method trial; no third repair in this task.',
  'predicted_effect':'Eliminate residual sleeve/sash contact without reintroducing arm/body contacts.'},
 {'id':'collar_support_crossings','region':'Nape/leaf transition and underlying robe at neck','severity':'STRUCTURAL_REVIEW_REQUIRED',
  'evidence':['outputs/previews/garment_recovery_v2/side_clay.png','outputs/previews/garment_recovery_v2/three_quarter_existing_color.png','outputs/reports/garment_recovery_v2/technical_verification.json'],
  'observation':'Smaller nape shelf than full v3; 87 collar/robe crossing segments in each tested pose. Some edge irregularity remains.',
  'likely_cause':'Separately lofted collar and shoulder-support surfaces do not share a fully solved seam/clearance structure.',
  'proposed_next_action':'A separate collar/shoulder seam construction trial after human review, rather than more point projection.',
  'predicted_effect':'Continuous neck-to-shoulder form with ordered collar layers.'},
 {'id':'frozen_underarm_volume','region':'Shoulder crown and sleeve underside in raised/horizontal arms','severity':'ARTISTIC_REVISE',
  'evidence':['outputs/previews/garment_recovery_v2/arm_raised_clay.png','outputs/previews/garment_recovery_v2/arm_horizontal_clay.png','outputs/previews/garment_recovery_v2/three_quarter_clay.png'],
  'observation':'No gross sleeve detachment in inspected images; large rounded underarm bags and local pinching remain. Sparse folds still do not communicate cloth tension/drape well.',
  'likely_cause':'Fixed authored drape and conventional skinning do not recompute gravity/tension when pose changes.',
  'proposed_next_action':'Evaluate seam/pattern form on target poses before selecting cloth-assisted shaping or corrective deformation in another authorized task.',
  'predicted_effect':'More plausible shoulder folds and gravity-directed volume.'},
 {'id':'inherited_hair_and_design','region':'Scalp/rear hair; lower design and haori layers','severity':'OUT_OF_SCOPE_UNCHANGED','outside_task_scope':True,
  'evidence':['outputs/previews/garment_recovery_v2/back_clay.png','outputs/previews/garment_recovery_v2/three_quarter_existing_color.png','outputs/previews/garment_recovery_v2/full_front_existing_color.png'],
  'observation':'Existing scalp exposure, planar rear hair, incomplete haori layering and unapproved inferred skirt/shoes remain. Hair/face/lower data preserved exactly.',
  'likely_cause':'Inherited source and absent approved side/back/lower reference; not caused by this garment recovery.',
  'proposed_next_action':'Separate human design/hair decision; no hair or turnaround reconstruction in this task.',
  'predicted_effect':'Remove inherited full-avatar blockers once separately authorized and reviewed.'}
]
review={'candidate':candidate,'comparison_source':source,'iterations_completed':2,'iteration_limit':2,
 'recommendation':'FAIL','recommendation_scope':'Entire garment geometry recovery is not reliably accepted; waist appearance improved but local crossings and shoulder/fold defects remain.',
 'human_approval':'NOT_APPROVED','decision':'REQUIRES_HUMAN_ART_REVIEW',
 'agent_visual_review':'IMPROVED_WAIST_PARTIAL_COLLAR_SHOULDER_NOT_ACCEPTED',
 'actual_images_inspected':{'iteration1':13,'iteration2':13,'source_full_v3':'Previously inspected 9 clay + 4 color, reused at matching cameras with verified image/artifact SHA.'},
 'waist_visual':'IMPROVED_IN_INSPECTED_VIEWS','waist_collision_free':'NOT_CERTIFIED',
 'collar_shoulders':'PARTIAL_REPAIR','cloth_drape':'NOT_ACCEPTED','scoped_collision_diagnostics':'RESIDUAL_CROSSINGS_FOUND',
 'art_gate':'NOT_APPROVED','vrm_tracking_animation_readiness':'NOT_TESTED','issues':issues,
 'method_limit':'Fixed controlled cloth surfaces and skinning solve local clearance but do not reliably solve seam continuity, coupled layer contacts and pose-dependent drape. Stop after two iterations.'}
dump(R/'visual_review.json',review)
baseline_audit=load(ROOT/'outputs/reports/full_concept_v3/geometry_audit.json')
new_names=set(m['new_objects'])
mods=[{'object':row['name'],'raw':row['raw']['triangles'],'evaluated':row['evaluated']['triangles'],'modifiers':row['modifier_costs']} for row in a['mesh_report'] if row['name'] in new_names]
dump(R/'geometry_comparison.json',{'candidate':candidate,'source':source,'render_enabled_source':baseline_audit['render_enabled_inventory'],
 'render_enabled_candidate':a['render_enabled_inventory'],'raw_scene_delta':a['raw_triangles']-baseline_audit['raw_triangles'],
 'evaluated_scene_delta':a['evaluated_triangles']-baseline_audit['evaluated_triangles'],'garment_modifier_contributions':mods,
 'count_limits':'Viewport evaluation; render-enabled object inventory does not simulate collection exclusion. Not exported VRM count or runtime FPS.'})
labels={'front':'Trước · pose lưu','three_quarter':'Góc 3/4','side':'Nghiêng','back':'Sau','arm_raised':'Nâng hai tay','arm_horizontal':'Tay ngang','full_front':'Toàn thân trước','full_three_quarter':'Toàn thân 3/4','portrait':'Cận mặt'}
buttons=''.join(f'<button type="button" data-view="{v}">{html.escape(label)}</button>' for v,label in labels.items())
page='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kagari — Garment Recovery v2</title>
<style>body{margin:0;background:#17171c;color:#eeecf1;font:16px/1.55 system-ui}main{max-width:1280px;margin:auto;padding:30px 24px}h1{font-size:36px;line-height:1.2;margin:12px 0}h2{font-size:22px}p{max-width:940px;color:#cbc7d0}.tag{display:inline-block;background:#673e4d;border-radius:25px;padding:5px 13px;font-size:13px}.note{border-left:3px solid #dba4ba;padding:4px 18px;margin:24px 0}a{color:#efbed3}nav,.controls{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}button,select{font:inherit;background:#292530;color:inherit;border:1px solid #574d5a;border-radius:8px;padding:9px 12px;cursor:pointer}button[aria-pressed=true]{background:#69465a;border-color:#d19ab4}button:disabled{opacity:.35;cursor:default}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;display:block;border-radius:10px;cursor:zoom-in;background:#777}figcaption{padding:9px 0;color:#cdc6d0}.meta{font-size:12px;overflow-wrap:anywhere}section{margin-top:30px}@media(max-width:680px){main{padding:22px 16px}.pair{grid-template-columns:1fr}h1{font-size:28px}}</style>
<main><span class="tag">2/2 lượt · Khuyến nghị FAIL · Chờ người dùng xem</span><h1>Kagari — sửa eo và cổ–vai</h1><p>Eo sạch hơn trên ảnh trước/3/4, cổ gáy bớt nhô. Số tam giác giữ nguyên. Vẫn còn giao nhau cục bộ và nếp rủ dưới nách chưa đạt; đây là bản WIP sau hai lượt sửa, chưa được duyệt mỹ thuật.</p>
<p><a href="../../wip/kagari_garment_recovery_v2.blend">Blender v2</a> · <a href="../../wip/kagari_garment_recovery_v1.blend">Lượt 1</a> · <a href="../../wip/kagari_full_concept_v3.blend">Full v3 gốc</a> · <a href="../../reports/garment_recovery_v2/report.md">Báo cáo tiếng Việt</a> · <a href="../../reports/garment_recovery_v2/technical_verification.json">Kiểm tra</a></p>
<div class="note"><strong>Đọc ảnh cùng kiểm tra bề mặt:</strong><p>Không còn các mảng kem cắt vào đai rõ như trước, nhưng kiểm tra tìm thấy 13 đoạn crossing tay áo–đai và 87 đoạn cổ–áo trong pose lưu. Những số này không phải số lỗi độc lập hay diện tích giao nhau. Vai và dưới nách vẫn có khối túi tròn. Tóc lỗi được giữ nguyên theo phạm vi nhiệm vụ.</p></div>
<section><h2>Đối chiếu cùng camera</h2><div class="controls"><label>Ảnh <select id="mode"><option value="color">Màu sẵn có</option><option value="clay">Clay</option></select></label><label>So với <select id="before"><option value="source">Full concept v3</option><option value="iteration1">Recovery lượt 1</option></select></label></div><nav aria-label="Góc nhìn">BUTTONS</nav>
<div class="pair"><figure><img id="old" src="../full_concept_v3/front_existing_color.png" alt="Full v3 trước sửa"><figcaption id="old-caption">Full concept v3 · Trước · pose lưu</figcaption></figure><figure><img id="new" src="front_existing_color.png" alt="Recovery v2 sau sửa"><figcaption id="new-caption">Recovery v2 · Trước · pose lưu</figcaption></figure></div><p>Bấm ảnh để mở PNG gốc. Clay dùng cùng góc nhìn, màu xám và thiết lập studio. Màu dùng lại shader/lighting của source; không thêm vật liệu. Pose nâng tay +30° và tay ngang là pose rig tĩnh, chưa phải mô phỏng vải hay animation.</p></section>
<section><h2>Kết quả và điểm dừng</h2><p>Face/morph, Hair, Body, rig rest và pose lưu khớp sau mở lại; connectivity, UV, weights và modifier của garment được bảo toàn. Bốn garment: 20.105 raw / 41.908 evaluated triangles; object bật render: 47.434 / 118.773, không tăng so với full v3.</p><p>Phương án tạo hình điều khiển và skinning cố định vẫn chưa giải quyết ổn định tiếp giáp cổ–vai, khoảng hở các lớp và độ rủ khi đổi pose. Dừng sau hai lượt, khuyến nghị FAIL cho recovery tổng thể. Không sửa tóc/mặt, không tạo turnaround, không trang trí và không xuất VRM.</p><p class="meta">garment-geometry-recovery-v2 · SHA256: DIGEST</p></section></main>
<script>const labels=LABELS;let view='front';const mode=document.getElementById('mode'),before=document.getElementById('before'),buttons=[...document.querySelectorAll('[data-view]')];const colors=new Set(['front','three_quarter','full_front','portrait']);function refresh(){if(mode.value==='color'&&!colors.has(view))view='front';const suffix=mode.value==='color'?'_existing_color.png':'_clay.png';const root=before.value==='source'?'../full_concept_v3/':'../garment_recovery_v1/';const name=before.value==='source'?'Full concept v3':'Recovery lượt 1';document.getElementById('old').src=root+view+suffix;document.getElementById('new').src=view+suffix;document.getElementById('old-caption').textContent=name+' · '+labels[view];document.getElementById('new-caption').textContent='Recovery v2 · '+labels[view];for(const b of buttons){b.disabled=mode.value==='color'&&!colors.has(b.dataset.view);b.setAttribute('aria-pressed',String(b.dataset.view===view))}}for(const b of buttons)b.addEventListener('click',()=>{view=b.dataset.view;refresh()});mode.addEventListener('change',refresh);before.addEventListener('change',refresh);for(const img of document.querySelectorAll('img'))img.addEventListener('click',()=>window.open(img.src,'_blank','noopener'));refresh();</script></html>'''
page=page.replace('BUTTONS',buttons).replace('LABELS',json.dumps(labels,ensure_ascii=False)).replace('DIGEST',candidate['sha256'])
(P/'review.html').write_text(page,encoding='utf-8')
state_path=ROOT/'config/project_state.json';state=load(state_path)
assert state['current_candidate']['sha256'] in [source['sha256'],candidate['sha256']]
state['previous_candidate']=source;state['comparison_source']=source;state['current_candidate']=candidate
state['current_character_source']=candidate.copy();state['current_gate']='GARMENT_GEOMETRY_RECOVERY_REVIEW_PENDING'
state['current_candidate_role']='FULL_AVATAR_SCOPED_GARMENT_RECOVERY_WIP';state['decision']='REQUIRES_HUMAN_ART_REVIEW'
state['agent_visual_review']=review['agent_visual_review'];state['agent_recommendation']='FAIL'
state['construction_authorization']={'evidence':(R/'user_authorization.md').relative_to(ROOT).as_posix(),'scope':'Waist intersections and collar/shoulder only; maximum two iterations; no face/hair/full-body reconstruction','approval_of_result':False}
state['garment_recovery']={'iterations_completed':2,'iteration_limit':2,'geometry_work_stopped':True,'recommendation':'FAIL','scope_expanded':False,'construction_plan':'outputs/reports/garment_recovery_v1/construction_plan.md'}
state['approvals']['garment_geometry_recovery']={'status':'NOT_APPROVED','evidence':None}
state['blocking_issues']=['Residual sleeve/sash, collar/robe and robe/Body surface crossings in saved pose','Shoulder bulges, underarm bags and frozen drape remain','Inherited scalp/rear-hair defects, outside this task','Human scoped recovery/full-avatar artistic review pending','VRM/runtime/animation readiness not tested']
state['updated_by']='publish_garment_recovery.py; stopped after two user-authorized repair iterations; no aesthetic approval inferred'
state['latest_report']={'path':(R/'report.md').relative_to(ROOT).as_posix(),'sha256':sha(R/'report.md'),'language':'vi','candidate_sha256':candidate['sha256'],'scope':'Two-iteration scoped garment recovery; FAIL recommendation'}
new_paths=[]
for directory in [ROOT/'outputs/reports/garment_recovery_v1',R]:new_paths.extend(p for p in directory.iterdir() if p.suffix in ['.json','.md','.txt'])
for directory in [ROOT/'outputs/previews/garment_recovery_v1',P]:new_paths.extend(p for p in directory.iterdir() if p.suffix in ['.png','.html'])
new_paths.extend([ROOT/v1['candidate']['path'],ROOT/candidate['path'],ROOT/'outputs/backups/garment_recovery_start/kagari_full_concept_v3.blend'])
for p in new_paths:
    rel=p.relative_to(ROOT).as_posix()
    if rel not in state['evidence']:state['evidence'].append(rel)
    state['artifact_records']=[r for r in state['artifact_records'] if r['path']!=rel]+[{'path':rel,'sha256':sha(p)}]
dump(state_path,state)
block={'candidate_path':candidate['path'],'candidate_sha256':candidate['sha256'],'candidate_version':candidate['version'],'decision':state['decision']}
delivery=f'''# Kagari — current garment recovery artifact

**Agent recommendation: FAIL. Human artistic approval: NOT_APPROVED.**
Two controlled waist/collar/shoulder repair iterations are complete and geometry work has stopped.
Waist appearance improves and nape shelf is reduced; residual surface crossings and rounded
shoulder/underarm drape remain. This is a full-avatar WIP with only three garment surfaces edited.

- [Current Blender candidate](wip/kagari_garment_recovery_v2.blend)
- [Gallery: source and iteration1 versus candidate](previews/garment_recovery_v2/review.html)
- [Vietnamese report and explicit failure recommendation](reports/garment_recovery_v2/report.md)
- [Technical checks and bounded intersection probes](reports/garment_recovery_v2/technical_verification.json)
- [Garment metadata and bound-material preservation](reports/garment_recovery_v2/preservation_details.json)
- [Raw/evaluated audit](reports/garment_recovery_v2/geometry_audit.json)
- [Visual findings](reports/garment_recovery_v2/visual_review.json)
- [Scope authorization](reports/garment_recovery_v2/user_authorization.md)
- [Preserved previous full-concept-v3 candidate](wip/kagari_full_concept_v3.blend)
- [Independent source backup](backups/garment_recovery_start/kagari_full_concept_v3.blend)
- [Iteration1 WIP](wip/kagari_garment_recovery_v1.blend)
- [Original Cycle03 baseline](wip/kagari_v03_clay_03.blend)

9 clay and 4 existing-color images per recovery iteration were visually inspected at existing
camera/light settings. Face/morph, Hair, original Body, rig rest and saved pose remain intact.
Untouched mesh data matches; garment connectivity, weights, UV assignments and modifiers match
full v3. 20,105 raw / 41,908 evaluated garment triangles; render-enabled inventory 47,434 /
118,773, unchanged. Viewport counts are not exported VRM/FPS measurements.

Saved pose retains 13 sleeve/sash and 87 collar/robe crossing edge segments in declared probes;
these are not counts of independent faults or an all-pose certificate. No third repair, hair/face
rebuild, ornaments, new materials, Skills expansion, turnaround, VRM or runtime/animation test.

<!-- PROJECT_STATE_BEGIN -->
```json
{json.dumps(block,indent=2)}
```
<!-- PROJECT_STATE_END -->
'''
(ROOT/'outputs/DELIVERY.md').write_text(delivery,encoding='utf-8')
print('GARMENT_RECOVERY_PUBLISHED',candidate['sha256'],'recommendation FAIL')
