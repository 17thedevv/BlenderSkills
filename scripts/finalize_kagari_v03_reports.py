"""Build review documents from real Blender manifests/audits without art approval."""
import difflib
import hashlib
import html
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MERGE=ROOT/'outputs/reports/v03_merge'
REPORT=ROOT/'outputs/reports/v03_clay_cycle03'
BACKUP=ROOT/'outputs/backups/v03_merge_2026-10-11'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def link(p,base=REPORT): return os.path.relpath(ROOT/p,base).replace('\\','/')

a=read(REPORT/'geometry_audit.json'); b=read(REPORT/'baseline_geometry_audit.json')
m=read(REPORT/'render_manifest.json')
new=[o for o in a['objects'] if o['name'].startswith('Kagari_v03_')]
m['new_structural_objects']=[o['name'] for o in new]
m['agent_visual_verdict']='FAIL_CONSTRUCTION'
m['cycle_count']=3
for r in m['renders']: r['image_sha256']=sha(ROOT/r['path'])
(REPORT/'render_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')

summary={
    'baseline':m['baseline'],'candidate':m['candidate'],
    'all_scene':{'baseline_raw':b['raw_triangles'],'baseline_evaluated':b['evaluated_triangles'],
                 'candidate_raw':a['raw_triangles'],'candidate_evaluated':a['evaluated_triangles']},
    'render_enabled_inventory':{'baseline':b['render_enabled_inventory'],'candidate':a['render_enabled_inventory']},
    'new_structural_objects':[{'name':o['name'],'raw':o['raw']['triangles'],'evaluated':o['evaluated']['triangles'],
                               'weights':o['weighting'],'topology':o['topology_raw'],'modifiers':o['modifier_costs']} for o in new],
    'new_raw_total':sum(o['raw']['triangles'] for o in new),
    'new_evaluated_total':sum(o['evaluated']['triangles'] for o in new),
    'largest_modifier_expansions':a['largest_modifier_expansions'],
    'largest_objects':a['largest_by_evaluated_triangles'],
    'exported_vrm':'NOT_TESTED','warudo_runtime':'NOT_TESTED',
    'note':'All-scene totals retain hidden superseded source objects. Render-enabled inventory is viewport evaluated, not final render/export simulation; this is not an FPS optimization result.'}
(REPORT/'geometry_comparison.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')

lines=['# Kagari v0.3 — actual clay construction review','',
       '**Decision: REQUIRES_HUMAN_ART_REVIEW. Agent construction verdict: FAIL.**',
       'Three targeted cycles completed within one scoped experiment. Further geometry changes stopped. The third candidate is an inspectable failed experiment, not a replacement approved for production. No human approval has been invented.','',
       '## Exact inputs and outputs','']
for label,r in [('Original source',m['source']),('Frozen same-camera baseline',m['baseline']),('Current experimental candidate',m['candidate'])]:
    lines+= [f"- {label}: [{r['path']}]({link(r['path'])}); SHA256 `{r['sha256']}`"]
concept='outputs/design/concept_option2_kagari.jpg'
lines += [f"- Concept: [{concept}]({link(concept)}); SHA256 `{sha(ROOT/concept)}`",
          f"- Candidate version: `{m['candidate']['version']}`.",
          '- Historical face/head renders exist, but explicit signed-off evidence was not found. The current instruction authorized this garment experiment; it did not approve the face.','',
          '## Observed top three defects and next geometry correction','',
          '| Priority | Observation in actual images | Proposed correction after human direction |',
          '|---|---|---|',
          '| 1 | Shoulder skin intersects the upper cloth; disconnected-looking slots and hard ridges at the sleeve join remain in front, 3/4 and isolated profile/back. The raised-arm pose exposes the same ridges. | Use a hand-authored shoulder/yoke panel with a real armhole edge, sew sleeve boundary to it, then transfer and locally smooth weights. Avoid moving a cylindrical torso neck ring inward without rebuilding the shoulder pattern. |',
          '| 2 | V-neck contact and overlap are pinched/creased; the diagonal wrap edge reaches the torso but its join is jagged. The layered outer haori/inner crossed collar distinction is not reproduced convincingly. | Trace separate inner wrap and outer haori panels from concept, define the visible inner edge/hidden seam and overlap depth explicitly; weld or bridge appropriate boundaries rather than project a strip onto skin. |',
          '| 3 | Torso is too cylindrical, sleeves are short bell forms, and medium folds are weak. This differs from the reference long sleeve and draped layered garment. | Build upper sleeve first from a small quad panel, add gravity-driven underarm slack and broad fold anchors at shoulder/obi; keep the lower sleeve outside this scoped experiment until the upper construction is approved. |','',
          '## Cycle evidence and baseline contrast','',
          '- Baseline: thick floating crossed strips, detached lapel ends and a mantle-like sleeve silhouette. Side view exposes the offset between strips and torso.',
          '- Cycle 01: source skin extraction preserves weights but reproduces breast forms, jagged collar and pointed shoulders. Rejected by agent; changed construction method immediately.',
          '- Cycle 02: sparse sewn torso/sleeve panel rings give readable hollow sleeves and less disconnected strip geometry. Neck opening remains too wide/off-shoulder and identity drifts toward a V-neck shirt.',
          '- Cycle 03: attempted nape contact and an attached diagonal wrap edge. Shoulder and neckline intersections worsen. Some cloth volume exists, but this is not a reliable artistic improvement over baseline.',
          '- Stop after cycle 03. Recommend manually constructed concept-traced garment panels, or a licensed compatible base garment only after source/license verification and user authorization for external acquisition. Do not increase subdivision or cover defects with ornament.','',
          '## Acceptance assessment','',
          '| Criterion | Observed result |','|---|---|',
          '| Collar layers and plausible contacts | FAIL — pinching/intersection remains; no acceptable layer construction |',
          '| Shoulder/sleeve and moderate raise | FAIL — mass exists but shoulder joins expose artifacts; no deformation certification |',
          '| Cloth form without ornament | PARTIAL — sleeve volume present; torso/fold quality and reference identity insufficient |',
          '| Traceable files, SHA, matched cameras | VERIFIED from manifests and actual file hashes |',
          '| Preserved Face/morphs/Hair/rig | VERIFIED from independent saved-file reopen comparison |',
          '| User form approval | NOT_APPROVED |',
          '| Candidate VRM/Warudo/OBS readiness | NOT_TESTED |','',
          '## Construction and evidence limits','',
          'Front concept establishes outer cream haori, burgundy crossed inner collar and soft drape. Side/back cut, armhole and pattern are inferred; the concept is not a measured sewing pattern. Current gray material hides color deliberately. Existing ornaments are hidden consistently in both sets; textures and original Face/Hair material assignments are preserved. Diagnostic isolated images temporarily hide unmodified Face/Hair/bow to expose garments and are labelled in the manifest.',
          'The candidate retains old garment objects hidden for recoverability and removes only source upper-jacket faces from Body. New mesh weights are normalized and no new subdivision modifier was added. Technical validity does not resolve visible intersections.','',
          '## Geometry cost (Blender viewport depsgraph, all scene meshes)','',
          '| Inventory | Baseline raw | Baseline evaluated | Candidate raw | Candidate evaluated |',
          '|---|---:|---:|---:|---:|',
          f"| All scene, including hidden source | {b['raw_triangles']:,} | {b['evaluated_triangles']:,} | {a['raw_triangles']:,} | {a['evaluated_triangles']:,} |",
          f"| Objects with render enabled* | {b['render_enabled_inventory']['raw_triangles']:,} | {b['render_enabled_inventory']['viewport_evaluated_triangles']:,} | {a['render_enabled_inventory']['raw_triangles']:,} | {a['render_enabled_inventory']['viewport_evaluated_triangles']:,} |",'',
          '*This is a filtered object inventory with viewport modifier levels, not a render/export pipeline or collection visibility simulation. The reduction comes from hiding superseded pieces and is not evidence of runtime performance improvement.',
          f"New structural meshes total {summary['new_raw_total']:,} raw / {summary['new_evaluated_total']:,} evaluated triangles. Growth is from sparse construction plus Solidify, not dense subdivision. Existing bow modifiers dominate expansion and were left intact under the protected scope.",'',
          '| Object / modifier | Triangle increase |','|---|---:|']
for s in a['largest_modifier_expansions'][:8]: lines.append(f"| {s['object']} / {s['name']} ({s['type']}) | +{s['delta']:,} |")
lines+=['',f"Full [geometry audit]({link('outputs/reports/v03_clay_cycle03/geometry_audit.json')}) and [comparison]({link('outputs/reports/v03_clay_cycle03/geometry_comparison.json')}) include topology, weights, shape keys, object costs and failures.",
        f"[Saved invariant check]({link('outputs/reports/v03_clay_cycle03/saved_invariants.json')}); [render/camera/pose/image hashes]({link('outputs/reports/v03_clay_cycle03/render_manifest.json')}); [construction plan before modeling]({link('outputs/reports/v03_clay/construction_plan.md')})."]
(REPORT/'visual_constructibility_review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Local HTML compares unedited Blender outputs, with common framing.
review=ROOT/'outputs/previews/v03_clay_cycle03/review.html'
parts=['<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kagari — v0.3 clay review</title>',
       '<style>body{background:#17191d;color:#eceef2;font:16px system-ui;margin:28px}a{color:#9acaff}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img{width:100%;max-width:900px}h2{margin-top:36px}code{overflow-wrap:anywhere} .warning{background:#462522;padding:16px}</style>',
       '<h1>Kagari — clay construction experiment</h1><p class="warning">REQUIRES_HUMAN_ART_REVIEW · Agent visual: FAIL. Sau 3 lượt, vai–tay áo và cổ vẫn lỗi. Dừng geometry; chưa thêm trang trí hoặc xuất VRM.</p>',
       f"<p>Candidate: <code>{html.escape(m['candidate']['path'])}</code><br>SHA256: <code>{m['candidate']['sha256']}</code></p>",
       '<p>Trái: baseline cố định. Phải: candidate 03. Camera, ánh sáng, framing và pose tương ứng giữ đồng nhất.</p>']
for name in ['front','three_quarter','side','back','pose_arm_raise','portrait']:
    parts += [f'<h2>{name}</h2><div class="grid">']
    for prefix in ['before','after']:
        r=next(r for r in m['renders'] if r['comparison']==prefix and r['view']==name and not r['isolated_garment'])
        src=link(r['path'],review.parent)
        parts.append(f'<figure><figcaption>{prefix}</figcaption><img src="{html.escape(src)}" loading="lazy"></figure>')
    parts.append('</div>')
for name in ['side','back']:
    parts += [f'<h2>{name} — diagnostic: Hair/Face/bow hidden temporarily</h2><div class="grid">']
    for prefix in ['before','after']:
        r=next(r for r in m['renders'] if r['comparison']==prefix and r['view']==name and r['isolated_garment'])
        parts.append(f'<figure><figcaption>{prefix}</figcaption><img src="{html.escape(link(r["path"],review.parent))}" loading="lazy"></figure>')
    parts.append('</div>')
parts += ['<h2>Concept and earlier cycles</h2>',f'<p><a href="{link(concept,review.parent)}">Source concept</a> · <a href="../v03_clay/after_front_clay.png">Cycle 01</a> · <a href="../v03_clay_cycle02/after_front_clay.png">Cycle 02</a> · <a href="../../reports/v03_clay_cycle03/visual_constructibility_review.md">Visual report</a></p></html>']
review.write_text('\n'.join(parts),encoding='utf-8')

briefpath=ROOT/'config/character_brief.json'
brief=read(briefpath)
brief['historical_user_approval']=brief.pop('user_approval',brief.get('historical_user_approval',{}))
brief['approval_source']='config/project_state.json; legacy approval booleans are historical claims, not current evidence.'
brief['version']='0.3.0'
brief['delivery_status']='Garment clay construction experiment failed agent visual review after three cycles; human review pending. See config/project_state.json.'
briefpath.write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Reproducible unified diff against the actual pre-merge backup; no Git assumed.
diff=[]; changed=[]
files=[]
for rel in ['.agents','config','docs','scripts','tests']:
    files.extend(p for p in (ROOT/rel).rglob('*') if p.is_file() and p.suffix in ['.md','.py','.json'] and '__pycache__' not in p.parts)
files += [ROOT/'README.md']
for p in sorted(files):
    rel=p.relative_to(ROOT); old=BACKUP/rel
    if rel.as_posix()=='config/project_state.json': continue  # generated evidence state, avoid self-referential hashed diff
    current=p.read_text(encoding='utf-8-sig'); previous=old.read_text(encoding='utf-8-sig') if old.is_file() else ''
    if previous==current: continue
    changed.append({'path':rel.as_posix(),'status':'MODIFIED' if old.is_file() else 'ADDED','sha256':sha(p)})
    diff.extend(difflib.unified_diff(previous.splitlines(True),current.splitlines(True),fromfile='before/'+rel.as_posix(),tofile='after/'+rel.as_posix()))
(MERGE/'merged_vs_backup.diff').write_text(''.join(diff),encoding='utf-8')
(MERGE/'changed_files.json').write_text(json.dumps(changed,indent=2)+'\n',encoding='utf-8')
skill_diff=[]
for record in changed:
    rel=Path(record['path'])
    if not record['path'].startswith('.agents/skills/') or rel.name!='SKILL.md': continue
    old=BACKUP/rel; p=ROOT/rel
    previous=old.read_text(encoding='utf-8-sig') if old.is_file() else ''
    skill_diff.extend(difflib.unified_diff(previous.splitlines(True),p.read_text(encoding='utf-8-sig').splitlines(True),fromfile='before/'+rel.as_posix(),tofile='after/'+rel.as_posix()))
(MERGE/'skills_guidance.diff').write_text(''.join(skill_diff),encoding='utf-8')
merge='''# v0.3 overlay merge rationale

The actual workspace has 13 skills and no Git repository. A file backup was created at `outputs/backups/v03_merge_2026-10-11` before edits, including original WIP blends and the concept. The provided ZIP was extracted to `outputs/upgrade_overlay_v03`. No commit was invented.

The overlay is an earlier 12-skill derivative. The merge retains all 13 local skill directories and YAML frontmatter, existing production steps, license provenance requirements, attachment/spring-bone guidance, raw topology and legacy audit inventory. Overlay/local differences are recorded in `overlay_vs_local.diff`; final changes against the actual backup are in `merged_vs_backup.diff`.

| Area | Change and rationale |
|---|---|
| Garment/hair skills | Add construction references, contact/layer/anchor planning, clay review before ornament and maximum three ineffective cycles. Retain useful local production/rig advice. |
| Fidelity guardian | Generic reference inventory and observable/inferred checks; remove mandated base mesh and Kagari identity from the generic skill. Project identity is stored in `config/kagari_design_contract.json`. |
| Visual critic | Actual image inspection, same-camera comparisons, artifact hash/version and separate art/technical/runtime status. |
| Face specialist | Correct bangs guidance: avatar geometry affects avatar readability/intersection; it does not directly obstruct the human webcam detector input. |
| Topology/performance | Raw and viewport-evaluated inventories, modifier stage costs, weight warnings, and explicit export/runtime distinction. |
| audit_blend.py | Preserve legacy fields/topology/shape keys/bones/actions; add depsgraph counts, modifier deltas, weight diagnostics, null/error on unavailable results and visible inventory caveat. |
| State validator | Independent of structural discovery. Require actual artifact/version/SHA and evidence; match machine-readable DELIVERY record and resolve local links. No invented human approval. |
| Project docs | README reflects 13 discovered skills. AGENTS/WORKFLOW resume from evidence state. Historical brief booleans moved to an explicitly historical field. |

`config/project_state.json` and `outputs/DELIVERY.md` identify the same final experimental candidate. Historical head/concept sign-off evidence is pending. Blender 4.2 and enabled VRM addon 4.10 were inspected. Warudo was not found in the two inspected Steam roots; no universal installation-absence claim is made. OBS executable exists. Candidate VRM export, Warudo/webcam, OBS capture and FPS remain NOT_TESTED.

Task A structural/state and Python tests passed before modeling; initial source audit was real Blender. A file `project_state_before_clay.json` preserves the pre-experiment state. Final check results are recorded in `validation_results.json`. Technical checks do not approve garment art. Task B stopped after three cycles with failed construction and requires human direction before another method or ornamentation.
'''
(MERGE/'merge_summary.md').write_text(merge+f'\nOverlay ZIP SHA256: `{sha(ROOT/"Kagari-Artistic-Skills-v0.3-overlay.zip")}`.\n',encoding='utf-8')
print('REPORTS_READY',m['candidate'],summary['new_raw_total'],summary['new_evaluated_total'])
