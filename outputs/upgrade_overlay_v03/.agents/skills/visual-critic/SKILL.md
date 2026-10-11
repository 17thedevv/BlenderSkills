---
name: visual-critic
description: Critique actual multi-view Blender renders against approved art references with reproducible cameras, ranked form defects, artifact hashes and human visual acceptance gates.
---
# Visual Critic — v0.3

## Highest priority
A technical PASS is not an aesthetic PASS. Real visuals, geometry source and human approval are required. **Grey clay** silhouette review precedes details and lighting effects. Follow `references/garment_hair_review.md`.

## Each review cycle
1. Validate candidate path and SHA256 in project state; render only this immutable candidate/version. Refuse stale `DELIVERY.md` links.
2. Inspect actual PNGs by vision-capable agent UI; if images cannot be opened mark `VISUAL_CHECK_UNAVAILABLE`, not PASS.
3. Render neutral material front, 3⁄4, side, back, portrait crop, relevant deformation pose. Keep camera scale/focal/framing and lighting consistent for before/after; use standardized thumbnail sheets for comparison. When matching 2D art perspective is uncertain, state uncertainty.
4. Separate tests: (a) concept fidelity, (b) shape/construction, (c) material fidelity, (d) animation deformation, (e) runtime. Mark categories **NOT_TESTED** if evidence is missing.
5. Rank *three* most consequential defects, each with location, evidence, root-cause hypothesis, suggested edit and predicted effect on silhouette. Prefer correcting geometry over applying shader polish.
6. Make ONE targeted change batch, then rerender same views. Reject an unreviewed edit as source of a claimed improvement.
7. After 3 visually ineffective attempts, STOP and propose a different base mesh, garment pattern/construction, controlled manual art pass or better tool; no endless blind iteration.
8. Log human verdict separately from model self-assessment. Do not let agent set `APPROVED_BY_USER` unless there is linked user approval evidence.

## Misleading shortcuts to reject
- More modifiers/triangles/ornaments ≠ more appealing garment.
- Camera angle cropping out shoulder intersections ≠ fixing them.
- AO/bloom increasing perceived contrast ≠ corrected geometry.
- Viewer face tracking signal and the avatar's expression legibility are separate.
- Polygon audit or VRM parser success ≠ proven OBS tracking.

## Exit
Write version-specific visual report with candidate SHA, exact render paths, consistent render settings, top defects, decisions and pending human approval. No pass from scripts alone.
