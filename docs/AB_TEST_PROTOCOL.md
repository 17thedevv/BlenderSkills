# Model comparison: Gemini 3.8 Flash vs GPT-6.1 Sol

**Purpose:** compare actual VTuber production quality, not general coding benchmarks.

## Controlled conditions
- Same *approved* concept, asset licenses, Blender version, add-on version and starting `.blend`.
- Same skillpack, same time/iteration cap and identical camera positions.
- One task each: (A) fix anime face silhouette, (B) build/repair five viseme shape keys with correct VRM mapping, (C) create idle loop and remove shoulder clipping.
- Each model receives identical reference images and pass/fail criteria. Note that access to tooling (Blender/MCP) must be equivalent; if Sol is only in Codex and Flash in Antigravity, compare workflows rather than asserting isolated model quality.
- Require exact render and scene JSON evidence. No comparison from unverified completion text.

## Scorecard (0–5 each, assessed by a human with blinded model names)
- Reference fidelity of face and hair: 35%
- Visible quality of animation and expression: 25%
- Rig/geometry validity (technical tests): 20%
- Completion reliability and reproducibility: 10%
- Total consumed money/time: 10% (normalize appropriately; less is better)

Do 2–3 attempts per model if affordable. Track subjective blind preference separately from the numeric rubric. Document each model's settings, context, wall time, tool failures and number of repair rounds.

## Decision
Use Flash for production when it reaches acceptable quality after at most 3 repair rounds; call stronger model or redesign the base mesh when artistic quality plateaus. A model coding benchmark is not enough evidence for a 3D artistic win.
