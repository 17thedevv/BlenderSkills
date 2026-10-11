---
name: reference-fidelity-guardian
description: Protect approved character identity and measurable reference fidelity while identifying inferred areas, justified design deviations and human approval gates during 2D-to-3D character work.
---
# Reference Fidelity Guardian — v0.3

## Scope
Design-specific details belong in `config/kagari_design_contract.json` or a per-character file, **not embedded in this generic Skill**. Do not mandate any specific base mesh; recommend using an approved editable base if constructive geometry cannot achieve the likeness.

## Before work
1. Read user concept and approved decisions. Inventory images and their angles/uncertainties.
2. Extract **must preserve** visual identity markers (shape, palette, accessory placement), then editable/inferred areas.
3. Set a local comparison plan: same focal length, approximate crop, view orientation, scale-normalized landmark ratios. Never claim objective 1:1 likeness from a single orthographic/illustrated view.
4. Create a change-impact note: modifying collar should not silently alter facial shape keys or hair; changing hair changes silhouette checkpoint, not automatically invalidating face morph tests.

## Approval checks
- Reference image + candidate render (same view) juxtaposed, with **annotated discrepancies**.
- At least 3 non-trivial silhouette/shape landmarks for edited region (e.g. neckline crossing location, shoulder breadth ratio, sleeve width/profile). Estimate or mark not measurable; do not invent precise measurements.
- For each changed region: `MATCH`, `INTERPRETED`, `MISMATCH`, `NOT_OBSERVABLE`, with evidence path.
- Stop if must-preserve characteristics were altered without user approval; propose the smallest geometry-level correction.
- Separate **human webcam capture quality** from **visual readability of the rendered avatar**. Avatar bangs do not interfere with detection of a user's face by MediaPipe.

## Exit
A signed-off reference delta report linked to exact candidate `.blend` hash and images, or `REQUIRES_HUMAN_REVIEW`. No autonomous artistic PASS.
