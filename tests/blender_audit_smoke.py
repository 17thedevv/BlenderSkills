"""Integration test with actual Blender geometry, not model wording."""
import bpy
import importlib.util
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',root/'scripts/audit_blend.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add()
cube=bpy.context.object
cube.shape_key_add(name='Basis')
key=cube.shape_key_add(name='TestDelta')
key.data[0].co.z+=.1
before=[tuple(v.co) for v in key.data]
sub=cube.modifiers.new('TestSubdivision','SUBSURF'); sub.levels=1; sub.render_levels=2
record=m.audit_obj(cube,bpy.context.evaluated_depsgraph_get())
assert record['raw']['triangles']==12,record
assert record['evaluated']['triangles']==48,record
assert record['modifier_costs'][0]['delta']==36,record
assert sub.show_viewport and sub.render_levels==2
assert before==[tuple(v.co) for v in key.data]
assert 'TestDelta' in record['shape_keys']
bpy.ops.object.armature_add()
rig=bpy.context.object
mod=cube.modifiers.new('UnweightedRig','ARMATURE'); mod.object=rig
record=m.audit_obj(cube,bpy.context.evaluated_depsgraph_get())
assert record['weighting']['vertices_without_deform_weight']==8,record['weighting']
print('BLENDER_AUDIT_SMOKE_PASS: raw/evaluated counts, modifier cost, weight warning, shape-key conservation')
