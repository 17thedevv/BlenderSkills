---
name: base-mesh-strategy
description: Selects a high-quality licensed VTuber base mesh or feasible Blender modeling approach, with topology and source-provenance checks. Use before creating the anime character body or when procedural results are ugly.
---
# Base Mesh Strategy

1. Evaluate in order: user's own Blender/VRoid/VRM mesh; editable licensed model; VRoid Studio authored base; hand-refined sculpt; fully procedural mesh ONLY for simple props and blockout.
2. For each candidate, record source URL/local path, creator, applicable license, redistribution/commercial/derivative constraints, format, geometry quality and facial blendshape compatibility.
3. Use a side-by-side test: neutral head render, deformability around eyes/mouth/shoulders, shape-key retention, UV/material friendliness, VRM target compatibility.
4. Prefer the best editable base that passes legal + quality gates. Do not blindly rebuild anime face from primitives when a robust base exists.
5. When importing or modifying a model, keep an unmodified `outputs/sources/` copy and separate WIP; never overwrite user-supplied asset.
6. If no approved asset exists, limit automation to coarse blocking, establish face proportion guides, and request a suitable reference or external modeling tool; do not pass low-quality blockout as final art.

**Exit:** `outputs/reports/base_mesh_decision.md`, trusted source manifest with license and scope; proposed implementation plan.
