# Kagari Artistic Production — Skills Upgrade v0.3 (overlay)

**This is an additive upgrade overlay, NOT a replacement for your Kagari workspace.** It builds on the accessible Virtual Character v0.2 pack (12 Skills). The user has since reported a **13-Skill local workspace with additional Kagari-specific edits**, which was not uploaded. Do not overwrite those local changes blindly; use `docs/AGENT_MERGE_PROMPT.md` to merge them.

This upgrade targets the observed failure: AI reliably adds meshes, materials and ornamentation but creates weak garment silhouettes, stiff layered collars, flat rear hair and excessive evaluated geometry. It prioritizes fabric and hair *construction*, then visual evidence and artifact traceability.

## Overlay contents

- Five strengthened/new Skills: `hair-outfit-builder`, `reference-fidelity-guardian`, `visual-critic`, `topology-expert`, `streaming-performance`.
- Modeling references: garment construction, anime hair, material vs geometry, acceptance rubric and pose tests.
- `config/kagari_design_contract.json`: Kagari-specific approved/required **visual descriptors** (not fabricated measurements).
- `config/project_state.template.json`: source-of-truth template; NO claim that any current candidate exists.
- `scripts/audit_blend.py`: raw & modifier-evaluated geometry totals, per object and warnings. Requires Blender.
- `scripts/validate_project_state.py`: separate artifact/evidence gate validation, file existence/hash checks. Requires Python only.
- `scripts/check_overlay.py`: checks package structure/frontmatter/config; NOT production/quality approval.
- `docs/AGENT_MERGE_PROMPT.md`: task prompt to merge into existing Kagari repo safely; run ONE garment blockout iteration only.
- `docs/TEST_PROTOCOL.md`: small A/B evaluation strategy and sign-off instructions.

## Apply safely

1. Back up / commit your local Kagari workspace first.
2. Compare `SKILL.md` updates with the 13 local Skills (do not replace local art direction with generic instructions).
3. Merge references and code after inspecting existing scripts and Blender/VRM versions; preserve working changes.
4. Link the real concept to `config/kagari_design_contract.json` and populate artifact and evidence paths only when they exist.
5. First experiment: **collar + upper torso clay blockout**, not entire avatar, new textures, or full hair replacement.
6. Get visual human approval before spending time on embroidered details and full garment construction.

## Hard constraints

- Semantic geometry before ornamentation. **Geometry cost does not imply artistic quality**.
- Never call a mesh good solely because scripts run, normals are valid, or a file exists.
- Ratings are **judgment aids**, not aesthetic ground truth; the user is final art director.
- Keep avatar readability and human webcam tracking input explicitly separate.
- Images with unknown rear/side geometry cannot support claims of exact 1:1 fidelity.
- `audit_blend.py` evaluated triangles are not exported VRM triangle counts or FPS measurements.

Run structural checks: `python scripts/check_overlay.py`.
Run project-state validation only **after configuring project_state.json**: `python scripts/validate_project_state.py --state path/to/project_state.json --root path/to/workspace`.
