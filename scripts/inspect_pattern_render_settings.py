import bpy,json
from pathlib import Path
root=Path('D:/Project-17/blender');out={}
for label,path in [('recovery2','outputs/wip/kagari_garment_recovery_v2.blend'),('study','outputs/wip/kagari_pattern_trial2_prototype.blend')]:
    bpy.ops.wm.open_mainfile(filepath=str(root/path));s=bpy.context.scene;sh=s.display.shading
    out[label]={'studio_light':sh.studiolight_rotate_z if hasattr(sh,'studiolight_rotate_z') else None,'studio_name':sh.studio_light,'shadow_intensity':sh.shadow_intensity,'render_engine':s.render.engine,'color_type':sh.color_type,'single_color':list(sh.single_color),'resolution':[s.render.resolution_x,s.render.resolution_y],'world':list(s.world.color),'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'unit_scale':s.unit_settings.scale_length,'unit_system':s.unit_settings.system}
(root/'outputs/reports/pattern_feasibility/render_settings_inspection.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
