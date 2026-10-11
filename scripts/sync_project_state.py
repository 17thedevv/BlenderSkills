"""Write a traceable pending-review state and matching delivery manifest.

This command records evidence; it cannot create APPROVED_BY_USER decisions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def hashed(rel):
    p=(ROOT/rel).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():
        raise ValueError('Missing or outside-project artifact: '+rel)
    with p.open('rb') as f:
        digest=hashlib.file_digest(f,'sha256').hexdigest()
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':digest}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--candidate',required=True)
    parser.add_argument('--baseline',required=True)
    parser.add_argument('--version',required=True)
    parser.add_argument('--evidence',action='append',default=[])
    parser.add_argument('--manifest')
    parser.add_argument('--visual-status',choices=['NOT_TESTED','FAIL'],default='NOT_TESTED')
    args=parser.parse_args()
    evidence=list(args.evidence)
    if args.manifest:
        evidence.append(args.manifest)
        manifest=json.loads((ROOT/args.manifest).read_text(encoding='utf-8'))
        evidence.extend(r['path'] for r in manifest['renders'])
    evidence=list(dict.fromkeys(evidence))
    concept='outputs/design/concept_option2_kagari.jpg'
    candidate=hashed(args.candidate); candidate['version']=args.version
    baseline=hashed(args.baseline)
    state={'schema_version':'1.1','project':'Kagari','current_gate':'GARMENT_CLAY_BLOCKOUT_PENDING',
           'current_candidate':candidate,'baseline':baseline,'reference_files':[concept],
           'evidence':evidence,'artifact_records':[hashed(p) for p in [concept]+evidence],
           'delivery_manifest':'outputs/DELIVERY.md','decision':'REQUIRES_HUMAN_ART_REVIEW',
           'approvals':{g:{'status':status,'evidence':None} for g,status in {
               'concept':'PENDING_EVIDENCE','face':'PENDING_EVIDENCE','garment_clay':'NOT_APPROVED',
               'rig':'NOT_TESTED','vrm_export':'NOT_TESTED','webcam':'NOT_TESTED','obs':'NOT_TESTED'}.items()},
           'historical_approval_note':'character_brief reports prior concept approval; original explicit sign-off message is not linked. The current user task authorizes this clay experiment, not aesthetic approval.',
           'tool_inventory':'outputs/reports/v03_merge/tool_inventory.json',
           'blocking_issues':['Human clay-form approval pending','No candidate VRM export/runtime/OBS validation','Base-asset license claims in historical reports require original source/license evidence before final redistribution'],
           'updated_by':'sync_project_state.py; evidence references only'}
    state['agent_visual_review']=args.visual_status
    if args.visual_status=='FAIL':
        state['current_gate']='GARMENT_CONSTRUCTION_FAILED_REQUIRES_METHOD_CHANGE'
        state['blocking_issues'].insert(0,'Three construction cycles exhausted; shoulder intersections and collar contact remain visibly defective. Do not ornament this form.')
    (ROOT/'config/project_state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    block={'candidate_path':candidate['path'],'candidate_sha256':candidate['sha256'],
           'candidate_version':candidate['version'],'decision':state['decision']}
    lines=['# Kagari delivery evidence — v0.3 construction experiment','',
           '<!-- PROJECT_STATE_BEGIN -->','```json',json.dumps(block,indent=2),'```','<!-- PROJECT_STATE_END -->','',
           'Decision: **REQUIRES_HUMAN_ART_REVIEW**. Structural/state validation does not approve the art.','',
           '| Item | Actual status |','|---|---|','| Concept and face sign-off | PENDING_EVIDENCE; historical claims are not newly certified |',
           f'| Garment clay | Agent visual review: {args.visual_status}; human NOT_APPROVED |','| Rig deformation certification | NOT_TESTED; only scoped smoke-test renders where linked |',
           '| Candidate VRM export/reimport | NOT_TESTED |','| Warudo webcam | NOT_TESTED |','| OBS/FPS | NOT_TESTED |','',
           'Current artifact/version/SHA are mirrored from `config/project_state.json`.','',
           '## Artifacts and evidence','']
    for record,label in [(candidate,'Current candidate'),(baseline,'Frozen baseline'),(hashed(concept),'Source concept')]+[(hashed(p),Path(p).name) for p in evidence]:
        link=os.path.relpath(ROOT/record['path'],ROOT/'outputs').replace('\\','/')
        lines.append(f"- [{label}]({link}) — SHA256 `{record['sha256']}`")
    lines+=['','No new ornaments, hair reconstruction, extensive rigging or final VRM export are authorized before clay approval in this iteration.']
    (ROOT/'outputs/DELIVERY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(block,indent=2))

if __name__=='__main__':
    main()
