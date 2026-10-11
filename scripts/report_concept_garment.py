"""Publish actual render review and synchronize state; never grant art approval."""
import json, hashlib, html
from pathlib import Path
ROOT=Path('D:/Project-17/blender'); REPORT=ROOT/'outputs/reports/concept_garment_v3'; PRE=ROOT/'outputs/previews/concept_garment_v3'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
manifest=read(REPORT/'render_manifest.json'); tech=read(REPORT/'technical_verification.json'); comp=read(REPORT/'comparison_manifest.json')
assert tech['technical_errors']==[] and tech['source_unchanged']
candidate=manifest['candidate']; baseline=manifest['baseline']; prior=manifest['prior_study']
assert sha(ROOT/candidate['path'])==candidate['sha256']
assert sha(ROOT/baseline['path'])==baseline['sha256']
for comparison in comp['comparisons']:
    for a,b in zip(manifest['renders'],comparison['renders']):
        assert all(a[k]==b[k] for k in ['view','camera_location','camera_rotation','ortho_scale','arm_L_euler'])
details=read(REPORT/'detail_manifest.json')
for r in manifest['renders']+details['renders']+[r for c in comp['comparisons'] for r in c['renders']]:
    assert sha(ROOT/r['path'])==r['image_sha256']
raw=sum(o['raw_triangles'] for o in tech['objects'])
evaluated=sum(o['evaluated_triangles'] for o in tech['poses'][0]['objects'])
review={'candidate':candidate,'agent_decision':'IMPROVED_PARTIAL_ACCEPTANCE','human_decision':'NOT_APPROVED',
    'reference':'outputs/design/concept_option2_kagari.jpg','reference_note':'Existing Kagari concept; no new concept image supplied. Front design guides the construction, side/back inferred.',
    'visually_inspected':[r['path'] for r in manifest['renders']+details['renders']]+[r['path'] for c in comp['comparisons'] for r in c['renders']],
    'criteria':{'collar_overlap_thickness':'OBSERVED; broad crossing leaf covers its under-leaf, nape fit remains coarse',
        'shoulder_sleeve_continuity':'IMPROVED_PARTIAL; shared mesh and sloping shoulder, slight cap/neck ridge still visible in profile',
        'wide_sleeve_silhouette':'OBSERVED; long flared hollow sleeve, not short cylindrical sleeve',
        'folds_volume':'PARTIAL; restrained chest folds and sleeve mass, rear and sleeve too smooth',
        'intersection_free':'NOT_CERTIFIED; proximity warning samples remain',
        'moderate_pose':'IMPROVED_PARTIAL; no gross armpit crumpling in front +30 test, only front pose inspected',
        'horizontal_pose':'STRESS_ONLY; volume rotates with skinning and proximity warnings increase',
        'full_concept_outfit':'OUTSIDE_SCOPE; no long outer lapels, obi, second sleeve or lower garment'},
    'top_defects':[
        {'region':'Nape and shoulder cap','evidence':'outputs/previews/concept_garment_v3/three_quarter_detail_clay.png',
            'observation':'Nape lip stands off and shoulder has a broad ridge.', 'cause':'Simplified control curve and shoulder bridge clearances.',
            'future_fix':'Fit nape and yoke cross-sections to neck/shoulder with consistent normal clearance.', 'predicted_effect':'Cleaner neck seating and softer shoulder silhouette.'},
        {'region':'Sleeve lower panel and rear torso','evidence':'outputs/previews/concept_garment_v3/back_clay.png',
            'observation':'Sleeve reads as a smooth flared surface and back has little drape.', 'cause':'Controlled envelope has too few broad tension folds.',
            'future_fix':'Add sparse folds anchored at armhole, lower cuff and waist after form review.', 'predicted_effect':'More readable cloth weight without noise.'},
        {'region':'Raised shoulder clearance','evidence':'outputs/previews/concept_garment_v3/arm_horizontal_clay.png',
            'observation':'Horizontal pose retains a frozen bag orientation; nearest-normal test flags body proximity.', 'cause':'Conventional weights and fixed authored volume.',
            'future_fix':'Inspect posed root close-ups and tune weights/clearance, then evaluate corrective or runtime support separately.', 'predicted_effect':'Safer pose range; no automatic runtime guarantee.'}],
    'raw_garment_triangles':raw,'evaluated_garment_triangles':evaluated,'vrm_export':'NOT_TESTED','runtime':'NOT_TESTED'}
(REPORT/'visual_review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False),encoding='utf-8')
authorization='''# Authorization for concept-directed rebuild

Source: user message in the current chat on 2026-10-11: "hay dung lai theo concept moi".

Context: user chose rebuilding the collar/shoulder/sleeve pattern from the Kagari concept rather than pausing for a specialist garment tool survey. This authorizes the limited new geometry experiment on a duplicate mannequin, not approval of any resulting artifact. The prior scope excludes ornamentation, production materials, a full character rebuild and final VRM export. Skills development remains paused. No new concept image was attached; the active project reference is concept_option2_kagari.jpg.
'''
(REPORT/'user_authorization.md').write_text(authorization,encoding='utf-8')
report=f'''# Kagari — dựng lại form theo concept

**Đánh giá agent: CẢI THIỆN, ĐẠT MỘT PHẦN. Chưa được người dùng duyệt.** Không tuyên bố đạt toàn bộ Clay Gate.

## Mẫu và phạm vi

Dùng [concept Kagari hiện có](../../design/concept_option2_kagari.jpg), không có hình concept mới được đính kèm. Các dấu hiệu được quan sát trực tiếp: bản cổ chéo rộng, vai xuôi, tay áo dài loe, eo gọn và nếp vải lớn có tiết chế. Mặt sau và cấu trúc đường may là phần suy diễn. Đây là mẫu một cổ áo, một tay áo và thân hỗ trợ trên mannequin; chưa tái tạo toàn bộ lớp áo khoác, hai tay áo, đai và phần dưới của concept.

Mẫu đã lưu: [kagari_concept_garment_v3.blend](../../wip/kagari_concept_garment_v3.blend). Version `{candidate['version']}`; SHA256 `{candidate['sha256']}`.

## Phương pháp đã thực hiện

Dựng các bề mặt vải mới bằng lưới có tham số, dựa trên đường nét concept và vai của mannequin. Không tái sử dụng mesh áo Cycle 03 hoặc mesh Cloth cũ, không chạy Cloth ở lần này. Hai thân trước chồng lên nhau; cổ chạy theo mép thân, lớp trái phủ trên lớp phải và nối qua gáy bằng chung đỉnh. Phần cổ dưới kết thúc trong vùng được thân trên che phủ, tránh chữ X lộ ra dưới ngực. Vai nối qua các hàng đỉnh tương ứng; gốc tay áo dùng chung đỉnh với thân. Tay áo gồm hai mảnh dài, mặt nối trên/dưới bo cong và cửa tay rỗng rộng.

Mannequin lấy bản sao từ study trước; tư thế dựng hạ hai tay 60° so với phương ngang. Chuyển bề mặt đã dựng về rest space bằng nghịch đảo skinning; gắn xương chest/upperChest/shoulder/upperArm/lowerArm với tối đa bốn ảnh hưởng mỗi đỉnh. Solidify dày 1,5 mm thân/tay và 1,8 mm cổ. Macro folds đặt theo vùng eo, nách và cuff; chưa có mô phỏng trọng lực hay xác nhận pattern may mặc 2D.

Kagari gốc giữ nguyên SHA `{baseline['sha256']}`. Mẫu panel cũ cũng giữ nguyên. Không sửa Skills, Face, Hair, morphs hoặc rig gốc; không cài phần mềm, thêm ornament, màu burgundy/cream hay shader trang trí.

## Render và so sánh

Đã nhìn trực tiếp sáu ảnh toàn cảnh: trước, 3/4, nghiêng, sau, nâng tay thêm 30° (còn 30° dưới phương ngang) và stress thêm 60° (tay ngang). Có hai ảnh cận cổ/vai bổ sung, không thay thế ảnh toàn cảnh. Pose dùng Armature thuần, không Cloth hoặc corrective morph. Đã xem các ảnh đối chiếu của Cycle 03 và study panel cũ.

Camera, ánh sáng clay, mannequin và tư thế trong [comparison_manifest.json](comparison_manifest.json) khớp chính xác với bản mới. Study panel cũ vốn dựng ở tư thế tay hạ 30°; render so sánh này cho thấy nó biến dạng ở pose hạ 60°, không thay thế những ảnh neutral gốc của nó. Cycle 03 có hai tay áo và đai, mẫu mới chỉ một tay áo; không so số polygon như cùng phạm vi.

| Phần | Cycle 03 / study panel cũ | Mẫu theo concept |
|---|---|---|
| Cổ | Giao cổ bị nhăn / bản cổ hẹp, vai cao | Cổ rộng cong, một đường chéo che lớp dưới; gáy còn bật |
| Vai | Hở gốc tay / tấm ngang cao | Vai xuôi và mesh nối liên tục; profile còn gợn rộng |
| Tay áo | Ống ngắn / túi ngắn bị nhăn | Tay dài loe, cửa tay rỗng rõ ở 3/4; mặt còn trơn |
| Thân trước | Khối đều / nếp crumple dồn ở root | Thân thoáng hơn, eo gọn, nếp lớn gần eo |
| Mặt sau | Phẳng / nhăn bất đối xứng | Form sạch hơn nhưng vẫn thiếu độ rủ |
| Nâng 30° | Gốc rời / nách gãy nhiều | Không có nếp gãy lớn ở front render; chưa chứng nhận mọi pose |

## Khuyết điểm còn lại

1. **Cổ sau/vai:** ảnh cận 3/4 và nghiêng cho thấy mép gáy bật khỏi cổ và yoke còn có một gờ rộng. Curve/clearance đang đơn giản; cần fit lại mặt cắt sau khi người dùng duyệt hướng form.
2. **Độ rủ:** silhouette tay rộng hơn rõ, nhưng tay và lưng còn giống bề mặt sạch có form hơn là vải có trọng lượng. Cần vài nếp lớn có điểm neo; không tăng chi tiết đồng loạt.
3. **Clearance và rig:** phép nearest-normal trên mannequin cắt có dấu hiệu rủi ro: thân/cổ lần lượt 3/2 mẫu ở neutral, 0/2 ở nâng 30°, 18/1 ở tay ngang. Đây không phải phép kiểm chứng giao mesh đầy đủ, cũng không phải số lỗ xuyên được xác nhận. Chưa được ghi INTERSECTION_FREE. Túi tay xoay theo xương, không tiếp tục rủ theo trọng lực thế giới.

Vùng bụng dưới và cổ mannequin có biên cắt chẩn đoán; đó không phải hình học avatar hoàn chỉnh. Bên không dựng tay áo cố ý để trống.

## Mesh và kiểm tra thật

| Thành phần | Tam giác raw | Tam giác sau modifier viewport |
|---|---:|---:|
| Thân + một tay áo | 8.507 | 17.516 |
| Cổ chéo liên tục | 1.152 | 2.712 |
| Tổng trang phục | {raw:,} | {evaluated:,} |
| Scene mannequin | 16.567 | 27.136 |

Hai surface riêng đều một thành phần liên thông, không có face diện tích bằng không hoặc cạnh non-manifold bên trong. Biên mở raw tại neckline, hem, cửa tay là có chủ đích trước Solidify. Weight chuẩn hóa, không thiếu weight, không quá bốn bone; tọa độ sau modifier hữu hạn trong ba pose. Không có subdivision hay Cloth modifier. So với study cũ (6.736 raw / 14.260 evaluated), bản mới tăng mesh để có tay dài và bề mặt nối được kiểm soát; không phải tối ưu runtime.

[Kiểm tra kỹ thuật](technical_verification.json), [audit thật](geometry_audit.json), [render manifest](render_manifest.json), [đánh giá hình ảnh](visual_review.json), [kế hoạch trước mesh](../concept_garment_v1/construction_plan.md).

## Các lượt dựng và giới hạn

Ba candidate mới được giữ riêng. v1 lộ form ngực quá sát, cổ đọc thành X và vai gợn; v2 sửa lớp phủ, bề mặt thân và thứ tự hàng vai nhưng tay quá hẹp khi nhìn trước; v3 mở phần vải dưới tay, mở rộng cổ và thêm hai nếp lớn gần eo. Đây là phương pháp bề mặt điều khiển theo concept, khác các thử nghiệm Cloth trước. Dừng sau v3 để người dùng đánh giá.

VRM export/reimport, Warudo, webcam, OBS và FPS đều NOT_TESTED. Study không phải avatar VRM đầy đủ; chưa có UV/material production, form vải động, pose-corrective hoặc chứng nhận góc xoay rộng. Mặt/người/hair gốc được bảo toàn bằng giữ nguyên source, chưa ghép study vào Kagari.

**REQUIRES_HUMAN_ART_REVIEW.** Trang phục chưa duyệt; không chuyển sang trang trí/materials hoặc tích hợp avatar trong lượt này.
'''
(REPORT/'report.md').write_text(report,encoding='utf-8')
page='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kagari · Form theo concept</title>
<style>*{box-sizing:border-box}body{margin:0;background:#171719;color:#efede8;font:16px/1.5 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:32px 24px 64px}h1{font-size:34px;line-height:1.2;margin:12px 0}h2{font-size:22px;margin:32px 0 12px}p{max-width:900px;color:#c4c1bb}a{color:#dfbb88}.badge{display:inline-block;background:#493c25;color:#f1cf93;padding:5px 12px;border-radius:20px;font-size:13px}.hero{display:grid;grid-template-columns:1fr 1.25fr;gap:18px}.hero img{width:100%;height:560px;object-fit:contain;background:#29292b;border-radius:8px}.hero figure{margin:0}.hero figcaption{padding:10px 0;color:#ccc}.bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}button{font:inherit;background:#29292e;color:#ddd;border:1px solid #525257;padding:8px 16px;border-radius:8px;cursor:pointer}button[aria-pressed=true]{background:#e4c99e;color:#23201a;border-color:#e4c99e}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:#262628;border:1px solid #3c3c40;border-radius:10px;overflow:hidden}.card img{display:block;width:100%;aspect-ratio:1;object-fit:contain}.card h3{font-size:16px;margin:14px}.card p{font-size:14px;margin:14px}.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.notes section{padding:18px;background:#252527;border-radius:10px}.notes h3{margin-top:0;font-size:17px}.notes p{font-size:15px;margin-bottom:0}.detail{display:grid;grid-template-columns:1fr 1fr;gap:16px}.detail img{width:100%;border-radius:8px}.muted{font-size:14px;color:#aaa}summary{cursor:pointer}details{margin-top:30px;padding:18px;border:1px solid #444;border-radius:10px}code{overflow-wrap:anywhere;font-size:13px}@media(max-width:850px){.hero,.compare,.notes{grid-template-columns:1fr}.hero img{height:440px}.detail{grid-template-columns:1fr}h1{font-size:28px}}
</style><main><span class="badge">Mẫu clay · Chờ duyệt form</span><h1>Kagari — dựng lại theo concept</h1><p>Một cổ áo, một tay áo dài loe và phần thân nối trên mannequin riêng. Cổ chéo rộng hơn, vai xuôi và thân trước thoáng hơn. Bản này chưa đạt toàn bộ kiểm tra và chưa ghép vào Kagari.</p>
<div class="hero"><figure><img src="../../design/concept_option2_kagari.jpg" alt="Concept Kagari hiện có"><figcaption>Concept Kagari hiện có · chỉ có góc trước</figcaption></figure><figure><img src="front_clay.png" alt="Mẫu clay mới dựng theo concept"><figcaption>Bản theo concept v3 · neutral clay · một tay áo</figcaption></figure></div>
<h2>So sánh cùng góc nhìn và tư thế</h2><p class="muted">Study panel trước được dựng với tay hạ 30°; các ảnh dưới đặt nó ở pose hạ 60° để so sánh với mẫu mới. Cycle 03 có hai tay áo và đai, mẫu mới chỉ một tay áo.</p>
<div class="bar">BUTTONS</div><div class="compare"><article class="card"><h3>Cycle 03 · baseline chưa duyệt</h3><img id="cycle03" src="cycle03_front_clay.png" alt="Cycle 03 cùng góc nhìn"><p>Tay áo ngắn, gốc vai rời, cổ bị nhăn.</p></article><article class="card"><h3>Study panel + Cloth trước</h3><img id="prior_panel" src="prior_panel_front_clay.png" alt="Study panel trước cùng góc nhìn"><p>Vai cao và nếp vải dồn ở nách.</p></article><article class="card"><h3>Form theo concept · v3</h3><img id="new" src="front_clay.png" alt="Mẫu theo concept cùng góc nhìn"><p>Cổ chéo rộng, tay dài loe; còn lỗi gáy và độ rủ.</p></article></div>
<h2>Cận cổ và vai</h2><div class="detail"><img src="front_detail_clay.png" alt="Cận cổ chính diện"><img src="three_quarter_detail_clay.png" alt="Cận cổ và vai góc ba phần tư"></div>
<h2>Những điểm cần đánh giá tiếp</h2><div class="notes"><section><h3>Cổ sau và vai</h3><p>Mép gáy hơi bật, yoke còn gờ rộng. Cổ chéo trước đã có lớp phủ rõ.</p></section><section><h3>Độ rủ</h3><p>Tay dài và rộng hơn, nhưng mặt tay và lưng còn trơn. Chưa tái tạo đầy đủ lớp áo khoác trong concept.</p></section><section><h3>Pose và clearance</h3><p>Nâng tay 30° bớt gãy nách. Giơ ngang vẫn cần kiểm tra sát cơ thể; chưa chứng nhận không xuyên mesh hoặc hoạt động trong VRM.</p></section></div>
<p class="muted">Phần bụng và cổ mannequin có biên cắt chẩn đoán. Bên chưa dựng tay áo cố ý để trống. Chưa thêm màu, họa tiết, phụ kiện hoặc đai.</p>
<p><a href="../../reports/concept_garment_v3/report.md">Báo cáo đầy đủ</a> · <a href="../../wip/kagari_concept_garment_v3.blend">File Blender mới</a></p>
<details><summary>Phiên bản và dữ liệu kiểm tra</summary><p>VERSION<br><code>DIGEST</code></p><p>9.659 tam giác raw · 20.228 sau modifier cho trang phục. Hai surface liên thông, weight chuẩn hóa; kiểm tra hình học không phải duyệt thẩm mỹ.</p><p><a href="../../reports/concept_garment_v3/technical_verification.json">Kiểm tra mesh và pose</a> · <a href="../../reports/concept_garment_v3/render_manifest.json">Render manifest</a></p></details></main>
<script>document.querySelectorAll('button[data-view]').forEach(b=>b.addEventListener('click',()=>{let v=b.dataset.view;document.querySelectorAll('button[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.getElementById('cycle03').src='cycle03_'+v+'_clay.png';document.getElementById('prior_panel').src='prior_panel_'+v+'_clay.png';document.getElementById('new').src=v+'_clay.png';}));</script></html>'''
labels={'front':'Trước','three_quarter':'3/4','side':'Nghiêng','back':'Sau','arm_raised':'Nâng 30°','arm_horizontal':'Tay ngang · stress'}
buttons=''.join(f'<button data-view="{n}" aria-pressed="{str(n=="front").lower()}">{html.escape(label)}</button>' for n,label in labels.items())
page=page.replace('BUTTONS',buttons).replace('VERSION',candidate['version']).replace('DIGEST',candidate['sha256'])
(PRE/'review.html').write_text(page,encoding='utf-8')
state=read(ROOT/'config/project_state.json')
state['current_candidate']=candidate; state['current_gate']='CONCEPT_GARMENT_CLAY_REVIEW_PENDING'
state['current_candidate_role']='ISOLATED_CONCEPT_DIRECTED_GARMENT_STUDY_NOT_FULL_AVATAR'
state['decision']='REQUIRES_HUMAN_ART_REVIEW'; state['agent_visual_review']='IMPROVED_PARTIAL_ACCEPTANCE'
state['previous_candidate']=prior
state['construction_authorization']={'evidence':'outputs/reports/concept_garment_v3/user_authorization.md','scope':'Concept-directed collar, one sleeve and shoulder/torso rebuild on duplicate mannequin','approval_of_result':False}
state['blocking_issues']=['Human concept-directed garment form approval pending','Nape/yoke fit and cloth fold volume remain incomplete','Body proximity warnings; no intersection-free or all-pose certificate','No VRM export/reimport or runtime verification']
state['updated_by']='report_concept_garment.py; user authorized rebuild, no human artifact approval inferred'
paths=[str(p.relative_to(ROOT)).replace('\\','/') for p in [REPORT/'report.md',REPORT/'visual_review.json',REPORT/'technical_verification.json',REPORT/'geometry_audit.json',REPORT/'render_manifest.json',REPORT/'comparison_manifest.json',REPORT/'detail_manifest.json',REPORT/'panel_seams.json',REPORT/'user_authorization.md',PRE/'review.html',ROOT/'outputs/reports/concept_garment_v1/construction_plan.md']]
paths+=[r['path'] for r in manifest['renders']+details['renders']]+[r['path'] for c in comp['comparisons'] for r in c['renders']]
paths+=['outputs/wip/kagari_concept_garment_v1.blend','outputs/wip/kagari_concept_garment_v2.blend']
for p in paths:
    if p not in state['evidence']: state['evidence'].append(p)
    state['artifact_records']=[r for r in state['artifact_records'] if r['path']!=p]+[{'path':p,'sha256':sha(ROOT/p)}]
(ROOT/'config/project_state.json').write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
block={'candidate_path':candidate['path'],'candidate_sha256':candidate['sha256'],'candidate_version':candidate['version'],'decision':state['decision']}
delivery='# Kagari — concept-directed garment study\n\n<!-- PROJECT_STATE_BEGIN -->\n```json\n'+json.dumps(block,indent=2)+'\n```\n<!-- PROJECT_STATE_END -->\n\n'
delivery+='**REQUIRES_HUMAN_ART_REVIEW. Agent: IMPROVED_PARTIAL_ACCEPTANCE. Human garment approval: NOT_APPROVED.**\n\n'
delivery+='New controlled sheet construction guided by the existing Kagari concept: wide crossed collar, sloping shoulder and one long flared hollow sleeve on a duplicate mannequin. Neutral clay only; no Cloth simulation, decoration, production materials, Skills changes or final export. Original character source and previous study hashes unchanged.\n\n'
delivery+='Observed improvements: visible crossover, long sleeve silhouette and fewer sharp armpit folds in the moderate front pose. Remaining: nape/yoke fit, overly smooth sleeve/back and body-proximity warnings. This is a limited study, not the complete layered outfit from the concept.\n\n'
delivery+='- [Current study](wip/kagari_concept_garment_v3.blend) — SHA256 `'+candidate['sha256']+'`\n'
delivery+='- [Unchanged Cycle 03 baseline](wip/kagari_v03_clay_03.blend) — SHA256 `'+baseline['sha256']+'`\n'
delivery+='- [Previous panel study](wip/kagari_panel_drape_reset_final.blend) — SHA256 `'+prior['sha256']+'`\n'
delivery+='- [Review gallery](previews/concept_garment_v3/review.html)\n- [Report](reports/concept_garment_v3/report.md)\n- [Technical verification](reports/concept_garment_v3/technical_verification.json)\n- [Render manifest](reports/concept_garment_v3/render_manifest.json)\n- [User rebuild authorization](reports/concept_garment_v3/user_authorization.md)\n\n'
delivery+='Garment only: 9,659 raw / 20,228 viewport-evaluated triangles. Both surfaces connected individually; weights normalized, at most four bones; three poses finite. Proximity checks are not a robust intersection certificate. VRM, Warudo, webcam, OBS and FPS NOT_TESTED. Stop for human review; Skills development remains paused.\n'
(ROOT/'outputs/DELIVERY.md').write_text(delivery,encoding='utf-8')
print('CONCEPT_REVIEW_PUBLISHED',candidate['sha256'],raw,evaluated)
