---
name: hair-outfit-builder
description: Construct convincing anime hair and layered stylized garments in Blender using shape-first reference-driven modeling, verifiable cloth seams and folds, and controlled real-time geometry cost.
---
# Hair & Outfit Builder — v0.3

## Trigger
Use for hairstyle, collar, sleeves, kimono-inspired torso layers, bows, trim, embroidery, and any modification that changes character silhouette or deformation. Read approved character-specific config, **not hardcoded geometry recipes**.

## Inputs & invariant
- Required: concept and approved constraints, source `.blend` backup, chosen base mesh, active camera(s), Blender version, current state and any existing armature/shape keys.
- Never recreate a model from scratch without a documented reason. Never destroy the neutral face, facial morphs, eye rigs, skinning, original user assets or unrelated objects.
- Before modeling, identify in the reference: **visible vs inferred** structures, structural layers (garments) vs graphic decorations, asymmetries, anchor points, cloth slack and gravity directions.
- Refer to `references/kimono_garment_construction.md`, `references/anime_hair_form.md` and `references/materials_vs_geometry.md` as needed. Do not load all files for unrelated tasks.

## Workflow
1. **Decompose** into meshes/subassemblies with names and attachment logic: inner undergarment, left/right crossed collar, outer robe, sleeve openings, sleeve body, waist transition, trim, embroidered panels, bow, hair cap/locks/ponytail. Draw a simple layer ordering diagram and collision map.
2. **Grey-clay silhouette blockout** with only structural geometry. Front/3⁄4/profile/back at matched framing. No gold piping, stars, embroidery, beads, bloom or beauty lighting. If the garment reads as painted strips or the hair as sheets, stop and rebuild those surfaces.
3. **Garment volume and construction**: preserve seams; collar edges must have believable thickness and follow neck/chest in 3D; construct sleeves as garment volumes with openings and folds instead of undifferentiated torso shells. Use manual modeling, curves/surfaces, shrinkwrap with clearance or cloth-supported workflows as appropriate; no single algorithm is mandated.
4. **Pose and collision smoke tests**: neutral, arms lowered, moderate arm raise, head yaw ±30° where appropriate. Compare collar, shoulder, ponytail and bow. Reject detached collar floating above skin, hard self-intersections, hair scalp gaps, inverted normals and unnaturally rigid fabric deformation.
5. **Hair clumps**: cap/roots + major volume + secondary clumps + accents. Avoid repeated parallel rectangular sheets, cut-flat ends, giant unbroken hair curtain and an exposed scalp shell. Read `references/anime_hair_form.md`.
6. **Materials only after approved shape**: MToon-compatible toon base; use texture/UV for flat embroidery and microdetail. Geometry for jewelry, true hems, buttons and silhouette-changing elements only. First test one representative material and ornament on VRM export/reimport when tooling exists.
7. **Cost check**: audited raw and evaluated triangles, top expanding modifiers, objects/material counts. Design within a profiled budget rather than treating a soft 80k target as an absolute threshold. See `streaming-performance`.
8. **Art-directed iteration**: list 3 highest-impact form defects; revise one region at a time; no more than 3 unproductive cycles before escalating to better base/pattern-driven or manual method.

## Stop rules
- No ornament detail until *clay* is approved.
- No global remeshing/decimation on face or morph targets without tested backups and explicit approval.
- If the current mesh's topology/shape makes fidelity implausible, report evidence and alternatives; do not conceal failure under more vertices.

## Exit evidence
- Saved `.blend` candidate and SHA256 in project state.
- Clay front/3⁄4/profile/back + one relevant pose render with consistent camera/light between iterations.
- Garment component list, pose issues, raw/evaluated counts, real warnings and next proposed change.
- Human **PASS/FAIL/NOT_REVIEWED** decision for appearance. Never self-approve an unreviewed garment.
