# Virtual Character — Anime Female Webcam VTuber Skillpack v0.3 merge

A purpose-built **Antigravity Skills + Blender QA** package for an anime-style female VTuber with **VRM 1.0, Warudo built-in MediaPipe webcam tracking, and OBS broadcast capture**. It is an orchestration and validation pack; it **does not contain a finished character**.

## Quick start
1. Unzip into the root of a **Virtual Character project workspace** (the `.agents/skills` path must be beneath workspace root).
2. Review/edit `config/character_brief.json`: name, hairstyle, references/licenses, palette, camera and target apps. Female/anime/webcam/Warudo/VRM1 defaults are filled, not the identity details.
3. Run `python scripts/check_skillpack.py` locally. Then paste `docs/ANTIGRAVITY_PROMPT.md` into Antigravity. Agent should do S0 + art-direction only until you approve the concept.
4. After modeling, agent uses `scripts/audit_blend.py` and `scripts/render_review.py` **inside Blender**, then `python scripts/audit_vrm.py outputs/character_final.vrm --output outputs/reports/vrm_audit.json` after VRM export.
5. Test webcam and OBS manually if the agent cannot access desktop; see `docs/WEBCAM_TRACKING_TEST.md`. Only actual passes count.

## Architecture
`Blender -> VRM 1.0 -> Warudo MediaPipe + webcam -> Warudo scene -> OBS`. Start with a licensed high-quality anime base and invest in face and hair; use eye bones for gaze and standard VRM expression presets. Advanced ARKit/Perfect Sync is optional. Use Warudo-generated setup blueprints, not a custom face-tracking backend for MVP.

## Skills (13; verified by scripts/check_skillpack.py)
`character-director`, `base-mesh-strategy`, `anime-face-specialist`, `hair-outfit-builder`, `topology-expert`, `vtuber-rigging`, `basic-animation-maker`, `visual-critic`, `vrm-delivery`, `webcam-tracking`, `live-broadcast-integration`, `streaming-performance`, `reference-fidelity-guardian`.

The v0.3 overlay is merged additively into the local 13-skill pack. Generic construction guidance lives in Skills/references; Kagari identity lives in `config/kagari_design_contract.json`. `config/project_state.json` identifies the current artifact/version/SHA and evidence. `outputs/DELIVERY.md` is reconciled with that state. A valid state is not human art approval.

Run `python scripts/check_skillpack.py` for structural checks, `python scripts/validate_project_state.py --root . --state config/project_state.json` for artifact/evidence checks, and `python -m unittest discover -s tests -v` for validator regression tests. Blender audit distinguishes raw/evaluated geometry and leaves VRM/runtime certification NOT_TESTED.

## Useful docs
- `docs/MODEL_RIG_ARCHITECTURE.md` — collections, humanoid map, expression tier and stress tests
- `docs/INTEGRATION_ARCHITECTURE.md` — tracking/mapping, Warudo→OBS, future modularization
- `docs/WORKFLOW.md` — S0/A–H stage gates
- `docs/WEBCAM_TRACKING_TEST.md` — actual operator verification checklist
- `docs/PERFORMANCE.md` — initial budget and measured performance protocol
- `docs/QUALITY_RUBRIC.md` — visual QA and hard blockers
- `docs/ANTIGRAVITY_PROMPT.md` — primary copy-paste handoff

## Tool verification
```
python scripts/check_skillpack.py
blender --background outputs/character_wip.blend --python scripts/audit_blend.py -- --output outputs/reports/scene_audit.json
blender --background outputs/character_wip.blend --python scripts/render_review.py -- --output-dir outputs/previews
python scripts/audit_vrm.py outputs/character_final.vrm --output outputs/reports/vrm_audit.json
```
The Blender commands require Blender and an actual `.blend` file. `audit_vrm.py` is a structural analyzer, **not proof that the avatar looks good, imports, tracks or streams correctly**.

## Reference URLs
- Antigravity Skills: https://antigravity.google/docs/skills
- VRM Blender Add-on: https://vrm-addon-for-blender.info/en-us/
- VRM 1.0 expressions: https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md
- Warudo: https://docs.warudo.app/docs/mocap/overview
- Warudo face tracking: https://docs.warudo.app/docs/mocap/face-tracking
- Warudo webcam MediaPipe: https://docs.warudo.app/docs/mocap/mediapipe
