"""Validate the skill bundle without Blender; run: python scripts/check_skillpack.py."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / '.agents' / 'skills'
REQUIRED = {
    'character-director', 'base-mesh-strategy', 'anime-face-specialist',
    'hair-outfit-builder', 'topology-expert', 'vtuber-rigging',
    'basic-animation-maker', 'visual-critic', 'vrm-delivery',
    'webcam-tracking', 'live-broadcast-integration', 'streaming-performance',
    'reference-fidelity-guardian',
}
errors = []
for name in sorted(REQUIRED):
    f = SKILLS / name / 'SKILL.md'
    if not f.is_file():
        errors.append(f'Missing: {f.relative_to(ROOT)}')
        continue
    content = f.read_text(encoding='utf-8')
    if not content.startswith('---\n'):
        errors.append(f'No YAML frontmatter: {name}')
        continue
    blocks = content.split('---\n', 2)
    front = blocks[1] if len(blocks) > 2 else ''
    nm = re.search(r'^name:\s*(.+)$', front, re.M)
    desc = re.search(r'^description:\s*(.+)$', front, re.M)
    if not nm or nm.group(1).strip() != name:
        errors.append(f'Name mismatch: {name}')
    if not desc or len(desc.group(1).strip()) < 35:
        errors.append(f'Missing/unhelpful description: {name}')
    for rel in re.findall(r'\]\((references/[^)]+)\)', content):
        target = (f.parent / rel).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f'Broken skill reference: {name}/{rel}')
try:
    brief = json.loads((ROOT / 'config' / 'character_brief.json').read_text(encoding='utf-8'))
    assert brief['target_output'] == 'VRM 1.0'
    assert brief['gender_presentation'] == 'female anime'
    assert brief['primary_runtime'] == 'Warudo'
    assert brief['tracking']['driver'] == 'Warudo MediaPipe built-in'
except (OSError, json.JSONDecodeError, AssertionError, KeyError) as exc:
    errors.append(f'Invalid config/character_brief.json: {exc}')
for f in ['.agents/AGENTS.md', 'docs/WORKFLOW.md', 'docs/QUALITY_RUBRIC.md',
          'docs/ANTIGRAVITY_PROMPT.md', 'docs/MODEL_RIG_ARCHITECTURE.md',
          'docs/WEBCAM_TRACKING_TEST.md', 'docs/INTEGRATION_ARCHITECTURE.md',
          'scripts/audit_blend.py', 'scripts/render_review.py', 'scripts/audit_vrm.py']:
    if not (ROOT / f).exists():
        errors.append(f'Missing {f}')
if errors:
    print('SKILLPACK FAILED')
    for e in errors:
        print(' -', e)
    sys.exit(1)
actual_count = len(list(SKILLS.glob('*/SKILL.md')))
print(f'SKILLPACK STRUCTURE OK ({actual_count} discovered skills; no artifact/art/runtime approval implied)')
