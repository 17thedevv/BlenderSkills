# Workflow v0.2 — anime female / webcam VTuber

For an existing project, resume from `config/project_state.json` and its hashed evidence, not the first-run defaults. A user-authorized scoped construction experiment can run while historical head approval evidence is pending; this does not approve the head or permit unrelated modeling/export. `outputs/DELIVERY.md` must mirror that state's current artifact, version and SHA. Legacy booleans in `character_brief.json` are historical metadata only.

Never equate Blender execution with model quality. Preserve original sources, obtain licenses/consent for external assets and installs.

| Gate | Phase | Agent skills | Verifiable evidence | Required human approval |
|---|---|---|---|---|
| S0 | Preflight | base-mesh-strategy, streaming-performance | Blender + VRM Add-on + Warudo and webcam availability; `scripts/check_skillpack.py` | Camera/install permission if relevant |
| A | Character design | character-director | Japanese-anime female identity sheet and license plan, color/silhouette references | Yes — concept before complex modeling |
| B | Head+face prototype | anime-face-specialist, hair-outfit-builder, visual-critic | Actual Blender front, 3/4, side, close-up renders | Yes — face approval |
| C | Body and deformation | topology-expert, base-mesh-strategy | Neutral + stress poses, technical audit, clipping notes | Review as necessary |
| D | Rig and VRM expressions | vtuber-rigging | Humanoid map, eyelid/vowel/emotion morph tests, eye bones LookAt | Yes for expressive face/rig |
| E | Animation | basic-animation-maker, visual-critic | sampled frames, loop seams, expression interactions | Review as necessary |
| F | VRM export | vrm-delivery | `.blend`, `.vrm`, VRM JSON audit, re-import | No auto-PASS based on JSON alone |
| G | Webcam runtime | webcam-tracking | T01–T08 from `docs/WEBCAM_TRACKING_TEST.md` | Yes — webcam live operation |
| H | OBS + performance | live-broadcast-integration, streaming-performance | T09–T11, actual 10-min profile + OBS framing | Yes — delivery |

**First run:** Only S0+A unless pre-existing character concept is approved. Do not create full-body geometry as filler while waiting for design approval. Once concept is approved, the head/face should be worked on before body detail.

**Decision points:**
1. If no approved/usable base mesh: compare candidate licensed bases and a face-only prototype, request user selection; never buy/download without permission.
2. If the selected VRM add-on is incompatible: stop VRM export gate; provide actual version/reason, not fictional API.
3. If agent lacks image inspection: mark visual gate NOT TESTED and request images/user review. Three failed aesthetic iterations → change method or ask human.
4. If live Warudo/webcam isn't accessible: prepare reproducible human test instructions; do not mark runtime PASS.
5. If FPS is below target: profile before compromising face quality; `docs/PERFORMANCE.md`.
6. If user wants automated AI conversations later: add a speech-to-text/LLM/TTS/mouth-driver component only as a separate phase, not part of webcam MVP.
