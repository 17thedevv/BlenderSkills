# Clay Review Rubric — Artistic Gate (Kagari)

Every criterion is scored 0, 1, 2, or `NOT_OBSERVABLE` based on **actual images**. The numbers guide discussion, not automated artistic truth. Approval rests with user.

| Criterion | 0 (reject) | 1 (revise) | 2 (candidate) |
|---|---|---|---|
| Garment silhouette | Reads as armor, decal or blob | Key cloth masses identifiable but proportion wrong | Layered robe reads in front, 3/4, side |
| Collar construction | Flat X of strips floating on chest | Partly shaped with odd joins | Crossed depth, believable attachment, edge thickness |
| Sleeves & shoulders | Detached, rounded solid shoulder | Seam visible but sleeve volume stiff | Sleeve opening and drape coherent across views |
| Cloth folds | Random noise or no folds | Some folds but inconsistent anchors | Major folds motivated by seams, tension, gravity |
| Hair silhouette | Flat sheet/scalp holes | Masses exist, tips awkward | Distinct clumps, root flow, soft volume, tapered ends |
| Ref identity | Core signature lost | Similar palette, major mismatch | Key motifs intact in observed views |
| Deformation | Severe clipping/inversions | Minor correctable collisions | Stable for target head/arm test poses |

**Hard reject regardless of score:** missing major approved character motif, major detached clothing, visible exposed scalp from error, missing required evidence, stale artifact, or critical arm deformation. If reference lacks rear/side view, do NOT claim perfect correspondence there.

## Recommended evidence set
- `front_clay.png`, `three_quarter_clay.png`, `side_clay.png`, `back_clay.png`, `pose_shoulder_clay.png`
- `portrait_crop.png` for VTuber readability
- `before_vs_after.png` with matched camera/lights/scale
- `visual_review.json` recording each issue with specific region and fix

The agent may propose revisions but cannot self-sign aesthetic PASS on behalf of user.
