# v0.3 Skill Quality Evaluation — Controlled Test

## Purpose
Determine whether v0.3 procedures improve **geometric construction and visual quality**, rather than measuring amount of code/mesh generated.

## Controlled comparison
Use the **same Kagari concept, same existing base mesh, same model/agent, same Blender build and saved camera lighting**, and similar execution budget for two experiments:

- A — baseline local skills and a collar/shoulder clay garment edit.
- B — local skills with v0.3 references/gates and the SAME collar/shoulder clay edit.

Do not run both edits on the same mutated `.blend`; branch from independent copies of baseline. Do not reuse the A result as input to B. Freeze references and design contract.

## Evidence
Both A and B must produce candidate blend/hash and neutral clay front, 3/4, side, back, moderate arm pose images; Blender raw/evaluated triangle audit; model output log; durations and calls if available; visible defects. No aesthetic claims without a vision review.

## Human blind review
Show comparable before/after images in shuffled anonymous order. Ask reviewer to judge separately: form silhouette, collar physical layering, sleeve/shoulder construction, hair untouched as expected, reference identity, pose integrity. Note if differences are negligible; do not force preference.

## Success definition
Consider B promising only when a human prefers its **structural quality**, it has no new critical pose regression, and evaluated geometry growth is explainable. Lower triangles alone do not imply beauty. A score is only a rubric aid.

## Go/no-go after 3 tries
If both versions are still poor after at most 3 substantive clay edits, do NOT endlessly inflate Skills. Change the modeling primitive/tool: garment sewing patterns + cloth simulation, a professionally constructed licensed base garment, direct GUI modeling with artist intervention, or specialized 3D generation+retopology. Record this as **representation/tooling bottleneck** candidate, not proof that the LLM itself is unintelligent.

## Reporting statuses
`STRUCTURE_CHECK_PASS` / `ASSET_VALIDATION_PASS` / `VISUAL_REVIEW_PENDING` / `HUMAN_APPROVED` are distinct stages. No broad `PASS` without stating which checks actually ran.
