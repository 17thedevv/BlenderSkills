import os
import sys
import shutil
import subprocess
import json
import winreg
from pathlib import Path

def find_in_registry():
    apps = {}
    keys_to_check = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
    ]
    for root, path in keys_to_check:
        try:
            with winreg.OpenKey(root, path) as k:
                num_subkeys = winreg.QueryInfoKey(k)[0]
                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(k, i)
                        with winreg.OpenKey(k, subkey_name) as subk:
                            # Try to get DisplayName and InstallLocation
                            display_name = ""
                            install_loc = ""
                            try:
                                display_name = winreg.QueryValueEx(subk, "DisplayName")[0]
                            except OSError:
                                pass
                            try:
                                install_loc = winreg.QueryValueEx(subk, "InstallLocation")[0]
                            except OSError:
                                pass
                            if not install_loc:
                                try:
                                    install_loc = winreg.QueryValueEx(subk, "")[0]
                                except OSError:
                                    pass
                            
                            target = (display_name or subkey_name).lower()
                            for app_name in ["blender", "warudo", "obs", "vroid", "steam"]:
                                if app_name in target:
                                    apps.setdefault(app_name, []).append({
                                        "name": display_name or subkey_name,
                                        "location": install_loc,
                                        "key": f"{path}\\{subkey_name}"
                                    })
                    except OSError:
                        pass
        except OSError:
            pass
    return apps

def check_blender():
    res = {"installed": False, "path": None, "version": None, "vrm_addon": False, "vrm_addon_version": None}
    blender_path = shutil.which("blender")
    if not blender_path:
        # Check default paths
        candidates = [
            r"D:\tools\blender-4.2.0-windows-x64\blender.exe",
            r"C:\Program Files\Blender Foundation",
            r"C:\Program Files (x86)\Blender Foundation",
            r"D:\Program Files\Blender Foundation",
            r"D:\Blender",
            r"C:\Blender",
        ]
        for c in candidates:
            if os.path.isfile(c):
                blender_path = c
                break
            elif os.path.exists(c):
                for root, dirs, files in os.walk(c):
                    if "blender.exe" in files:
                        blender_path = os.path.join(root, "blender.exe")
                        break
            if blender_path:
                break
    
    if blender_path and os.path.exists(blender_path):
        res["installed"] = True
        res["path"] = blender_path
        # Query version
        try:
            cp = subprocess.run([blender_path, "--version"], capture_output=True, text=True, timeout=10)
            res["version"] = cp.stdout.strip().splitlines()[0] if cp.stdout else "Unknown"
        except Exception as e:
            res["version"] = f"Error: {e}"
            
        # Check addons in blender
        check_addon_code = """
import addon_utils
import json
installed_addons = [mod.__name__ for mod in addon_utils.modules()]
vrm_addons = [name for name in installed_addons if 'vrm' in name.lower()]
print("VRM_ADDONS:" + json.dumps(vrm_addons))
"""
        try:
            cp = subprocess.run([blender_path, "--background", "--python-expr", check_addon_code], capture_output=True, text=True, timeout=15)
            for line in cp.stdout.splitlines():
                if line.startswith("VRM_ADDONS:"):
                    vrm_list = json.loads(line.replace("VRM_ADDONS:", ""))
                    if vrm_list:
                        res["vrm_addon"] = True
                        res["vrm_addon_name"] = vrm_list
        except Exception as e:
            res["vrm_addon_error"] = str(e)
            
    return res

def check_obs():
    res = {"installed": False, "path": None}
    obs_path = shutil.which("obs64") or shutil.which("obs")
    if not obs_path:
        candidates = [
            r"C:\Program Files (x86)\Steam\steamapps\common\OBS Studio\bin\64bit\obs64.exe",
            r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
            r"D:\Program Files\obs-studio\bin\64bit\obs64.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                obs_path = c
                break
    if obs_path and os.path.exists(obs_path):
        res["installed"] = True
        res["path"] = obs_path
    return res

def check_warudo():
    res = {"installed": False, "path": None}
    # Check Steam libraries and common locations
    candidates = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Warudo\Warudo.exe",
        r"D:\SteamLibrary\steamapps\common\Warudo\Warudo.exe",
        r"E:\SteamLibrary\steamapps\common\Warudo\Warudo.exe",
        r"C:\Warudo\Warudo.exe",
        r"D:\Warudo\Warudo.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            res["installed"] = True
            res["path"] = c
            break
    return res

def check_vroid():
    res = {"installed": False, "path": None}
    candidates = [
        r"C:\Program Files\VRoid\VRoidStudio\VRoidStudio.exe",
        r"C:\Program Files (x86)\Steam\steamapps\common\VRoidStudio\VRoidStudio.exe",
        r"D:\SteamLibrary\steamapps\common\VRoidStudio\VRoidStudio.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            res["installed"] = True
            res["path"] = c
            break
    return res

def check_webcam():
    cameras = []
    try:
        # Run powershell Get-PnpDevice
        ps_cmd = 'Get-PnpDevice -Class "Camera","Image" -Status OK | Select-Object FriendlyName, InstanceId, Status | ConvertTo-Json'
        cp = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=10)
        if cp.stdout.strip():
            data = json.loads(cp.stdout.strip())
            if isinstance(data, list):
                cameras = data
            elif isinstance(data, dict):
                cameras = [data]
    except Exception as e:
        cameras = [{"error": str(e)}]
    return cameras

if __name__ == "__main__":
    report = {}
    report["registry_search"] = find_in_registry()
    report["blender"] = check_blender()
    report["obs"] = check_obs()
    report["warudo"] = check_warudo()
    report["vroid"] = check_vroid()
    report["webcam"] = check_webcam()
    print(json.dumps(report, indent=2))
