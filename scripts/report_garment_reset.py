"""Create evidence-based garment study report, gallery and pending-review state."""
import json, hashlib, os, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'outputs/reports/garment_reset_final'; P=ROOT/'outputs/previews/garment_reset_final'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def record(rel): return {'path':rel,'sha256':sha(ROOT/rel)}
def link(rel,base=R): return os.path.relpath(ROOT/rel,base).replace('\\','/')
m=read(R/'render_manifest.json'); a=read(R/'geometry_audit.json'); v=read(R/'technical_verification.json')
b=read(ROOT/'outputs/reports/v03_clay_cycle03/geometry_audit.json')
c=read(ROOT/'outputs/reports/garment_reset/matched_cycle03_manifest.json')
d=read(ROOT/'outputs/reports/garment_reset/drape_execution.json')
garments=[o for o in a['objects'] if o['name'] in m['prototype_objects']]
graw=sum(o['raw']['triangles'] for o in garments); geval=sum(o['evaluated']['triangles'] for o in garments)
basegarments=[o for o in b['objects'] if o['name'].startswith('Kagari_v03_')]
br=sum(o['raw']['triangles'] for o in basegarments); be=sum(o['evaluated']['triangles'] for o in basegarments)
# Record matched settings verification rather than asserting camera similarity.
camera_keys=['camera_location','camera_rotation','ortho_scale','arm_L_euler']
matched={r['view']:all(r[k]==next(x for x in c['renders'] if x['view']==r['view'])[k] for k in camera_keys) for r in m['renders']}
assert all(matched.values()),'Comparison framing/pose mismatch'
verdict={'candidate':m['candidate'],'decision':'REQUIRES_HUMAN_ART_REVIEW','agent_visual_acceptance':'FAIL',
 'scope':'Isolated duplicate-mannequin collar, upper support and one sleeve; not a full character candidate.',
 'all_original_eight_cycle03_images_inspected':True,'all_final_five_and_matched_five_images_inspected':True,
 'matched_camera_and_pose_fields':matched,'source_unchanged':v['source_unchanged'],
 'criteria':{
  'fabric_thickness_and_overlap':'PARTIAL: broad front panels genuinely overlap; connected nape/attached band, but neckline and seam spacing remain coarse.',
  'natural_shoulder_sleeve_continuity':'FAIL: joined mesh surface exists, but pinned shoulder seam sits too high and reads as a plate, especially profile/3-quarter.',
  'wide_sleeve_silhouette':'OBSERVED: one wide hanging fabric bag and distal opening, unlike the short radial tube.',
  'plausible_folds_volume':'PARTIAL: gravity-derived back/torso tension folds and hanging sleeve mass; folds gather too sharply at armpit.',
  'no_obvious_intersections':'NOT_CERTIFIED: neutral major body breakthrough is not obvious, but dark root folds/gaps and raised-pose angular artifacts leave intersection risk.',
  'basic_arm_deformation':'FAIL: actual ordinary armature raise reveals sharp root pinching; no solver/corrective morph used to disguise it.'},
 'human_approval':'NOT_APPROVED','vrm_export':'NOT_TESTED','warudo_runtime':'NOT_TESTED',
 'new_method_trials':[
   {'path':'outputs/wip/kagari_panel_drape_prototype_01.blend','status':'SELECTED_FOR_METHOD_REVIEW_NOT_APPROVED','reason':'Best readable broad sleeve/drape among tests; final adds continuous nape seam.'},
   {'path':'outputs/wip/kagari_panel_drape_prototype_02.blend','status':'REJECTED_BY_AGENT','reason':'Softer pins and anatomical shoulder placement collapse sleeve/root during long drape.'},
   {'path':'outputs/wip/kagari_panel_drape_prototype_03.blend','status':'REJECTED_BY_AGENT','reason':'Clearance placement/higher bending reduce some collapse, but bag/root remain crumpled and restricted.'}],
 'stop_reason':'Three new-method trials exhausted; no further aesthetic repairs before human direction.',
 'next_method_recommendation':'Keep explicit panel/seam topology but hand-fit the yoke and armhole first; restrict cloth to free sleeve bag/hem with stable boundary, transfer/smooth binding at root. Test flat pattern/seam layout before another full-surface solve.'}
(R/'visual_review.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
complexity={'prototype_garment_raw':graw,'prototype_garment_evaluated':geval,'prototype_whole_scene_raw':a['raw_triangles'],
 'prototype_whole_scene_evaluated':a['evaluated_triangles'],'cycle03_four_structural_meshes_raw':br,
 'cycle03_four_structural_meshes_evaluated':be,'largest_modifier_expansions':a['largest_modifier_expansions'],
 'comparison_limits':'Cycle03 has two sleeves, two torso layers and collar/edge; reset has one sleeve and minimum torso support. Whole-avatar and mannequin totals are different scopes; no optimization/FPS claim.',
 'exported_vrm_triangles':None,'export_count_status':'NOT_TESTED'}
(R/'mesh_complexity_comparison.json').write_text(json.dumps(complexity,indent=2)+'\n',encoding='utf-8')
lines=['# Kagari — garment strategy reset: reviewed prototype','',
 '**Decision: REQUIRES_HUMAN_ART_REVIEW. Full artistic acceptance: FAIL.**',
 'The construction method has changed; the rejected Cycle 03 meshes were not polished or used to generate this new garment. Three independent panel/drape configurations were investigated. The first configuration is retained for the clearest wide-sleeve method comparison; later configurations are shown and rejected. No ornaments or full-character reconstruction.','',
 '## Method and scope','',
 'New overlapping front sheet panels, back support, sewn shoulder bridge and one wide front/back sleeve bag. Explicit shared vertex indices/bridge faces establish seams. Blender-native Cloth with Collision/self-collision runs for 65 sequential frames on a copied mannequin. The frame-65 surface is frozen into a conventional rigged mesh; equilibrium/convergence was not certified. A final continuous collar nape bridge shares vertices with both real front-panel collar leaves. Thickness is 1.6 mm at the existing meter scale, without subdivision.',
 'The duplicate mannequin has arms 30 degrees below horizontal; the acceptance pose raises its left arm by 30 degrees to horizontal. Rendered pose is ordinary skinning only, with no live Cloth or pose-corrective morph. Original Kagari Face/Hair/morphs/rig are not edited; the source .blend SHA remains unchanged.',
 f"[Failure analysis and tool/method comparison]({link('outputs/reports/garment_reset/failure_analysis_and_method.md')}) includes all six construction failures, installed-tool evidence and official Blender sources. [Plan before geometry]({link('outputs/reports/garment_reset/construction_plan.md')}).",'',
 '## Actual files and hashes','']
for label,item in [('Selected sewn prototype',m['candidate']),('Original rejected Cycle 03',m['baseline']),('Pre-drape panel/seam setup',m['raw_setup']),('Frozen drape before collar seam',m['input_drape'])]:
    lines.append(f"- {label}: [{item['path']}]({link(item['path'])}); SHA256 `{item['sha256']}`")
concept='outputs/design/concept_option2_kagari.jpg'
lines+=[f"- Reference: [{concept}]({link(concept)}); SHA256 `{sha(ROOT/concept)}`.",
        '- Mannequin source is duplicated upper Body plus copied armature and a plain head surrogate. Lower/body cut boundaries are deliberately visible diagnostic crop boundaries, not final avatar geometry. The unsleeved side intentionally ends at an open armhole.',
        '- Source side/back sleeve pattern is inferred from the front concept; this is a method study, not an approved pattern or 1:1 reconstruction.','',
        '## Observed comparison with Cycle 03','',
        '| Region | Cycle 03, same mannequin/camera | Panel/drape prototype |','|---|---|---|',
        '| Collar | Pinched V-ring plus projected diagonal edge over an elliptical torso | Real broad front-panel overlap with an attached thin collar band; neckline still angular/high |',
        '| Sleeve | Short rigid radial tube/bell forms | One wide fabric bag, open forearm aperture, visible hanging lower volume |',
        '| Shoulder | Exposed shoulder and broken-looking tube root | Mesh continuity from support to sleeve is real; pinned shoulder still high/boxy |',
        '| Torso/back | Smooth cylindrical envelope with little tension response | Gravity-derived folds run between shoulder, side seam and hem; too asymmetric and concentrated at the root |',
        '| Arm raise | Tubes follow arm with ridged joins | Bag follows arm, but root pinches and develops angular folds. Still fails acceptable deformation |',
        '| Waist sash | Rigid extruded belt | Not built; intentionally outside this limited prototype. Removing it is not evidence of a successful sash reconstruction |','',
        '## Acceptance evidence','',
        '| Required criterion | Agent observation |','|---|---|']
for k,val in verdict['criteria'].items(): lines.append(f'| {k.replace("_"," ")} | {val} |')
lines+=['','Neither successful simulation nor normalized weights equals artistic success. All five final images and matched Cycle 03 views were inspected, in addition to the original eight images. No blanket intersection-free claim is supported.','',
        '## Top three remaining defects / next corrections','',
        '1. **Shoulder/yoke sits too high and stiff.** Profile and 3/4 show a box-like cap/overhang. Recut the yoke against the duplicate shoulder, match armhole edge length and place the seam before simulating. Current pinning preserves a bad starting boundary.',
        '2. **Armpit/root folds and binding are unreliable.** Front/back and raised arm show concentrated jagged folding. Separate free bag cloth from the strongly supported yoke; give the armhole an adequate slack/gusset transition and solve only the hanging region. Smooth weights after neutral drape; keep an ordinary rig-only test.',
        '3. **Collar/nape and hem need a cleaner pattern fit.** The overlap now has real panel mass and continuous nape topology, but neckline stands off and the support hem is an oblique/floating crop. Fit collar band width/cross-section to that seam and reduce excessive pinning; do not use ornament to cover it.',
        'Stop here after three new-method trials. Proposed changes are future work pending human direction, not already completed.','',
        '## Mesh complexity and verification','',
        '| Scope | Raw triangles | Viewport-evaluated triangles |','|---|---:|---:|',
        f'| New support + one sleeve | {garments[0]["raw"]["triangles"]:,} | {garments[0]["evaluated"]["triangles"]:,} |',
        f'| Continuous overlapping collar | {garments[1]["raw"]["triangles"]:,} | {garments[1]["evaluated"]["triangles"]:,} |',
        f'| New garment only | {graw:,} | {geval:,} |',
        f'| Mannequin study whole scene | {a["raw_triangles"]:,} | {a["evaluated_triangles"]:,} |',
        f'| Cycle 03 four structural meshes | {br:,} | {be:,} |','',
        'These scopes differ: Cycle 03 includes two sleeves and two torso layers. Whole-avatar totals also include unrelated hair/bow/hidden geometry. These are no FPS/export benchmarks. Solidify expands the new support by +6,356 triangles and collar by +1,168; no subdivision or live cloth modifier remains on the final mesh.',
        'Both garment surfaces are connected individually, have zero zero-area faces and zero interior non-manifold edges in raw topology. Open boundary edges at neckline/hem/armhole are intentional before thickness. All deforming vertices have normalized weights with at most four deform influences. Evaluated neutral/raised coordinates are finite. These technical results do not resolve the visible root artifacts.',
        f"[Full geometry audit]({link('outputs/reports/garment_reset_final/geometry_audit.json')}); [technical verification]({link('outputs/reports/garment_reset_final/technical_verification.json')}); [complexity comparison]({link('outputs/reports/garment_reset_final/mesh_complexity_comparison.json')}).",'',
        '## VRM and rigging risks','',
        '- Native Cloth is an authoring/drape tool here. The final mesh can be evaluated with an Armature; VRM export/re-import has not been run, and Blender Cloth motion is not a runtime certification.',
        '- Sleeve root/underarm still needs pose-safe topology and weights. A frozen neutral fold rotates with skinning; it does not continue to hang under world gravity. Dynamic cloth/spring-bone or corrective treatment would require separate design/testing.',
        '- Pattern UVs and seam groups are retained as working data, but production UV layout/materials are not approved. Solidify must be handled consistently by export; final exported triangle count is unknown.',
        '- The mannequin .blend is not a complete VRM avatar: it has no delivery-ready facial expressions/metadata, second sleeve, full outfit or validated runtime. The copied humanoid armature is a study binding only. Original character source remains separate.',
        '- No new software, external mesh or asset was installed/downloaded. Registered tools and a scoped Windows install inventory were inspected.','',
        '## Human review','',
        'Review the panel/drape direction and decide whether to continue with a hand-fitted yoke/armhole plus selectively simulated sleeve, or pause this automatic construction route. Current form is NOT_APPROVED and should not unlock decorations or integration into Kagari.']
(R/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Gallery contains original eight, five matched comparisons and both rejected
# new-method trials. Images are original, unedited Blender renders.
parts=['<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kagari garment strategy reset</title>',
 '<style>body{background:#181a1e;color:#eef0f5;font:16px system-ui;margin:28px}a{color:#9acaff}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}img{width:100%}figure{margin:0}h2{margin-top:36px}code{overflow-wrap:anywhere}.warn{background:#492722;padding:18px}</style>',
 '<h1>Kagari — panel / seam / drape study</h1><p class="warn">REQUIRES_HUMAN_ART_REVIEW · Form chưa đạt đầy đủ: vai cứng và nách bị gãy khi nâng tay. Đây là mannequin riêng, không phải avatar mới.</p>',
 f'<p><a href="{link("outputs/reports/garment_reset_final/report.md",P)}">Báo cáo phương pháp, lỗi và risks</a> · <a href="{link(m["candidate"]["path"],P)}">Prototype .blend</a></p>',
 f'<p>SHA256 <code>{m["candidate"]["sha256"]}</code></p><p>Trái: Cycle 03 trên cùng mannequin. Phải: panel/drape mới. Cùng camera, A-pose và ánh sáng; chỉ một tay áo mới, không dựng obi.</p>']
for view in ['front','three_quarter','side','back','arm_raised']:
    parts += [f'<h2>{view}</h2><div class="grid">']
    for label,r in [('Cycle 03',next(x for x in c['renders'] if x['view']==view)),('New panel / drape',next(x for x in m['renders'] if x['view']==view))]:
        parts.append(f'<figure><figcaption>{label}</figcaption><img src="{html.escape(link(r["path"],P))}" loading="lazy"></figure>')
    parts.append('</div>')
parts += ['<h2>Rejected new-method trials 02 / 03 — không chọn</h2><div class="grid">']
for trial in ['garment_reset_v02','garment_reset_v03']:
    parts.append(f'<figure><figcaption>{trial}: co dúm / tự xuyên ở nách</figcaption><img src="../{trial}/prototype_three_quarter_clay.png" loading="lazy"></figure>')
parts.append('</div><h2>Original eight Cycle 03 images inspected</h2><div class="grid">')
for filename in ['after_front_clay','after_three_quarter_clay','after_side_clay','after_back_clay','after_pose_arm_raise_clay','after_portrait_clay','after_side_garment_isolated','after_back_garment_isolated']:
    parts.append(f'<figure><figcaption>{filename}</figcaption><img src="../v03_clay_cycle03/{filename}.png" loading="lazy"></figure>')
parts.append('</div></html>')
(P/'review.html').write_text('\n'.join(parts),encoding='utf-8')

# Preserve historical approval records. New user request authorizes the study,
# not its art. Source character is kept explicitly separate from current study.
state=read(ROOT/'outputs/backups/garment_strategy_reset_start/project_state.json')
state.update({'current_gate':'ISOLATED_GARMENT_METHOD_REVIEW_PENDING','current_candidate':m['candidate'],
 'current_candidate_role':'ISOLATED_MANNEQUIN_GARMENT_PROTOTYPE_NOT_FULL_AVATAR',
 'current_character_source':m['baseline'],'baseline':m['baseline'],'decision':'REQUIRES_HUMAN_ART_REVIEW',
 'agent_visual_review':'FAIL_ACCEPTANCE','blocking_issues':['Prototype shoulder and sleeve-root deformation still fail acceptance',
 'Human garment-method/form approval pending','No prototype VRM export/reimport or Warudo/OBS verification'],
 'updated_by':'report_garment_reset.py; no human approval inferred'})
state['approvals']['garment_clay']={'status':'NOT_APPROVED','evidence':None}
files=['outputs/reports/garment_reset_final/report.md','outputs/reports/garment_reset_final/visual_review.json',
 'outputs/reports/garment_reset_final/geometry_audit.json','outputs/reports/garment_reset_final/technical_verification.json',
 'outputs/reports/garment_reset_final/mesh_complexity_comparison.json','outputs/reports/garment_reset_final/render_manifest.json',
 'outputs/previews/garment_reset_final/review.html','outputs/reports/garment_reset/failure_analysis_and_method.md',
 'outputs/reports/garment_reset/construction_plan.md','outputs/reports/garment_reset/artifact_and_tools.json',
 'outputs/reports/garment_reset/installed_garment_tools.json','outputs/reports/garment_reset/panel_patterns_and_seams.json',
 'outputs/reports/garment_reset/drape_execution.json','outputs/reports/garment_reset_v02/drape_execution.json',
 'outputs/reports/garment_reset_v03/drape_execution.json','outputs/reports/garment_reset/matched_cycle03_manifest.json',
 m['raw_setup']['path'],m['input_drape']['path'], 'outputs/wip/kagari_panel_drape_prototype_02.blend','outputs/wip/kagari_panel_drape_prototype_03.blend']
files += [x['path'] for x in m['renders']+c['renders']]
files += ['outputs/previews/v03_clay_cycle03/'+s+'.png' for s in ['after_front_clay','after_three_quarter_clay','after_side_clay','after_back_clay','after_pose_arm_raise_clay','after_portrait_clay','after_side_garment_isolated','after_back_garment_isolated']]
files += [f'outputs/previews/{trial}/prototype_{view}_clay.png' for trial in ['garment_reset_v02','garment_reset_v03'] for view in ['front','three_quarter','side','back','arm_raised']]
files=list(dict.fromkeys(files)); state['evidence']=files; state['artifact_records']=[record(rel) for rel in [concept]+files]
state['reference_files']=[concept]
(ROOT/'config/project_state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
block={'candidate_path':m['candidate']['path'],'candidate_sha256':m['candidate']['sha256'],'candidate_version':m['candidate']['version'],'decision':'REQUIRES_HUMAN_ART_REVIEW'}
delivery=['# Kagari — isolated garment method study','', '<!-- PROJECT_STATE_BEGIN -->','```json',json.dumps(block,indent=2),'```','<!-- PROJECT_STATE_END -->','',
 '**REQUIRES_HUMAN_ART_REVIEW. Agent acceptance: FAIL.** Current candidate is a standalone mannequin prototype, not a complete replacement Kagari avatar. The original character source is unchanged.','',
 'Two real overlapping front panels, one wide sleeve and shoulder/torso support; neutral clay only. No decorations, second sleeve, obi or full-character reconstruction. No VRM/runtime certification. Human approval NOT_APPROVED.','']
for label,r in [('Study candidate',m['candidate']),('Unchanged character source / baseline',m['baseline']),('Source concept',record(concept))]+[(Path(p).name,record(p)) for p in files]:
    delivery.append(f'- [{label}]({link(r["path"],ROOT/"outputs")}) — SHA256 `{r["sha256"]}`')
delivery += ['','Do not ornament, integrate this geometry into Kagari or export it as a final VRM before human review and the unresolved construction/pose checks.']
(ROOT/'outputs/DELIVERY.md').write_text('\n'.join(delivery)+'\n',encoding='utf-8')
print('GARMENT_RESET_REPORTED',graw,geval,m['candidate'])
