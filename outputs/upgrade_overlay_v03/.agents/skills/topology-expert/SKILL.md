---
name: topology-expert
description: Audit and improve Blender character mesh topology, weights and pose deformation without damaging face morphs or mistaking raw geometry for modifier-evaluated geometry.
---
# Topology Expert — v0.3

## Geometry integrity
1. Back up source scene and record mesh object names, parenting, armature, shape keys, material slots and UV before edits.
2. Identify topology needs **by function**: flexible face/eyelids/mouth, shoulders/elbows, garment seam/fold areas, rigid pendants, hair clumps. Use only necessary loops; avoid topology density increases on flat ornaments.
3. Run `scripts/audit_blend.py` (overlay version) and compare both **raw mesh** and **depsgraph-evaluated mesh** triangle counts. Locate top expanding modifiers and expensive repeated objects. The evaluated count is not exported VRM count.
4. For each weighted mesh: check for vertices unassigned to required deform groups (rig-dependent), extreme weights and armature modifier order. Shape-key conservation requires comparing key names, key deltas and sample expressions before/after.
5. Pose smoke-tests, not just neutral checks: shoulder modest rotation, head yaw, eyelid + mouth combined shape keys; render to expose unacceptable intersections.
6. Distinguish legitimate fabric open boundaries from unwanted non-manifold defects; do not blindly close all garment openings.

## Forbidden shortcuts
- Apply destructive remesh/decimation to face mesh with shape keys unless explicitly authorized after tested backup.
- Claim mesh quality from a triangle budget alone.
- Count `obj.data.polygons` as modifier-evaluated geometry.

## Exit evidence
Raw/evaluated totals, top objects/modifiers, shape-key inventory delta, pose renders, any unapplied modifiers with justification, and unverified export assumptions.
