"""Reopen source and candidate and compare protected geometry/pose fingerprints."""
import json
from pathlib import Path
code=Path(__file__).with_name('build_kagari_v03_clay.py').read_text(encoding='utf-8')
exec(compile(code[:code.index('before=protected();')],__file__,'exec'))
original=protected(); candidate=ROOT/'outputs/wip/kagari_v03_clay_03.blend'
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene=bpy.context.scene; arm=bpy.data.objects['Armature']; body=bpy.data.objects['Body']
current=protected()
result={'source':str(SOURCE),'candidate':str(candidate),'source_sha256':filehash(SOURCE),
        'candidate_sha256':filehash(candidate),'source_fingerprints':original,
        'saved_candidate_fingerprints':current,'checks':{name:original[name]==current[name] for name in original},
        'scope':'Face coordinates/all shape key coordinates and values, Hair mesh/material assignment/weights/bindings, armature bones and neutral pose. No runtime certification.'}
(ROOT/'outputs/reports/v03_clay_cycle03/saved_invariants.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert all(result['checks'].values()),'Protected saved-state mismatch'
print('SAVED_INVARIANTS_PASS',result['checks'])
