"""Read-only Blender/VRM capability inventory; never opens camera or exports."""
import bpy
import addon_utils
import json
from pathlib import Path
ROOT=Path('D:/Project-17/blender')
addons=[]
for module in addon_utils.modules():
    info=getattr(module,'bl_info',{})
    if 'vrm' in (module.__name__+' '+info.get('name','')).lower():
        addons.append({'module':module.__name__,'version':list(info.get('version',[])),
                       'enabled':module.__name__ in bpy.context.preferences.addons,'path':module.__file__})
record={'blender':{'path':bpy.app.binary_path,'version':bpy.app.version_string,'status':'EXECUTED_BACKGROUND'},
        'vrm_addons':addons,'import_operator_registered':hasattr(bpy.ops.import_scene,'vrm'),
        'export_operator_registered':hasattr(bpy.ops.export_scene,'vrm'),
        'candidate_export':'NOT_TESTED','candidate_reimport':'NOT_TESTED',
        'warudo':{'status':'NOT_FOUND_IN_INSPECTED_STEAM_LIBRARIES','runtime_test':'NOT_TESTED',
                  'inspected_roots':['C:/Program Files (x86)/Steam/steamapps/common','D:/SteamLibrary/steamapps/common']},
        'obs':{'path':'C:/Program Files (x86)/Steam/steamapps/common/OBS Studio/bin/64bit/obs64.exe',
               'executable_exists':Path('C:/Program Files (x86)/Steam/steamapps/common/OBS Studio/bin/64bit/obs64.exe').is_file(),
               'capture_test':'NOT_TESTED'},
        'webcam':{'capture':'NOT_TESTED','note':'No live camera access in this iteration.'},
        'signed_off_face_renders':{'status':'PENDING_EVIDENCE','note':'Existing renders located; explicit face/head approval not linked in available project files.'}}
p=ROOT/'outputs/reports/v03_merge/tool_inventory.json'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
