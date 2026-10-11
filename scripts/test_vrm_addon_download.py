import urllib.request
import json

url = "https://api.github.com/repos/saturday06/VRM_Addon_for_Blender/releases/latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("Latest VRM Addon tag:", data.get("tag_name"))
        for asset in data.get("assets", []):
            print("Asset:", asset.get("name"), asset.get("browser_download_url"))
except Exception as e:
    print("Error:", e)
