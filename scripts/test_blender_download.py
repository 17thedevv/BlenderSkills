import urllib.request
import re

for ver in ["Blender4.2", "Blender4.1", "Blender3.6"]:
    url = f"https://download.blender.org/release/{ver}/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            files = re.findall(r'href=[\"\'](blender-[0-9\.]+-windows-x64\.zip)[\"\']', content)
            print(f"{ver}:", sorted(list(set(files))))
    except Exception as e:
        print(f"Error {ver}:", e)
