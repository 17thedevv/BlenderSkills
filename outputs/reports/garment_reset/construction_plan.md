# Garment strategy reset — plan before mesh authoring

Source: `outputs/wip/kagari_v03_clay_03.blend`, SHA256 `4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051`.
Reference: `outputs/design/concept_option2_kagari.jpg`. Only its visible front construction is observed; sleeve pattern/back cut are inferred for the experiment.

Build a separate duplicate mannequin and copied armature in a new file. Do not edit/reuse the rejected robe, sleeve, collar or obi meshes. No Face/Hair/rig edits in the character source. The full avatar remains the approved identity source, not replaced by the mannequin prototype.

## Method choice

Use Blender-native rectangular-panel modeling with explicitly shared/welded seam vertices, followed by a short Cloth drape with mannequin collision and pinned shoulder/neck anchors. Freeze a settled mesh, preserve panel-grid topology, bind it to the duplicate humanoid armature, and test an ordinary arm raise. Keep the simulation setup and flattened panel outlines separately so the construction is reviewable.

This hybrid is simpler than installing a specialist application. Pure free cloth sewing adds solver instability and is unnecessary for an already known seam pattern; pure posed cylinders cannot supply meaningful hanging sleeve material. A live Blender Cloth solver is not a portable VRM feature: the actual deliverable is its static settled surface plus conventional skin weights. Any corrective morph or further motion system requires later testing.

## Limited pieces and seams

- Support only the upper torso needed by the neckline and one shoulder connection. No skirt, obi, second sleeve, jewelry or complete outfit rebuild.
- Construct the left/character-positive-X sleeve from front and back broad rectangular sheets. Close their lower hanging edge and distal seam except a wrist aperture; the large lower bag stays below the arm, rather than using circular radial tube rings.
- Use a drop-shoulder seam at the outer end of the torso/yoke panel. Match vertex counts and weld/bridge front/back seam vertices. Include armpit slack rather than collapsing all seam weights onto a single bone.
- Upper sleeve seam follows the arm only near the top. Lower panel edge is primarily gravity draped and gains folds from shoulder/root/wrist tension, not periodic decoration.
- Build a collar as the boundary of overlapping front garment panels, with a continuous nape bridge. Character left front passes over right front; locate a real depth separation at the chest crossing. The collar outer edge follows the garment-panel contact seam, with a slightly rolled thin section.
- Pin the neckline/shoulder structural anchors and arm-top attachment, not the entire surface. Drape front/back and the sleeve bag using collision clearance. Initial cloth must start outside the mannequin.
- No subdivision modifier, detailed folds, colors/textures, trim or embroidery. Neutral gray, modest Solidify only after drape.

## Evidence and acceptance

Record a standalone raw panel scene, settled prototype, source SHA, seam/pin/solver settings, static mesh counts, weights and modifier costs. Compare Cycle 03 and prototype on the same bare mannequin for matched framing; retain all eight original render paths as failure evidence. Render front, 3/4, profile, back and a 30-degree additional upper-arm raise. Also retain a rig-only arm-pose image if any later corrective or drape adjustment is needed so it is not confused with ordinary skinning.

Inspect real images and report acceptance per criterion. Normalized weights or successful rendering cannot approve the form. Stop for human review before ornament or integration into Kagari.
