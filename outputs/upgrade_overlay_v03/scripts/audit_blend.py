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
        "uv_layers": [l.name for l in raw.uv_layers],
        "shape_keys": [k.name for k in raw.shape_keys.key_blocks] if raw.shape_keys else [],
        "vertex_groups": [g.name for g in obj.vertex_groups],
        "armatures": [m.object.name for m in obj.modifiers if m.type == "ARMATURE" and m.object],
        "topology_raw": raw_topology(raw),
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
    return result


def main():
    args_raw = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--top", type=int, default=20)
    args = p.parse_args(args_raw)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    report = [audit_obj(o, depsgraph) for o in bpy.data.objects if o.type == "MESH"]
    raw_total = sum(x["raw"]["triangles"] for x in report)
    evaluated_total = sum(x["evaluated"]["triangles"] for x in report if x["evaluated"])
    failed = [x["name"] for x in report if x["evaluated"] is None]
    payload = {
        "schema_version": "0.3",
        "scope": "all Blender data objects with type MESH; hidden/unused objects may be included",
        "blend_file": bpy.data.filepath or "UNSAVED",
        "blender_version": bpy.app.version_string,
        "raw_triangles": raw_total,
        "evaluated_triangles_partial_if_errors": evaluated_total,
        "evaluated_complete": not failed,
        "evaluation_failed_objects": failed,
        "mesh_object_count": len(report),
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
    print(f"AUDIT: {out} raw={raw_total} evaluated={evaluated_total} complete={not failed}")
    if failed:
        print(f"WARN: {len(failed)} objects failed depsgraph evaluation", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
