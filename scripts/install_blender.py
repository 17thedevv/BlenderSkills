import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
from pathlib import Path

TOOLS_DIR = Path("D:/tools")
DOWNLOADS_DIR = TOOLS_DIR / "downloads"
BLENDER_URL = "https://download.blender.org/release/Blender4.2/blender-4.2.0-windows-x64.zip"
BLENDER_ZIP = DOWNLOADS_DIR / "blender-4.2.0-windows-x64.zip"
BLENDER_TARGET = TOOLS_DIR / "blender-4.2.0-windows-x64"

VRM_ADDON_URL = "https://github.com/saturday06/VRM-Addon-for-Blender/releases/download/v4.10.0/VRM_Addon_for_Blender-Extension-4_10_0.zip"
VRM_ADDON_ZIP = DOWNLOADS_DIR / "VRM_Addon_for_Blender-Extension-4_10_0.zip"

def download_file(url, target_path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and target_path.stat().st_size > 1000000:
        print(f"Already exists: {target_path} ({target_path.stat().st_size} bytes)")
        return
    print(f"Downloading {url} to {target_path}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(target_path, "wb") as f:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1MB
        last_pct = -1
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = int(downloaded * 100 / total)
                if pct % 10 == 0 and pct != last_pct:
                    print(f"Download progress: {pct}% ({downloaded // (1024*1024)}MB / {total // (1024*1024)}MB)")
                    last_pct = pct
    print(f"Download completed: {target_path}")

def extract_zip(zip_path, target_dir):
    print(f"Extracting {zip_path} to {target_dir}...")
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(target_dir.parent)
    print("Extraction completed.")

def verify_blender(blender_exe):
    print(f"Verifying Blender executable at {blender_exe}...")
    res = subprocess.run([str(blender_exe), "--version"], capture_output=True, text=True)
    print("Blender version output:\n", res.stdout)
    return res.returncode == 0

def install_vrm_addon(blender_exe, addon_zip):
    print(f"Installing VRM Add-on from {addon_zip}...")
    # For Blender 4.2+, extensions can be installed via command line or python script
    setup_py = f"""
import bpy
import sys

addon_path = r"{addon_zip}"
try:
    # Try extension install
    if hasattr(bpy.ops.preferences, "extension_install"):
        bpy.ops.preferences.extension_install(repo_index=0, filepath=addon_path)
        print("Installed via extension_install")
    elif hasattr(bpy.ops.preferences, "addon_install"):
        bpy.ops.preferences.addon_install(filepath=addon_path)
        print("Installed via addon_install")
except Exception as e:
    print("Error during install op:", e)

# Save preferences
bpy.ops.wm.save_userpref()

# Check modules
import addon_utils
print("Active modules with VRM:")
for m in addon_utils.modules():
    if "vrm" in m.__name__.lower():
        print(" - Found:", m.__name__)
"""
    tmp_script = TOOLS_DIR / "setup_vrm.py"
    tmp_script.write_text(setup_py, encoding="utf-8")
    res = subprocess.run([str(blender_exe), "--background", "--python", str(tmp_script)], capture_output=True, text=True)
    print("Addon setup output:\n", res.stdout)
    if res.stderr:
        print("Addon setup stderr:\n", res.stderr)

if __name__ == "__main__":
    download_file(BLENDER_URL, BLENDER_ZIP)
    blender_exe = BLENDER_TARGET / "blender.exe"
    if not blender_exe.exists():
        extract_zip(BLENDER_ZIP, BLENDER_TARGET)
    
    if blender_exe.exists():
        verify_blender(blender_exe)
        download_file(VRM_ADDON_URL, VRM_ADDON_ZIP)
        install_vrm_addon(blender_exe, VRM_ADDON_ZIP)
        print(f"SUCCESS: Blender is ready at {blender_exe}")
    else:
        print(f"ERROR: Could not find {blender_exe} after extraction.")
