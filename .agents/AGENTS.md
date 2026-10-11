# Virtual Character v0.3 — Anime Webcam VTuber agent contract

Goal: One original Japanese-anime-style **female** VTuber, live webcam face tracking, using Blender source + VRM 1.0 + Warudo MediaPipe + OBS. This is NOT a general Blender procedural modeling experiment.

1. Open `config/project_state.json`, `config/kagari_design_contract.json`, `config/character_brief.json`, `docs/WORKFLOW.md`, `docs/MODEL_RIG_ARCHITECTURE.md`, `docs/INTEGRATION_ARCHITECTURE.md`; load the one or two relevant `.agents/skills` for the current phase (progressive disclosure).
2. Prioritize: expressive face / silhouette / bangs > eye/brow/lip deformation > upper body / clothing > full body > minor accessories. Choose licensed editable base over primitive-mesh procedural-from-zero if visual quality is better.
3. NO fabricated art, render images, app tests, FPS metrics, benchmark scores, webcam observations, shape-key mapping or exported model. Code execution success is NOT aesthetic success. Use actual images and human approval for concept and face.
4. All external assets require verifiable provenance/permission for modification and commercial streaming/redistribution as needed; do not download/install/exe untrusted code without user's authorization. Preserve old .blend source files and independent WIP snapshots.
5. Always use VRM 1.0 expression presets and explicit bindings: blink/bilateral, five vowels, five primary emotions. Eye bones for LookAt. ARKit 52/Perfect Sync is optional, not a prerequisite. Do NOT invent nonexistent addon API/operator names.
6. Webcam and OBS access require real user-local session and app permissions; if not accessible, provide human test checklist and mark gates NOT TESTED rather than pretending live tests passed.
7. Iterate at most three aesthetic repair rounds per gate. Identify top 3 real visual defects from neutral-light render and fix surgically; do not hide poor geometry with lighting.
8. No detailed full-body modeling until human Gate B face approval. Stop after critical quality or license blockers. Use `outputs/DELIVERY.md` for PASS/FAIL/NOT TESTED/PENDING.
9. Preserve performance budgets as starting targets; optimize based on Warudo/OBS measurements, not artificial mesh count thresholds.
10. Resume from `config/project_state.json`, not a stale first-run instruction. Preserve explicit user task scope. Authorized construction experiments may make a new WIP before art approval, but remain REQUIRES_HUMAN_ART_REVIEW and cannot unlock ornamentation/export. Reconcile DELIVERY artifact/version/SHA after each saved candidate. Historical reports are evidence records, not automatic user sign-off.
