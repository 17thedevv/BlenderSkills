# Live streaming integration: Blender → VRM → Warudo → OBS

## Primary runtime

```text
Character reference / approved identity
  ↓
Blender source (.blend)
  ├── face shape keys and VRM 1.0 expression maps
  ├── humanoid + leftEye/rightEye bones
  ├── MToon-compatible hair/skin/clothes materials
  └── spring bone chains (limited and tested)
  ↓
VRM add-on export (.vrm), verify and re-import
  ↓
Warudo (Character asset: VRM 1.0)
  ↑                        ↑
Webcam → MediaPipe    Hotkey expressions / optional mic lip sync
         ↓
Calibration + body/head/face mapping / smoothing
         ↓
Warudo scene camera / background
         ↓
OBS capture → livestream/recording
```

**Warudo** documents VRM0/1 support and built-in MediaPipe/OpenSeeFace webcams. Prefer MediaPipe and begin with generated onboarding tracking blueprints. Turn on eye-bone mapping for LookAt if model supports it. Use Warudo's expression hotkeys/overrides rather than rebuilding expression state in Blender at runtime.

**OBS** is not assumed to support a particular capture transparency setting: inspect available scene methods and actually verify (window/game capture, transparency or chroma workflow). Keep webcam and microphone permissions local and explicit.

## Input mapping contracts
- Face: real-time tracking outputs are mapped by Warudo to VRM preset shapes/blendshapes. VRM basic expression mapping is enough for MVP; ARKit 52/Perfect Sync is an optional quality upgrade requiring *model-side morphs*.
- Head: Warudo drives head/neck; avoid separate looping head turns at runtime.
- Eyelids: select auto vs tracking blinking intentionally (no double blink).
- Eye gaze: use bone LookAt in model; test axis/mirror signs.
- Mouth: use webcam-driven lip sync first; optional Warudo microphone lip sync fallback must not double-open the mouth.
- Emotion: mapped preset expression activated from a hotkey, with blink/mouth overrides checked for correct blending.
- Hair physics: runtime spring bone dynamics follow motion; stress test pitch/yaw and neck accessories.
- OBS: present composited output (Warudo scene), not the raw webcam feed unless explicitly desired.

## Future integration with project's own Virtual Character runtime
Only after the off-the-shelf Warudo MVP has been visually approved: investigate runtime VRM 1.0 loader, OSC/VMC or MediaPipe input adapter, independent facial state mixer, and stream output. Do not build a custom engine/bridge as a prerequisite for the MVP; use a thin abstraction `TrackingInput -> Retargeter -> ExpressionMixer -> VRMRuntime` when needed. Preserve the same expression names/mapping and stress-test fixtures.

Sources:
- https://docs.warudo.app/docs/mocap/overview
- https://docs.warudo.app/docs/mocap/mediapipe
- https://docs.warudo.app/docs/mocap/face-tracking
- https://docs.warudo.app/docs/tutorials/data-folder
- https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md
