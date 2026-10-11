# Kagari upper garment clay construction plan

Scope authorized by `outputs/reports/v03_merge/user_task.txt`: one construction experiment and human review, no ornamentation/export. Existing head renders are available but explicit signed-off face/head evidence is not linked; protected meshes are frozen.

Baseline: `outputs/wip/kagari_outfit_detail_v1.blend`.
Concept: `outputs/design/concept_option2_kagari.jpg`, illustrative front view.
Planned candidate: `outputs/wip/kagari_v03_clay_01.blend` (a proposed path until saved).

## Observed and inferred construction

Observed: cream underlayer, burgundy crossed collar, cream outer robe/sleeves, shoulder coverage. Crossing extends from viewer-left neck to viewer-right lower torso on the frontmost panel. Side/rear pattern and exact sleeve seam are inferred because no approved orthographic pattern exists.

Layer ordering outside → inside:

`wrapped front collar overlap → outer robe surface / collar seam → cream under-top → existing skin`

The under-collar ends beneath the overlap. Its lower tail cannot remain visible as a floating X. The collar continues around the nape and follows neck/clavicle/chest curvature, with its outer edge contacting the garment and its inner edge near skin.

## Garment pattern and anchoring

- Use the existing body's continuous shoulder/upper-arm topology as a seam/deformation guide, not a rigid sphere wrapped around the torso.
- Extract a new garment surface from upper torso and upper/mid arm regions into its own object. Retain torso/shoulder/arm weight transitions; preserve the original Face, every facial morph, rig and Hair mesh.
- Fit a V opening and hem boundary. Offset the cloth with clearance, creating slack mainly below the armpit and towards the sleeve hem; top shoulder remains a contact/tension anchor.
- Sleeve remains an open fabric shell with an actual opening. Use broad folds anchored at shoulder/armpit and a sleeve longitudinal fold; no repeated sine-noise decoration.
- Inner top uses a higher V opening and sits inside outer robe. Use modest edge thickness and existing anatomical loop density; no dense subdivision.
- Build one low-density collar around the nape and down the crossed front. Project contact edges to the garment/skin guide and keep a small physical thickness. Use garment weights near its sewn edge.
- Hide superseded upper garment/detail meshes in this new experiment. Retain unrelated source assets in the file; hide existing ornaments consistently in clay comparison. No texture editing.

## Test plan

- Save immutable neutral baseline/candidate snapshots and record SHA before renders.
- Identical orthographic camera definitions and neutral studio lights: front, 3/4, side, back and front moderate arm raise, plus portrait/context crop.
- Moderate raise: rotate each upper arm 30° toward its rest T-pose from the baseline relaxed pose; save exact pose matrices/settings in the render manifest.
- Inspect real images and verify source/candidate protected-data hashes. Record raw/evaluated geometry and cumulative modifier expansions.
- Rank three visible construction defects. At most three ineffective targeted cycles, then recommend a different garment pattern/base or manual construction method.
- Human verdict remains REQUIRES_HUMAN_ART_REVIEW. No trim, flowers, hair reconstruction or VRM export in this experiment.
