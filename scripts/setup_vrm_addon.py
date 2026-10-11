import os
import sys
import zipfile
import urllib.request
import subprocess
from pathlib import Path

BLENDER_EXE = r"D:\tools\blender-4.2.0-windows-x64\blender.exe"
EXT_ZIP = r"D:\tools\downloads\VRM_Addon_for_Blender-Extension-4_10_0.zip"
CLASSIC_URL = "https://github.com/saturday06/VRM-Addon-for-Blender/releases/download/v4.10.0/VRM_Addon_for_Blender-4_10_0.zip"
CLASSIC_ZIP = r"D:\tools\downloads\VRM_Addon_for_Blender-4_10_0.zip"

appdata = os.environ.get("APPDATA")
blender_user = Path(appdata) / "Blender Foundation" / "Blender" / "4.2"

# 1. Setup extension directory
ext_dir = blender_user / "extensions" / "user_default" / "vrm_addon_for_blender"
ext_dir.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(EXT_ZIP, 'r') as z:
    z.extractall(ext_dir)
print(f"Extracted extension to {ext_dir}")

# 2. Setup classic addon directory as well
addon_dir = blender_user / "scripts" / "addons"
addon_dir.mkdir(parents=True, exist_ok=True)
if not os.path.exists(CLASSIC_ZIP):
    print("Downloading classic addon zip...")
    req = urllib.request.Request(CLASSIC_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(CLASSIC_ZIP, "wb") as f:
        f.write(resp.read())

with zipfile.ZipFile(CLASSIC_ZIP, 'r') as z:
    z.extractall(addon_dir)
print(f"Extracted classic addon to {addon_dir}")

# 3. Test in Blender
test_script = """
import addon_utils
import bpy

print("--- TESTING ADDONS IN BLENDER ---")
modules = [mod.__name__ for mod in addon_utils.modules()]
vrm_mods = [m for m in modules if 'vrm' in m.lower()]
print("Found VRM modules:", vrm_mods)

for m in vrm_mods:
    try:
        addon_utils.enable(m, default_set=True)
        print(f"Successfully enabled: {m}")
    except Exception as e:
        print(f"Failed to enable {m}: {e}")

# Check operators
vrm_ops = [op for op in dir(bpy.ops) if 'vrm' in op.lower()]
print("VRM ops:", vrm_ops)
if hasattr(bpy.ops, 'export_scene') and hasattr(bpy.ops.export_scene, 'vrm'):
    print("SUCCESS: bpy.ops.export_scene.vrm is available!")
"""

tmp_py = Path("D:/tools/test_vrm_load.py")
tmp_py.write_text(test_script, encoding="utf-8")

res = subprocess.run([BLENDER_EXE, "--background", "--python", str(tmp_py)], capture_output=True, text=True)
print("Output:\n", res.stdout)
if res.stderr:
    print("Stderr:\n", res.stderr)
