# Reproduce the limited experiment

Run from `D:/Project-17/blender` in PowerShell, using the existing portable Blender. No pip/addon installation is required. The generator checks the exact preserved Recovery v2 SHA before copying only its mannequin/armature. It never saves to that source path.

```powershell
& D:/tools/blender-4.2.0-windows-x64/blender.exe -b --python scripts/build_pattern_feasibility.py -- trial3
& D:/tools/blender-4.2.0-windows-x64/blender.exe -b --python scripts/render_pattern_comparison.py -- trial3
& D:/tools/blender-4.2.0-windows-x64/blender.exe -b outputs/wip/kagari_pattern_trial3_prototype.blend --python scripts/audit_blend.py -- --output outputs/reports/pattern_feasibility/trial3/geometry_audit.json
& D:/tools/blender-4.2.0-windows-x64/blender.exe -b --python scripts/verify_pattern_feasibility.py -- trial3
python scripts/publish_pattern_feasibility.py
python scripts/validate_project_state.py --root . --state config/project_state.json
```

These commands regenerate/overwrite the **experimental** outputs and publish new hashes; keep the delivered hashed files as the reviewed evidence if you want to compare a rerun. `.blend` bytes/cache results and solver time are not claimed bit-identical across Blender builds, machines or threads. All three parameter branches are available: replace `trial3` with `trial1` or `trial2` in the generator to reproduce the rejected variants; use `trial3` for final publication. Baseline comparison is generated separately and is not imported by the prototype generator.

The source scene `outputs/wip/kagari_pattern_trial3_source.blend` contains six planar pattern objects in hidden `2D_PATTERNS_SOURCE_ONLY`, placed fabric panels with loose sewing edges, pin group, native Cloth/Collision settings and the gradual pose timeline. It is saved before solving. Show the pattern collection for cut inspection; hide it again before solving/rendering. The transient cloth cache is not a packaged bake; sequentially rerun frames using the script.

The frozen prototype `outputs/wip/kagari_pattern_trial3_prototype.blend` opens in neutral with `Simulated_neutral` + `Collar_neutral` visible. Other snapshots are hidden. To inspect a stress snapshot, show its matching garment and collar and set the copied upper-arm bone to −38° or 0°, with the opposite arm still +68°. A static snapshot does not respond correctly to arbitrary new poses. `Rig_Only_Neutral_Drape` is the separate armature diagnostic; show it instead of simulated garment for a true ordinary-skinning test. Its weights are a heuristic preview, not production painting. No corrective keys are included.

Mesh positions, metric cut grids, seam pairs and anchors are in `trial3/patterns_and_seams.json`. Cloth settings/timeline/collar construction are in `scripts/build_pattern_feasibility.py`; pose frames and actual seam gaps/timings are in `trial3/simulation.json`; camera transforms, pose angles, PNG hashes and scene SHA are in `trial3/render_manifest.json`. Collar finishing strips are generated **after** draping along the front cut edges, with an inferred nape and exact endpoint seam welds. They are not independently simulated/sewn collar panels; this limitation is part of the failed result.

The original Recovery v2 full-avatar scene remains separate. The study is not a VRM source avatar ready for export.
