import sys
import subprocess
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

blender_exe = r"D:\tools\blender-4.2.0-windows-x64\blender.exe"
source_dir = Path("outputs/sources/aplaybox_hsin")
blend_files = list(source_dir.glob("*.blend"))

if not blend_files:
    print("No .blend file found in", source_dir)
    sys.exit(1)

blend_path = blend_files[0]
print("Auditing:", blend_path.name)

output_json = Path("outputs/reports/scene_audit_aplaybox.json")
output_json.parent.mkdir(parents=True, exist_ok=True)

cmd = [
    blender_exe,
    "--background",
    str(blend_path),
    "--python",
    "scripts/audit_blend.py",
    "--",
    "--output",
    str(output_json)
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("Blender return code:", res.returncode)
print("Blender stdout:\n", "\n".join(res.stdout.splitlines()[-30:]))
if res.stderr:
    print("Blender stderr:\n", "\n".join(res.stderr.splitlines()[-20:]))

if output_json.exists():
    data = json.loads(output_json.read_text(encoding='utf-8'))
    print("=== AUDIT SUMMARY ===")
    print("Total objects:", len(data.get("objects", [])))
    total_tris = sum(o.get("triangles", 0) for o in data.get("objects", []))
    print("Total triangles:", total_tris)
    for o in data.get("objects", []):
        print(f" - Object: {o.get('name')}, Tris: {o.get('triangles')}, Shape keys: {len(o.get('shape_keys', []))}, Bones: {len(o.get('vertex_groups', []))}")
