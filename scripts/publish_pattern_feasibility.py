"""Publish reviewed experiment, provenance and state without unlocking art gates."""
import json,hashlib,math,html,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'outputs/reports/pattern_feasibility';PRE=ROOT/'outputs/previews/pattern_feasibility'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
mans={}
for tag in ['trial1','trial2','trial3']:
    p=REPORT/tag/'render_manifest.json';m=read(p)
    # Normalize exact camera/pose metadata from the explicitly executed pose
    # sequence. Original row objects contained unrelated Recovery pose fields.
    for r in m['renders']:
        r['camera']={k:r['camera'][k] for k in ['camera_location','camera_rotation','ortho_scale']}
        r['upper_arm_pose']={'L':[0,0,math.radians({'neutral':-68,'raised30':-38,'horizontal':0}[r['pose']])],'R':[0,0,math.radians(68)]}
    dump(p,m);mans[tag]=m
comp=read(REPORT/'comparison_manifest.json')
for r in comp['renders']:
    r['camera']={k:r['camera'][k] for k in ['camera_location','camera_rotation','ortho_scale']}
    r['upper_arm_pose']={'L':[0,0,math.radians({'neutral':-68,'raised30':-38,'horizontal':0}[r['pose']])],'R':[0,0,math.radians(68)]}
    r['comparison_context']='Recovery v2 garment copy, cropped only for matched mannequin comparison'
    r['reference_prototype_sha256']=comp['prototype_sha256']
    r['artifact_sha256']=comp['source_sha256']
dump(REPORT/'comparison_manifest.json',comp)
man=mans['trial3'];candidate=man['candidate'];source={**man['source_character'],'version':'garment-geometry-recovery-v2'};verification=read(REPORT/'trial3/technical_verification.json');audit=read(REPORT/'trial3/geometry_audit.json')
sources=[]
for path,expected in [('outputs/wip/kagari_garment_recovery_v2.blend',source['sha256']),('outputs/backups/pattern_feasibility_start/kagari_garment_recovery_v2.blend',source['sha256']),('outputs/wip/kagari_full_concept_v3.blend','ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16'),('outputs/wip/kagari_v03_clay_03.blend','4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051')]:
    actual=sha(ROOT/path);assert actual==expected;sources.append({'path':path,'sha256':actual,'matches_expected':True})
dump(REPORT/'source_preservation.json',{'result':'PASS_BYTE_HASH_PRESERVATION','files':sources,'geometry_foundation':'Only Body_GarmentDisplay and Armature copied into generator; no source garment objects loaded by build script. Old garment objects are loaded exclusively by separate comparison script.'})
dump(REPORT/'visual_review.json',{'candidate':candidate,'recommendation':'ABANDON','recommendation_scope':'Current fully automated cut/constraint configuration, not all pattern-based modeling','human_verdict':'NOT_APPROVED','inspection':'All 14 final trial3 PNGs and all 12 matched Recovery v2 comparison PNGs visually inspected; trial1 and trial2 inspected in representative front/3q/side/back/stress images, not asserted as complete 14-image visual reviews.','criteria':{'silhouette':0,'collar':0,'shoulder_sleeve':0,'folds':1,'deformation':0,'hair_face_full_identity':'NOT_OBSERVABLE_LIMITED_MANNEQUIN_STUDY'},'issues':[{'region':'collar/front support','evidence':['outputs/previews/pattern_feasibility/trial3/neutral_front_clay.png','outputs/previews/pattern_feasibility/trial3/raised30_front_clay.png'],'observation':'Wide opening exposes the underlying mannequin torso; overlap collapses into thin pointed crossing strips. Under leaf wrinkles severely during raising.','cause_hypothesis':'Front cut ease/overlap and sparse hem constraints do not fit the body; band inherits the failed drape. Post-drape finishing band is not independently sewn/simulated.','future_change':'Fit a measured front neckline/overlap cut with controlled collar width before solving; test band as an actual sewn component.','predicted_effect':'A broad stable crossover with supported outer band, instead of a pointed lower X. Not implemented.'},{'region':'shoulder/underarm/back','evidence':['outputs/previews/pattern_feasibility/trial3/neutral_side_clay.png','outputs/previews/pattern_feasibility/trial3/neutral_back_clay.png','outputs/previews/pattern_feasibility/trial3/horizontal_side_clay.png'],'observation':'Crushed angular seam folds, discontinuous-looking shoulder contact and visible body exposure in stress view.','cause_hypothesis':'Panel rest lengths/placement/anchor tensions conflict; residual sewing gaps are force-welded after solve.','future_change':'Human-fit the shoulder/armhole cut and seam rest-length pairing, consider a small gusset, validate sew closure before freezing.','predicted_effect':'Smoother contact and distributed tension. Not implemented.'},{'region':'wide sleeve / rig-only stress','evidence':['outputs/previews/pattern_feasibility/trial3/neutral_front_clay.png','outputs/previews/pattern_feasibility/trial3/horizontal_front_clay.png','outputs/previews/pattern_feasibility/trial3/rig_only_horizontal_front_clay.png'],'observation':'Gravity bag is readable in raised/horizontal solve but narrow/crumpled in neutral. Rig-only horizontal raise leaves arm above/through the upper cloth edge.','cause_hypothesis':'Cut/initial placement/support constraints do not preserve intended neutral silhouette; heuristic skinning cannot reproduce pose-specific gravity/contact.','future_change':'Re-establish the sleeve cut after human art review; separately author armhole weights, accepted pose correctives and secondary controls.','predicted_effect':'Preserved sleeve bag plus pose-safe upper edge. Not implemented.'}]})
# Vector evidence from the actual metric pattern arrays; no render is repainted.
patterns=read(REPORT/'trial3/patterns_and_seams.json');svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 740"><rect width="1300" height="740" fill="#f4f1eb"/><g font-family="sans-serif" fill="#192b30"><text x="30" y="32" font-size="22">Actual metric cuts — trial3 (diagnostic, rejected fit)</text>']
for num,(name,pat) in enumerate(patterns['pieces'].items()):
    grid=pat['metric_2d_m'];qs=[q for row in grid for q in row];mn=min(q[0] for q in qs);mx=max(q[0] for q in qs);my=max(q[1] for q in qs);x0=40+(num%3)*430;y0=90+(num//3)*310
    def point(q):return f'{x0+(q[0]-mn)*650:.1f},{y0+q[1]*650:.1f}'
    outline=grid[0]+[r[-1] for r in grid[1:]]+list(reversed(grid[-1][:-1]))+[r[0] for r in reversed(grid[1:-1])]
    svg.append(f'<text x="{x0}" y="{y0-24}" font-size="18">{html.escape(name)} — {(mx-mn)*1000:.0f} × {my*1000:.0f} mm bounds</text><polygon points="'+ ' '.join(point(q) for q in outline)+'" fill="#d9e2e0" stroke="#1e5960" stroke-width="2"/>')
    for row in grid[::3]:svg.append('<polyline points="'+' '.join(point(q) for q in row)+'" fill="none" stroke="#8aa4a6" stroke-width=".6"/>')
svg.append('<text x="30" y="725" font-size="15">Cut extents are not approved tailoring dimensions. Collar finishing band is generated after drape; see script and report.</text></g></svg>')
(PRE/'metric_patterns.svg').write_text(''.join(svg),encoding='utf8')
# Offline human review: same image scale and a clearly separate rig-only view.
gallery='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kagari — Pattern feasibility</title><style>body{font:16px system-ui;background:#181b20;color:#e7e9ed;margin:24px auto;max-width:1400px;padding:0 16px}h1{font-size:28px}p{max-width:1000px;line-height:1.5}.fail{color:#ffb4a9}select,button{font:inherit;padding:8px;background:#2c323d;color:white;border:1px solid #555;border-radius:6px;margin:6px}label{display:inline-block}a{color:#9fd0ff}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}img{width:100%;display:block}figcaption{padding:10px;background:#282d36}#modeNote{padding:12px;background:#2b303b}details{margin:20px 0}#pattern{background:#f4f1eb}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><h1>Kagari — thử nghiệm dựng từ rập</h1><p class="fail"><b>FAIL về mỹ thuật. Khuyến nghị: ABANDON cấu hình tự động này. Chưa được người dùng duyệt.</b></p><p>Sewing constraints và mô phỏng đã chạy thật, nhưng cổ–vai nhăn vỡ, tay áo không giữ silhouette ở neutral. Không tích hợp vào model đầy đủ. Cả hai bên dùng cùng mannequin, góc máy, gray clay và ánh sáng.</p><label>Cấu hình <select id="trial"><option value="trial3">Trial 3 — cuối, không duyệt</option><option value="trial2">Trial 2 — không duyệt</option><option value="trial1">Trial 1 — không duyệt</option></select></label><label>Pose <select id="pose"><option value="neutral">Neutral: upper arm −68°</option><option value="raised30">Giơ thêm 30°: −38°</option><option value="horizontal">Ngang: 0°</option></select></label><label>Góc <select id="view"><option value="front">Trước</option><option value="three_quarter">3/4</option><option value="side">Nghiêng</option><option value="back">Sau</option></select></label><label>Biến dạng <select id="mode"><option value="simulation">Kết quả cloth tại pose</option><option value="rig_only">Chỉ skinning — stress phía trước</option></select></label><p id="modeNote"></p><div class="pair"><figure><a id="baseLink"><img id="base" alt="Recovery v2 đối chiếu"></a><figcaption>Recovery v2 — bản sao cắt phạm vi, chỉ armature</figcaption></figure><figure><a id="studyLink"><img id="study" alt="Mẫu từ rập"></a><figcaption id="caption"></figcaption></figure></div><p>Phần tay áo đối diện và mép dưới baseline được cắt trong bản sao để khớp phạm vi. Không chấm các biên cắt đó. Prototype chỉ có một tay áo; mannequin có cổ/thân đã cắt và đầu trơn. Cổ finishing band được tạo sau solve, không có solve vải riêng. Mesh đóng băng dùng weld cạnh may; weld không chứng minh sewing hội tụ.</p><details><summary>Rập 2D thực tế</summary><img id="pattern" src="metric_patterns.svg" alt="Rập metric của thử nghiệm"></details><p><a href="../../reports/pattern_feasibility/report.md">Báo cáo, số liệu và thiếu sót</a> · <a href="../../reports/pattern_feasibility/strategy_comparison.md">Bốn phương án</a> · <a href="../../reports/pattern_feasibility/production_integration.md">Retopo / rig / VRM</a> · <a href="../garment_recovery_v2/review.html">Gallery Recovery v2 gốc</a></p><script>const trial=document.getElementById('trial'),pose=document.getElementById('pose'),view=document.getElementById('view'),mode=document.getElementById('mode');function show(){if(mode.value==='rig_only'){if(pose.value==='neutral')pose.value='raised30';view.value='front';view.disabled=true}else view.disabled=false;let p=pose.value,v=view.value,t=trial.value,m=mode.value;let a='comparison/recovery2_'+p+'_'+v+'_clay.png';let b=t+'/'+(m==='rig_only'?'rig_only_'+p+'_front_clay.png':p+'_'+v+'_clay.png');document.getElementById('base').src=a;document.getElementById('baseLink').href=a;document.getElementById('study').src=b;document.getElementById('studyLink').href=b;document.getElementById('caption').textContent=t+' — '+(m==='rig_only'?'chỉ armature, không cloth/correctives':'snapshot cloth tại đúng pose');document.getElementById('modeNote').textContent=m==='rig_only'?'Đây là kiểm tra rig thực: biến dạng từ neutral đã đóng băng. Cánh tay xuyên mép vải vẫn là lỗi.':'Đây là hình học đã mô phỏng riêng ở từng pose; không phải khả năng tự động của mesh skinned hay VRM.'}for(const e of [trial,pose,view,mode])e.addEventListener('change',show);show();</script></html>'''
(PRE/'review.html').write_text(gallery,encoding='utf8')
# Counts compare declared scopes; lower clothes and opposite sleeve excluded.
garment=[r for r in verification['meshes'] if r['object'] in ['Simulated_neutral','Collar_neutral']]
dump(REPORT/'geometry_comparison.json',{'study_neutral_only':{'raw_triangles':sum(r['raw_triangles'] for r in garment),'evaluated_triangles':sum(r['evaluated_triangles'] for r in garment),'meshes':garment},'recovery2_matched_crop':comp['crop_records'],'scope_warning':'Cut shapes and hem heights differ. Counts do not prove quality or represent full-avatar VRM/FPS. Stored snapshots, archives and 2D pattern collection are excluded from the study-neutral total.'})
# Project state publication is intentionally done after the final report exists.
if not (REPORT/'report.md').exists():
    print('GALLERY_AND_EVIDENCE_PUBLISHED_REPORT_PENDING');raise SystemExit(0)
state=read(ROOT/'config/project_state.json')
state['previous_candidate']=source;state['comparison_source']=source
state['current_candidate']=candidate;state['current_character_source']={**source,'role':'PRESERVED_FULL_AVATAR_FAILED_GARMENT_BASELINE'}
state['current_gate']='PATTERN_GARMENT_FEASIBILITY_HUMAN_REVIEW_PENDING';state['current_candidate_role']='ISOLATED_MANNEQUIN_GARMENT_EXPERIMENT'
state['decision']='REQUIRES_HUMAN_ART_REVIEW';state['agent_recommendation']='ABANDON';state['agent_visual_review']='FAILED_VISIBLE_IMPROVEMENT_TEST'
state['pattern_feasibility']={'configurations_completed':3,'modeling_stopped':True,'recommendation':'ABANDON','scope':'Current fully automated panel/sewing configuration only','full_character_reconstruction':False,'source_setup':man['source_setup'],'render_manifest':'outputs/reports/pattern_feasibility/trial3/render_manifest.json','human_approval':'NOT_APPROVED'}
state['approvals']['pattern_garment_prototype']={'status':'NOT_APPROVED'}
state['latest_report']={'path':'outputs/reports/pattern_feasibility/report.md','sha256':sha(REPORT/'report.md'),'language':'vi','candidate_sha256':candidate['sha256'],'scope':'Pattern sewing feasibility, isolated upper mannequin; failed art; abandon current automatic setup'}
state['updated_by']='publish_pattern_feasibility.py; limited study stopped after three configurations; human art approval absent'
state['preserved_full_avatar_body_render_surface']=state.get('preserved_full_avatar_body_render_surface',state.get('body_render_surface'))
state['body_render_surface']={'active':'Pattern_Duplicate_Upper_Mannequin','role':'Cropped duplicate in experimental scene only','full_avatar_source_body':'Body_GarmentDisplay','source_data_intact':True}
state['blocking_issues']=['Pattern prototype failed collar overlap, shoulder continuity and neutral sleeve silhouette','Sewing gaps remain before welding; physical convergence not certified','Ordinary armature-only stress fails; simulated snapshots do not establish VRM deformation','Full avatar Recovery v2 remains failed and unchanged','Human artistic approval absent; export/runtime remain untested']
state['construction_authorization']={'evidence':'outputs/reports/pattern_feasibility/user_request.md','source':'Latest human task: Pattern-Based Garment Modeling Feasibility Study','scope':'Copied upper mannequin, one collar, one sleeve and shoulder connection; research, renders, audit and report only','full_character':False,'software_install':False,'stop_for_human_art_review':True}
files=list(REPORT.rglob('*'))+list(PRE.rglob('*'))
files += [ROOT/mans[t]['candidate']['path'] for t in mans]+[ROOT/mans[t]['source_setup']['path'] for t in mans]
files += [ROOT/'scripts'/n for n in ['build_pattern_feasibility.py','render_pattern_comparison.py','verify_pattern_feasibility.py','publish_pattern_feasibility.py','inspect_pattern_source.py','inspect_pattern_render_settings.py']]
files += list((ROOT/'outputs/backups/pattern_feasibility_start').glob('*'))
records={r['path']:r for r in state.get('artifact_records',[])}
evidence=set(state.get('evidence',[]))
for p in files:
    if not p.is_file() or p.suffix=='.log':continue
    rel=p.relative_to(ROOT).as_posix();records[rel]={'path':rel,'sha256':sha(p)};evidence.add(rel)
state['artifact_records']=list(records.values());state['evidence']=sorted(evidence)
dump(ROOT/'config/project_state.json',state)
block={'candidate_path':candidate['path'],'candidate_sha256':candidate['sha256'],'candidate_version':candidate['version'],'decision':state['decision']}
delivery=f'''# Kagari — pattern garment feasibility experiment

**Artistic result: FAIL. Recommendation: ABANDON the current automated cut/sewing setup. Human approval: NOT_APPROVED.**

Three isolated configurations complete. True sewing constraints and cloth pose snapshots are available, but collar overlap/shoulder folds and neutral sleeve silhouette fail. Ordinary rig-only stress also fails. This is an isolated upper-mannequin study, not a new full Kagari model. No installation, external mesh, decoration or VRM export.

- [Review gallery: matched Recovery v2, all poses and rig-only diagnostic](previews/pattern_feasibility/review.html)
- [Report and explicit shortcomings](reports/pattern_feasibility/report.md)
- [Final experiment Blender](wip/kagari_pattern_trial3_prototype.blend)
- [Editable sewing/pattern source scene](wip/kagari_pattern_trial3_source.blend)
- [Strategy comparison and sources](reports/pattern_feasibility/strategy_comparison.md)
- [Integration requirements](reports/pattern_feasibility/production_integration.md)
- [Geometry and modifier audit](reports/pattern_feasibility/trial3/geometry_audit.json)
- [Technical verification](reports/pattern_feasibility/trial3/technical_verification.json)
- [Source preservation](reports/pattern_feasibility/source_preservation.json)
- [Render evidence](reports/pattern_feasibility/trial3/render_manifest.json)
- [Preserved full-avatar Recovery v2](wip/kagari_garment_recovery_v2.blend)
- [Independent source backup](backups/pattern_feasibility_start/kagari_garment_recovery_v2.blend)

Current full-character source remains Recovery v2; latest candidate is an experimental mannequin. Final prototype garment only: 4,944 raw / 10,484 evaluated triangles, excluding stored snapshots/2D patterns. Counts and finite normalized weights do not approve art. Modeling stopped for human review.

<!-- PROJECT_STATE_BEGIN -->
```json
{json.dumps(block,indent=2)}
```
<!-- PROJECT_STATE_END -->
'''
(ROOT/'outputs/DELIVERY.md').write_text(delivery,encoding='utf8')
print('PATTERN_STUDY_PUBLISHED',candidate)
