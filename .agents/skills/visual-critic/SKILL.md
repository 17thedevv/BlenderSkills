---
name: visual-critic
description: Inspects real Blender renders of stylized VTuber models, facial expressions and animation to identify and repair top visual defects. Use at every milestone, never from logs alone.
---
# Visual Critic

## v0.3 traceable construction review

Read [garment and hair review](references/garment_hair_review.md) for construction edits. Review the current version/SHA recorded in project state; reports and DELIVERY must identify that same artifact. Save the candidate before rendering, and verify its hash remains unchanged after temporary render/pose setup.

For garment construction, neutral clay and a relevant pose precede ornamentation. Keep framing, focal length, lights and render settings fixed across baseline/candidate. Separate reference identity, physical construction, material fidelity, deformation and runtime; mark missing evidence NOT_TESTED rather than assigning an aggregate PASS. Inferred side/back forms are not a proven 1:1 reference match.

Each defect needs a region, real image path, root-cause hypothesis, proposed geometry change and predicted visual effect. Log the agent's judgment separately from the human verdict. Do not set APPROVED_BY_USER without linked explicit user evidence and an identified artifact. The current avatar's readability and the human webcam tracking signal are different checks.

## Existing visual evidence requirements

1. Run `scripts/render_review.py` or equivalent to generate actual front, 3/4, side, back and face_close renders. Use identical camera/lights during before/after comparisons.
2. **Inspect each PNG visually** using image-capable viewing tool. If agent cannot view PNGs, STOP, report `VISUAL_CHECK_UNAVAILABLE`, and request human review or tool setup.
3. Compare to approved user reference(s), distinguishing reference fidelity from style quality. Read `docs/QUALITY_RUBRIC.md`; score only assessable categories and mark remaining as N/A.
4. Record top 3 specific flaws with location, evidence file, likely root cause and one surgical fix each. Examples: left eyelid intersects iris at 60% blink; cheek too narrow in 3/4; front bangs cover eyebrows in head pitch.
5. Apply one targeted revision batch, then rerender. Up to 3 repair cycles per gate; escalate to another method/base mesh or ask for guidance beyond that.
6. Do not optimize lighting/camera to hide defects. Use neutral-light technical renders for geometry review and beauty renders for artistic review.
7. Always distinguish automatically checked properties from aesthetic judgments. Save `outputs/reports/visual_review.md` with concrete before/after paths.

**Exit:** genuine reviewed previews, top-issues log, and human approval requirement for subjective face identity.

## v0.2 broadcast-focused review
- Include the OBS-scale portrait crop and face close-up on each design gate; a beautiful full-body render does not prove the webcam-framed face works.
- Flag bangs obscuring eyes, expression shape intersections, asymmetric eyelid motion, hair collisions during head turns, unreadable mouth motion, and face flicker. Do not treat soft focus or aggressive bloom as a fix.
