---
name: vrm-delivery
description: Packages and verifies VTuber Blender files, VRM 1.0 avatar expressions and optional separate animation clips for supported streaming apps. Use only after model/rig approvals.
---
# VRM Delivery

1. Confirm installed VRM Add-on supports exact Blender version and VRM 1.0 export. Read locally available exporter API; check required metadata and mapped humanoid bones. No hardcoded imaginary exporter operator assumptions.
2. Backup WIP; save final `.blend`, ensure textures packed/referenced, and export `outputs/character_final.vrm` only if exporter succeeds.
3. Verify file exists and nonzero bytes; re-import VRM in fresh scene with add-on, or test in actual target app. Inspect bone map, material/render compatibility, expression presets and blink/visemes.
4. In tracking app, validate orientation, eye look, neutral pose, mouth sync, blink and clipped accessories. Unsupported apps or unavailable webcam mean `NOT TESTED`, not PASS.
5. Deliver animation clips as distinct assets when target runtime needs them; `.vrm` is chiefly avatar data. No assumption arbitrary Blender Action clips travel in the VRM avatar.
6. Audit provenance/licenses for base meshes, downloaded assets and textures. State redistribution limitations.
7. Write `outputs/DELIVERY.md`: per-gate PASS/PENDING/BLOCKED/NOT TESTED, actual file paths, app+Blender+add-on versions, known defects and necessary follow-ups.

**Exit:** verified character assets with honest compatibility report; Gate F PASS only when target requirements are demonstrated.

## v0.2 additional delivery gates
- Run `python scripts/audit_vrm.py <exported.vrm> --output outputs/reports/vrm_audit.json` and address missing required expression/bone mappings before live testing. This tool validates VRM structure only; it does NOT test mesh aesthetics or in-app compatibility.
- Real Warudo built-in MediaPipe and OBS confirmation is a separate handoff. Use `webcam-tracking`, `live-broadcast-integration`, and `streaming-performance` skills; mark runtime verification NOT TESTED until a webcam operator has checked `docs/WEBCAM_TRACKING_TEST.md`.
