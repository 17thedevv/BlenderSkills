---
name: topology-expert
description: Audits and repairs deformation-critical Blender mesh topology, normals, skinning readiness, UVs and mesh validity for anime VTuber rigs. Use before skinning and whenever poses break geometry.
---
# Topology Expert

## v0.3 geometry and invariant checks

Record source SHA, mesh names, parent/rig, UV/material inventory and all shape-key coordinates before editing. Compare protected meshes and morph deltas after the change, not just shape-key names.

The audit must retain raw topology checks and report raw and depsgraph-evaluated triangles separately, object/material counts, modifier-stack expansion and failures. Evaluated Blender geometry is not an exported VRM count. Missing evaluations must be null/NOT_TESTED with an error, never a successful zero.

For armature-bound meshes, report vertices without positive weights on deform bones, non-normalized weight sums, excessive influences and invalid armature references. Separate intentional rigid/bone-parented props from deforming cloth. Retain deformable edge flow and verify moderate shoulder/arm movement before detail work.

1. Run `blender --background file.blend --python scripts/audit_blend.py -- --output outputs/reports/scene_audit.json` (after `--help` where supported).
2. Inspect mesh object naming, UV layers, shape keys, missing weights, normal orientations, duplicate overlapping surfaces and triangulation where required.
3. Focus clean deforming edge flow on eyelids, lips, jaw, neck, shoulders, elbows, wrists, hips and knees; quads are preferred where feasible, triangles are not intrinsically forbidden.
4. Preserve all shape keys when editing topology; arbitrary vertex count/order changes can destroy expression deltas. Plan corrective shapes before destructive remesh/decimate.
5. Confirm normals and material zones after modifier application. Apply transforms carefully; armature and shape key data can break if done blindly.
6. Pose-test joints with a matrix of neutral/half/extreme angles; compare visible pinching and clipping with staged preview renders.
7. Non-manifold boundary edges can be intentional for open shells (e.g. eyelid/hair/card meshes): flag for review, do not auto-fix every boundary.

**Exit:** audit JSON, topology risk list, proof of deformation preview, Gate C state. Do not declare 'topology perfect' from one scalar alone.
