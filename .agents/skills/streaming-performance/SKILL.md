---
name: streaming-performance
description: Profiles and optimizes anime VRM avatar mesh, textures, materials, spring bones, webcam tracking, Warudo and OBS together for stable real-time VTubing. Use before live delivery and after major visual changes.
---
# Streaming Performance

## v0.3 cost accounting

Report three distinct domains: Blender raw geometry, current depsgraph-evaluated geometry and actual exported/runtime geometry. Use the audit's largest objects and cumulative modifier stages to locate expansion; record evaluation context and visibility. An export count or runtime FPS remains NOT_TESTED until measured independently.

Before duplicating ornament, measure one sample at the intended crop, including its evaluated triangles, material/object costs and export compatibility. Prefer textures/atlases for flat embroidery and microdetail. Preserve camera, workload, warm-up/duration and software versions when reporting performance; a screenshot alone is not timing evidence.

1. Treat `config/character_brief.json:model_budget_starting_targets` as starting targets for profiling, NOT strict limits or measured frame rates.
2. Run `scripts/audit_blend.py` on the actual `.blend`. Identify high-triangle hair/clothing, material draw-call proliferation, large textures, duplicate hidden geometry and heavy physics chains; assess image quality before reducing fidelity.
3. Export actual VRM and audit with `scripts/audit_vrm.py`. Profile in Warudo alone, then Warudo + MediaPipe, then Warudo + OBS, then intended game load. Report FPS, 1% lows if measurable, GPU VRAM and CPU/GPU use from real measurements.
4. Optimize in order: unused geometry/textures, extra material slots, spring chains, texture resolution, preview lighting/postprocessing, webcam tracker CPU/GPU placement, then geometry LOD compromises. Never degrade approved face silhouette without another approval.
5. Validate the same animation/tracking tests after every optimization. Report changes and before/after measurements; no unverifiable 'optimized' claims.

**Exit:** performance table with observed metrics or NOT TESTED and clear next checks.
