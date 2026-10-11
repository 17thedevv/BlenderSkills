---
name: webcam-tracking
description: Calibrates and verifies live webcam-driven VRM 1.0 face/head/eye/blink/lip tracking in Warudo MediaPipe. Use after VRM export and when debugging jitter, expression mapping or tracking dropouts.
---
# Webcam Tracking — Warudo MediaPipe

**Prerequisites:** A REAL exported VRM 1.0, compatible installed Warudo, visible webcam consent, user present for calibration. Never assert an app was opened or webcam data reviewed without evidence.

1. Inspect the Warudo version and model version compatibility. Primary path: Warudo onboarding assistant → import `.vrm` → select built-in MediaPipe webcam face tracking; allow it to generate tracking blueprints. Confirm model loads before tuning.
2. Test neutral face, eyes closed, unilateral blink (if reliably detectable), vowel-like mouth motion, smile, brow movement, head yaw ±20°, pitch ±15°, and moderate lateral head motion. Actual tracker capabilities vary with webcam.
3. Verify face/head, eyelids, eye bones and mouth preset mappings. Use the Warudo **VRM blendshape mapping** for VRM presets. Do NOT assume all 52 ARKit/Perfect Sync shapes exist in a basic VRM model; they are an optional advanced target.
4. Configure mirror mode and calibrated neutral pose. Check whether body movement is acceptable; minimize accidental torso bounce and disable redundant idle head animation when camera tracking already drives head motion.
5. Tune tracking filters incrementally: less smoothing for latency, more if jittery. Adjust only one variable at a time, capture short samples and document perceived lag and instability. If facial motion is trapped open or misfires, inspect face mappings and thresholds.
6. Prefer Warudo's built-in MediaPipe to OpenSeeFace initially (official handbook recommends MediaPipe). If webcam tracking quality degrades during gaming/OBS, profile CPU/GPU and experiment with CPU MediaPipe mode; do not silently degrade game FPS.
7. If supported, configure Warudo microphone lip-sync as fallback on tracking loss, testing for mouth override conflicts. Track lost-camera handling (return toward neutral, not frozen expression or extreme pose).
8. Complete `docs/WEBCAM_TRACKING_TEST.md` using **actual observed results**, never synthetic PASS labels. Request a user-provided confirmation if you cannot access live apps/webcam.

**Exit:** user-validated tracking tests with screenshots or explicit observations and outstanding limitations; not a Blender-only success.

References:
- https://docs.warudo.app/docs/mocap/mediapipe
- https://docs.warudo.app/docs/mocap/face-tracking
- https://docs.warudo.app/docs/mocap/overview
