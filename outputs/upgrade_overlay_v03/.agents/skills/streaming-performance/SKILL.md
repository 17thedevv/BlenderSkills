---
name: streaming-performance
description: Profile Blender and exported VTuber avatar complexity at object, modifier, material and runtime stages while preserving on-camera facial and garment quality.
---
# Streaming Performance — v0.3

## Stage-aware budgets
1. Profile in three **distinct** domains: Blender raw mesh, Blender depsgraph evaluated mesh, and actual exported VRM meshes/rendered runtime. These are *not interchangeable*.
2. Use `scripts/audit_blend.py` to report raw/evaluated triangles, per-object modifier stacks, largest contributors, object/material counts. Blender modifiers may not survive export or may be applied differently.
3. Before duplicating ornaments, measure one sample's evaluated cost; use texture/atlas for embroidery and gold lines when silhouette does not require geometry.
4. Record runtime settings (Warudo build, render resolution, OBS settings, webcam, FPS, CPU/GPU/VRAM), 1% low if obtainable, warm-up and capture duration. A screenshot without timing/profile is not FPS evidence.
5. Treat 80k tris / 2048px / 8 materials / 30 FPS as *project starting heuristics* until profiled, NOT universal thresholds or pass/fail certification.
6. Optimize largest measured bottleneck first. Keep eyes, face deformations and silhouette-facing clumps at higher quality than rear ornament details.

## Guardrails
- Do not flatten or decimate the face to meet a self-imposed triangle limit.
- Do not claim export counts or FPS based solely on Blender evaluated mesh.
- Document tradeoffs and obtain human artistic approval if optimization materially changes style.

## Exit
Report before/after cost and scene/render settings; actual user hardware test marked `NOT_TESTED` if unavailable.
