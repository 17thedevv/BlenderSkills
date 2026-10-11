"""Structure/config check only; cannot validate actual Blender images or quality."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["hair-outfit-builder", "reference-fidelity-guardian", "visual-critic", "topology-expert", "streaming-performance"]
errors = []
for name in SKILLS:
    f = ROOT / ".agents" / "skills" / name / "SKILL.md"
    if not f.exists():
        errors.append(f"missing {f}")
        continue
    content = f.read_text(encoding="utf-8")
    if not content.startswith("---\n") or not re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", content):
        errors.append(f"frontmatter invalid: {name}")
    if not re.search(r"(?m)^description:\s*\S.{35,}", content):
        errors.append(f"description missing/too short: {name}")
for rel in ["config/kagari_design_contract.json", "config/project_state.template.json"]:
    try:
        json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"bad json {rel}: {e}")
for rel in ["docs/AGENT_MERGE_PROMPT.md", "docs/TEST_PROTOCOL.md",
            "scripts/audit_blend.py", "scripts/validate_project_state.py"]:
    if not (ROOT / rel).is_file():
        errors.append(f"missing {rel}")
for e in errors:
    print("ERROR", e)
print(f"OVERLAY {'FAIL' if errors else 'STRUCTURE OK'} ({len(SKILLS)} Skills; artistic quality NOT_TESTED)")
sys.exit(bool(errors))
