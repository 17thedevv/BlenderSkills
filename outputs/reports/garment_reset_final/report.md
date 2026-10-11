# Kagari — garment strategy reset: reviewed prototype

**Decision: REQUIRES_HUMAN_ART_REVIEW. Full artistic acceptance: FAIL.**
The construction method has changed; the rejected Cycle 03 meshes were not polished or used to generate this new garment. Three independent panel/drape configurations were investigated. The first configuration is retained for the clearest wide-sleeve method comparison; later configurations are shown and rejected. No ornaments or full-character reconstruction.

## Method and scope

New overlapping front sheet panels, back support, sewn shoulder bridge and one wide front/back sleeve bag. Explicit shared vertex indices/bridge faces establish seams. Blender-native Cloth with Collision/self-collision runs for 65 sequential frames on a copied mannequin. The frame-65 surface is frozen into a conventional rigged mesh; equilibrium/convergence was not certified. A final continuous collar nape bridge shares vertices with both real front-panel collar leaves. Thickness is 1.6 mm at the existing meter scale, without subdivision.
The duplicate mannequin has arms 30 degrees below horizontal; the acceptance pose raises its left arm by 30 degrees to horizontal. Rendered pose is ordinary skinning only, with no live Cloth or pose-corrective morph. Original Kagari Face/Hair/morphs/rig are not edited; the source .blend SHA remains unchanged.
[Failure analysis and tool/method comparison](../garment_reset/failure_analysis_and_method.md) includes all six construction failures, installed-tool evidence and official Blender sources. [Plan before geometry](../garment_reset/construction_plan.md).

## Actual files and hashes

- Selected sewn prototype: [outputs/wip/kagari_panel_drape_reset_final.blend](../../wip/kagari_panel_drape_reset_final.blend); SHA256 `bd8e9adbe4a38b77facc32449f44d0627dd01bdbebe8fe81181344c7ea3f17a2`
- Original rejected Cycle 03: [outputs/wip/kagari_v03_clay_03.blend](../../wip/kagari_v03_clay_03.blend); SHA256 `4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051`
- Pre-drape panel/seam setup: [outputs/wip/kagari_panel_seams_setup.blend](../../wip/kagari_panel_seams_setup.blend); SHA256 `f468cd72d1cd42831a1fed95bbf53261a7583e235109182ed2e509af9bbcc04f`
- Frozen drape before collar seam: [outputs/wip/kagari_panel_drape_prototype_01.blend](../../wip/kagari_panel_drape_prototype_01.blend); SHA256 `7f3c049b85a0b7b218468ed896e549e692a00ca106c0d76d0ec4404843be62fd`
- Reference: [outputs/design/concept_option2_kagari.jpg](../../design/concept_option2_kagari.jpg); SHA256 `adef163e41f93b12151786b44555c7e6555021e2173947ebb0e52f950c43cc64`.
- Mannequin source is duplicated upper Body plus copied armature and a plain head surrogate. Lower/body cut boundaries are deliberately visible diagnostic crop boundaries, not final avatar geometry. The unsleeved side intentionally ends at an open armhole.
- Source side/back sleeve pattern is inferred from the front concept; this is a method study, not an approved pattern or 1:1 reconstruction.

## Observed comparison with Cycle 03

| Region | Cycle 03, same mannequin/camera | Panel/drape prototype |
|---|---|---|
| Collar | Pinched V-ring plus projected diagonal edge over an elliptical torso | Real broad front-panel overlap with an attached thin collar band; neckline still angular/high |
| Sleeve | Short rigid radial tube/bell forms | One wide fabric bag, open forearm aperture, visible hanging lower volume |
| Shoulder | Exposed shoulder and broken-looking tube root | Mesh continuity from support to sleeve is real; pinned shoulder still high/boxy |
| Torso/back | Smooth cylindrical envelope with little tension response | Gravity-derived folds run between shoulder, side seam and hem; too asymmetric and concentrated at the root |
| Arm raise | Tubes follow arm with ridged joins | Bag follows arm, but root pinches and develops angular folds. Still fails acceptable deformation |
| Waist sash | Rigid extruded belt | Not built; intentionally outside this limited prototype. Removing it is not evidence of a successful sash reconstruction |

## Acceptance evidence

| Required criterion | Agent observation |
|---|---|
| fabric thickness and overlap | PARTIAL: broad front panels genuinely overlap; connected nape/attached band, but neckline and seam spacing remain coarse. |
| natural shoulder sleeve continuity | FAIL: joined mesh surface exists, but pinned shoulder seam sits too high and reads as a plate, especially profile/3-quarter. |
| wide sleeve silhouette | OBSERVED: one wide hanging fabric bag and distal opening, unlike the short radial tube. |
| plausible folds volume | PARTIAL: gravity-derived back/torso tension folds and hanging sleeve mass; folds gather too sharply at armpit. |
| no obvious intersections | NOT_CERTIFIED: neutral major body breakthrough is not obvious, but dark root folds/gaps and raised-pose angular artifacts leave intersection risk. |
| basic arm deformation | FAIL: actual ordinary armature raise reveals sharp root pinching; no solver/corrective morph used to disguise it. |

Neither successful simulation nor normalized weights equals artistic success. All five final images and matched Cycle 03 views were inspected, in addition to the original eight images. No blanket intersection-free claim is supported.

## Top three remaining defects / next corrections

1. **Shoulder/yoke sits too high and stiff.** Profile and 3/4 show a box-like cap/overhang. Recut the yoke against the duplicate shoulder, match armhole edge length and place the seam before simulating. Current pinning preserves a bad starting boundary.
2. **Armpit/root folds and binding are unreliable.** Front/back and raised arm show concentrated jagged folding. Separate free bag cloth from the strongly supported yoke; give the armhole an adequate slack/gusset transition and solve only the hanging region. Smooth weights after neutral drape; keep an ordinary rig-only test.
3. **Collar/nape and hem need a cleaner pattern fit.** The overlap now has real panel mass and continuous nape topology, but neckline stands off and the support hem is an oblique/floating crop. Fit collar band width/cross-section to that seam and reduce excessive pinning; do not use ornament to cover it.
Stop here after three new-method trials. Proposed changes are future work pending human direction, not already completed.

## Mesh complexity and verification

| Scope | Raw triangles | Viewport-evaluated triangles |
|---|---:|---:|
| New support + one sleeve | 5,968 | 12,324 |
| Continuous overlapping collar | 768 | 1,936 |
| New garment only | 6,736 | 14,260 |
| Mannequin study whole scene | 13,644 | 21,168 |
| Cycle 03 four structural meshes | 6,496 | 13,960 |

These scopes differ: Cycle 03 includes two sleeves and two torso layers. Whole-avatar totals also include unrelated hair/bow/hidden geometry. These are no FPS/export benchmarks. Solidify expands the new support by +6,356 triangles and collar by +1,168; no subdivision or live cloth modifier remains on the final mesh.
Both garment surfaces are connected individually, have zero zero-area faces and zero interior non-manifold edges in raw topology. Open boundary edges at neckline/hem/armhole are intentional before thickness. All deforming vertices have normalized weights with at most four deform influences. Evaluated neutral/raised coordinates are finite. These technical results do not resolve the visible root artifacts.
[Full geometry audit](geometry_audit.json); [technical verification](technical_verification.json); [complexity comparison](mesh_complexity_comparison.json).

## VRM and rigging risks

- Native Cloth is an authoring/drape tool here. The final mesh can be evaluated with an Armature; VRM export/re-import has not been run, and Blender Cloth motion is not a runtime certification.
- Sleeve root/underarm still needs pose-safe topology and weights. A frozen neutral fold rotates with skinning; it does not continue to hang under world gravity. Dynamic cloth/spring-bone or corrective treatment would require separate design/testing.
- Pattern UVs and seam groups are retained as working data, but production UV layout/materials are not approved. Solidify must be handled consistently by export; final exported triangle count is unknown.
- The mannequin .blend is not a complete VRM avatar: it has no delivery-ready facial expressions/metadata, second sleeve, full outfit or validated runtime. The copied humanoid armature is a study binding only. Original character source remains separate.
- No new software, external mesh or asset was installed/downloaded. Registered tools and a scoped Windows install inventory were inspected.

## Human review

Review the panel/drape direction and decide whether to continue with a hand-fitted yoke/armhole plus selectively simulated sleeve, or pause this automatic construction route. Current form is NOT_APPROVED and should not unlock decorations or integration into Kagari.
