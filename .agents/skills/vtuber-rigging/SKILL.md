---
name: vtuber-rigging
description: Creates and validates humanoid VTuber armatures, skin weights, face shape keys and VRM 1.0 expression mapping. Use after mesh approval to enable tracking, lip sync and facial animation.
---
# VTuber Rigging

1. Read installed VRM Add-on documentation/version and verify target app supports intended VRM 1.0 features. Do not invent add-on operator names or UI fields.
2. Bind humanoid rig with validated parent hierarchy and VRM humanoid mappings, including hips, spine, chest, neck, head, left/right upper/lower arms/hands and legs/feet. Additional bones only as required.
3. Apply smooth weights near critical joints. Validate twist and elbow/shoulder extremes; avoid excessive vertex weight influences when not needed.
4. Create face morphs with realistic deltas: `blink`, `blinkLeft`, `blinkRight`, `aa`, `ih`, `ou`, `ee`, `oh`, `happy`, `sad`, `surprised` (minimum can be scoped by brief). If shapes are generated on different mesh objects, document them.
5. Bind them to the VRM 1.0 expression presets using installed add-on API/UI; do not assume matching Blender shape-key names are sufficient. Test expression values at 0, 0.5, and 1.0, including emotion + lip/blink combinations.
6. Test look-at or gaze tracking mode on target runtime. Respect VRM expression override behavior for mouth/blink/look-at to avoid excessive combined deformation.
7. Save rig validation snapshots and input files before export. Do not claim a working VTuber until external import/tracking checks pass.

**Reference:** https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md

**Exit:** rigged `.blend` WIP, bone and expression mapping report, Gate D state.

## v0.2 profile: webcam anime female
- Required VRM 1.0 presets: `blink`, `blinkLeft`, `blinkRight`; `aa`, `ih`, `ou`, `ee`, `oh`; `happy`, `angry`, `sad`, `relaxed`, `surprised`. Use explicit expression bindings and confirm exported JSON data. A `neutral` key may exist but is not a required emotional expression.
- Prefer leftEye/rightEye bones + VRM LookAt bone mode. Expression-mode look directions are conditional alternatives, not automatic duplicates.
- Never add independent head/neck tracking twice (e.g. active head idle and live webcam driver). Tune Warudo mapping per its installed configuration.
- Test `happy+aa`, `happy+blink`, `sad+aa`, `surprised+blink`, and directional eye/look combinations; use per-expression VRM procedural overrides where visually necessary.
- Limit hair dynamics and keep spring bone colliders clear of eyes/cheeks. Stress test ±20° head yaw and ±15° pitch before approval.
