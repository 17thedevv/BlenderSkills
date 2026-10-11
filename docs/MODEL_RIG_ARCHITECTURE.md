# 3D Model, Humanoid Rig and Expression Architecture — female anime webcam avatar

## Design priorities
The subject is one **original female anime Japanese-style VTuber**. Character name, hairstyle, costume and palette require user approval. Prioritize human-readability in webcam portrait crop. Avoid equating high-poly with beauty.

- **Model build:** use properly licensed VRoid Studio base or an editable base mesh if possible. Document origins and derivative rights. A Blender procedurally sculpted fallback is allowed only if the agent can show significantly better evidence than a chosen base. Never present borrowed characters as original.
- **Blender source hierarchy** (suggested collections): `00_REFERENCE` (linked only; licenses in docs), `10_BODY`, `20_HEAD_FACE`, `30_EYES_TEETH`, `40_HAIR`, `50_OUTFIT`, `60_ARMATURE`, `70_PHYSICS_HELPERS`, `80_LIGHTS_CAMERAS`, `90_DEBUG` (not exported). Each active mesh has descriptive names and sensible transforms.
- **Face:** upper/lower eyelid geometry/shape keys must blink without iris penetration. Test a 3/4 portrait; angular anime eyeballs/pupils may need curve-shaped eyelid deformations. Preserve comfortable neutral expression. Use neutral tech light AND beauty light for reviews.
- **Hair:** coherent large clumps, readable bangs, no camera occlusion of eyes, limited controllable side locks. Physically simulate only chosen strands with spring bones and colliders to avoid clipping; never blanket-apply physics to every hair strand.
- **Outfit:** clean cel-shaded materials (MToon when export/runtime support confirmed), no unlicensed brands; avoid dangling accessories crossing head/neck tracking range.
- **Topology:** loops around lids, corners of mouth, neck, shoulders, elbow. Surface quality matters more than raw non-manifold counts (open eyelid shells may be intended). Tests must reveal actual deformation.

## Rig architecture
`Armature[hips → spine → chest → upperChest? → neck → head; left/right shoulder → upperArm → lowerArm → hand; upperLeg → lowerLeg → foot; toes optional]` with VRM humanoid mapping. Use supported optional bones `leftEye`, `rightEye`, fingers as needed. A single runtime head driver, avoid double-applying head pose to a Blender idle action. Add optional accessory/hair bone chains isolated from humanoid joints. Verify T-pose/rest orientation against VRM exporter.

## VRM 1.0 expressions
**Required preset mappings**: `blink`, `blinkLeft`, `blinkRight`, `aa`, `ih`, `ou`, `ee`, `oh`, `happy`, `angry`, `sad`, `relaxed`, `surprised`. `neutral` optional and not used as main blend driver. Other preset `lookUp/lookDown/lookLeft/lookRight` are needed only when LookAt expression mode (instead of bone mode) is used.

- Names alone are not enough: shape keys must be bound to VRM 1.0 `expressions.preset` via the VRM add-on, with proper morphTargetBind indices/mesh links on export.
- Use correct expression override settings and test `happy + aa + blink`, `sad + mouth`, `surprised + blink`. Some emotional expressions should suppress competing procedural blink/mouth; decide per-expression from visual evidence.
- Keyframes for expressions should not be mistaken for real-time tracking data. Webcam provides rotation/blendshape weights during run time; Blender Actions primarily serve authored non-tracking animations.
- **Two tiers:** MVP basic VRM expression set; advanced ARKit/Perfect Sync only if user requests realism, base mesh supports it, tracking can map it, and visual improvements are demonstrated. MediaPipe exposing multiple tracking channels does NOT magically produce 52 matching model morphs.

## Animation
`idle_loop` (subtle breathing through torso, no duplicated tracked head motion), `nod` and `wave` as optional separately controlled Actions. Blink is primarily driven by real-time tracking/Warudo. Verify animation blending; VRM avatar does not automatically store arbitrary Blender Action clips. Explore separate `.vrma` ONLY after confirming the exporter and target runtime can consume it.

## Technical acceptance
1. Neutral portrait front/3-4/side and approved face close-up in actual Blender renders.
2. Shape keys at 0/0.5/1, and combinations. Head yaw/pitch, shoulder/wave pose, and hair clipping stress tests.
3. Humanoid mappings and VRM JSON extension verified by `scripts/audit_vrm.py`, plus re-import/application runtime check.
4. Webcam live test in Warudo: eyes, mouth, head, expression hotkeys and dropouts. OBS scene verified separately.
