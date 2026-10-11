"""Blender raw/evaluated geometry audit; NOT a VRM-export or FPS certificate.

Usage:
 blender --background project.blend --python scripts/audit_blend.py -- --output outputs/reports/mesh_geometry_v03.json

Notes:
 - Audits all Blender scene mesh objects (including hidden ones). Visibility flags included.
 - Shape key state and active evaluation context can change evaluated counts.
 - Per-object evaluated geometry is evaluated with current depsgraph, not guaranteed export geometry.
"""

import argparse
import json
import hashlib
import sys
from pathlib import Path

try:
    import bpy
    import bmesh
except ImportError as exc:
    raise SystemExit("Run with Blender Python (blender --python), not system Python") from exc


def triangle_count(mesh):
    return sum(max(len(p.vertices) - 2, 0) for p in mesh.polygons)


def raw_topology(mesh):
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        return {
            "loose_vertices": sum(not bool(v.link_edges) for v in bm.verts),
            "boundary_edges": sum(e.is_boundary for e in bm.edges),
            "non_manifold_edges_including_boundaries": sum(not e.is_manifold for e in bm.edges),
        }
    finally:
        bm.free()


def weights(obj):
    rigs = [m.object for m in obj.modifiers if m.type == 'ARMATURE' and m.object and m.object.type == 'ARMATURE']
    if not rigs:
        return {'status': 'NOT_APPLICABLE' if obj.parent_type == 'BONE' else 'NOT_TESTED', 'reason': 'No armature modifier; may be a rigid or unbound object.'}
    names = {b.name for rig in rigs for b in rig.data.bones if b.use_deform}
    deform_indices = {g.index for g in obj.vertex_groups if g.name in names}
    missing = []; non_normalized = []; excess = []
    for v in obj.data.vertices:
        values = [g.weight for g in v.groups if g.group in deform_indices and g.weight > 1e-8]
        if not values:
            missing.append(v.index)
        elif abs(sum(values) - 1.0) > .02:
            non_normalized.append(v.index)
        if len(values) > 4:
            excess.append(v.index)
    return {'status': 'CHECKED_RAW_WEIGHTS_ONLY', 'deform_group_count': len(deform_indices),
            'vertices_without_deform_weight': len(missing), 'missing_weight_sample': missing[:20],
            'non_normalized_deform_weight_vertices': len(non_normalized),
            'vertices_with_more_than_four_deform_influences': len(excess),
            'single_bone_cloth_warning': obj.get('deformation_role') == 'cloth' and len(deform_indices) <= 1,
            'pose_quality': 'NOT_TESTED'}


def evaluated_count(obj):
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = None
    try:
        me = ev.to_mesh()
        if me is None:
            raise RuntimeError('No evaluated mesh')
        return triangle_count(me)
    finally:
        if me is not None:
            ev.to_mesh_clear()


def modifier_costs(obj):
    flags = [m.show_viewport for m in obj.modifiers]
    stages = []; previous = triangle_count(obj.data)
    try:
        for mod in obj.modifiers:
            mod.show_viewport = False
        for i, mod in enumerate(obj.modifiers):
            if not flags[i]:
                stages.append({'name': mod.name, 'type': mod.type, 'status': 'DISABLED_IN_VIEWPORT', 'triangles': None, 'delta': None})
                continue
            mod.show_viewport = True
            bpy.context.view_layer.update()
            try:
                count = evaluated_count(obj)
                stages.append({'name': mod.name, 'type': mod.type, 'status': 'COUNTED', 'triangles': count, 'delta': count - previous if previous is not None else None})
                previous = count
            except Exception as exc:
                stages.append({'name': mod.name, 'type': mod.type, 'status': 'NOT_TESTED', 'triangles': None, 'delta': None, 'error': str(exc)})
                previous = None
    finally:
        for mod, flag in zip(obj.modifiers, flags):
            mod.show_viewport = flag
        bpy.context.view_layer.update()
    return stages


def audit_obj(obj, depsgraph):
    raw = obj.data
    result = {
        "name": obj.name,
        "raw": {"vertices": len(raw.vertices), "faces": len(raw.polygons), "triangles": triangle_count(raw)},
        "evaluated": None,
        "evaluated_error": None,
        "modifiers": [{"name": mod.name, "type": mod.type, "enabled_render": mod.show_render,
                       "enabled_viewport": mod.show_viewport} for mod in obj.modifiers],
        "materials": [m.name if m else None for m in obj.data.materials],
        "hidden_render": bool(obj.hide_render),
        "hidden_viewport": bool(obj.hide_viewport),
        "hidden_in_view_layer": bool(obj.hide_get()),
        "uv_layers": [l.name for l in raw.uv_layers],
        "shape_keys": [k.name for k in raw.shape_keys.key_blocks] if raw.shape_keys else [],
        "shape_key_values": {k.name: k.value for k in raw.shape_keys.key_blocks} if raw.shape_keys else {},
        "vertex_groups": [g.name for g in obj.vertex_groups],
        "armatures": [m.object.name for m in obj.modifiers if m.type == "ARMATURE" and m.object],
        "topology_raw": raw_topology(raw),
        "weighting": weights(obj),
        "parent": obj.parent.name if obj.parent else None,
        "parent_type": obj.parent_type,
    }
    evaluated = None
    eval_obj = None
    try:
        eval_obj = obj.evaluated_get(depsgraph)
        evaluated = eval_obj.to_mesh()
        if evaluated is None:
            raise RuntimeError("depsgraph evaluated mesh was None")
        result["evaluated"] = {
            "vertices": len(evaluated.vertices),
            "faces": len(evaluated.polygons),
            "triangles": triangle_count(evaluated),
        }
    except Exception as exc:
        result["evaluated_error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if evaluated is not None and eval_obj is not None:
            eval_obj.to_mesh_clear()
    if result["evaluated"]:
        result["triangle_delta"] = result["evaluated"]["triangles"] - result["raw"]["triangles"]
    else:
        result["triangle_delta"] = None
    result['modifier_costs'] = modifier_costs(obj)
    # Legacy consumers still receive raw topology/inventory fields.
    result.update(result['topology_raw'])
    result.update({'vertices': result['raw']['vertices'], 'polygons': result['raw']['faces'],
                   'triangles': result['raw']['triangles'], 'armature_modifiers': result['armatures'],
                   'notes': 'Open shells may legitimately have boundaries; weights and counts do not prove deformation quality.'})
    return result


def main():
    args_raw = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--top", type=int, default=20)
    args = p.parse_args(args_raw)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    report = [audit_obj(o, depsgraph) for o in bpy.context.scene.objects if o.type == "MESH"]
    raw_total = sum(x["raw"]["triangles"] for x in report)
    evaluated_total = sum(x["evaluated"]["triangles"] for x in report if x["evaluated"])
    failed = [x["name"] for x in report if x["evaluated"] is None]
    modifier_failures = [x['name'] + ':' + s['name'] for x in report for s in x['modifier_costs'] if s['status'] == 'NOT_TESTED']
    blend = Path(bpy.data.filepath) if bpy.data.filepath else None
    digest = None
    if blend and blend.is_file():
        with blend.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    arms = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']
    render_visible = [x for x in report if not x['hidden_render']]
    visible_complete = bool(render_visible) and all(x['evaluated'] for x in render_visible)
    payload = {
        "schema_version": "0.3",
        "scope": "all mesh objects in active scene, including hidden scene objects; unused datablocks excluded",
        "blend_file": bpy.data.filepath or "UNSAVED",
        "blender_version": bpy.app.version_string,
        "blend_sha256": digest,
        "evaluation_context": {'depsgraph_mode': depsgraph.mode, 'frame': bpy.context.scene.frame_current,
                               'units': bpy.context.scene.unit_settings.system, 'scale_length': bpy.context.scene.unit_settings.scale_length,
                               'note': 'Counts use current viewport modifier flags/levels; render and export may differ.'},
        "raw_triangles": raw_total,
        "evaluated_triangles_partial_if_errors": evaluated_total,
        "evaluated_complete": bool(report) and not failed,
        "evaluated_triangles": evaluated_total if report and not failed else None,
        "geometry_count_status": 'COUNTED' if report and not failed else 'NOT_TESTED',
        "evaluation_failed_objects": failed,
        "mesh_object_count": len(report),
        "render_enabled_inventory": {
            'scope': 'Objects with hide_render=False; viewport-evaluated counts, NOT final render/export counts. Collection exclusion not simulated.',
            'objects': len(render_visible),
            'raw_triangles': sum(x['raw']['triangles'] for x in render_visible),
            'viewport_evaluated_triangles': sum(x['evaluated']['triangles'] for x in render_visible) if visible_complete else None,
            'status': 'COUNTED' if visible_complete else 'NOT_TESTED'},
        "total_objects": len(bpy.context.scene.objects),
        "mesh_count": len(report),
        "triangle_count_total": raw_total,
        "triangle_count_total_semantics": 'RAW_ONLY_LEGACY_ALIAS',
        "mesh_report": report,
        "armatures": [{'name': a.name, 'bone_count': len(a.data.bones), 'bone_names': [b.name for b in a.data.bones]} for a in arms],
        "actions": [{'name': a.name, 'frame_range': list(a.frame_range)} for a in bpy.data.actions],
        "potential_issues": ([x['name'] + ': missing deform weights' for x in report if x['weighting'].get('vertices_without_deform_weight', 0)]
                             + [x['name'] + ': empty raw mesh' for x in report if not x['raw']['faces']]
                             + failed + modifier_failures + ([] if report else ['No mesh objects in active scene'])),
        "visual_approval": 'NOT_TESTED', "vrm_export_validated": False, "external_vtuber_app_validated": False,
        "modifier_cost_failures": modifier_failures,
        "largest_modifier_expansions": sorted(
            [dict(object=x['name'], **s) for x in report for s in x['modifier_costs'] if s.get('delta') is not None],
            key=lambda x: x['delta'], reverse=True)[:max(0, args.top)],
        "distinct_material_names": sorted({m for x in report for m in x["materials"] if m}),
        "largest_by_evaluated_triangles": [
            {"name": x["name"], "raw_triangles": x["raw"]["triangles"],
             "evaluated_triangles": x["evaluated"]["triangles"], "delta": x["triangle_delta"],
             "modifiers": x["modifiers"]}
            for x in sorted((x for x in report if x["evaluated"]),
                            key=lambda x: x["evaluated"]["triangles"], reverse=True)[:max(0, args.top)]
        ],
        "objects": report,
        "certification": {
            "visual_quality": "NOT_TESTED",
            "exported_vrm_triangles": "NOT_TESTED",
            "warudo_fps": "NOT_TESTED",
        },
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"AUDIT: {out} raw={raw_total} evaluated={evaluated_total} complete={bool(report) and not failed}")
    if failed or modifier_failures or not report:
        print(f"WARN: {len(failed)} evaluated meshes / {len(modifier_failures)} modifier stages unavailable", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
