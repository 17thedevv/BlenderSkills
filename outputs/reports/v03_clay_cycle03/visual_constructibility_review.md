# Kagari v0.3 — actual clay construction review

**Decision: REQUIRES_HUMAN_ART_REVIEW. Agent construction verdict: FAIL.**
Three targeted cycles completed within one scoped experiment. Further geometry changes stopped. The third candidate is an inspectable failed experiment, not a replacement approved for production. No human approval has been invented.

## Exact inputs and outputs

- Original source: [outputs/wip/kagari_outfit_detail_v1.blend](../../wip/kagari_outfit_detail_v1.blend); SHA256 `8ead8701d3526c1343166a5ad9f286e3cb1f67a0570d7ef2d4eb4109ada838dd`
- Frozen same-camera baseline: [outputs/wip/kagari_v03_clay_baseline.blend](../../wip/kagari_v03_clay_baseline.blend); SHA256 `002626a68dc4862ef518d6b79a3409d64befa1fb87e6cd56d35a42444094ffdf`
- Current experimental candidate: [outputs/wip/kagari_v03_clay_03.blend](../../wip/kagari_v03_clay_03.blend); SHA256 `4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051`
- Concept: [outputs/design/concept_option2_kagari.jpg](../../design/concept_option2_kagari.jpg); SHA256 `adef163e41f93b12151786b44555c7e6555021e2173947ebb0e52f950c43cc64`
- Candidate version: `v0.3-clay-03`.
- Historical face/head renders exist, but explicit signed-off evidence was not found. The current instruction authorized this garment experiment; it did not approve the face.

## Observed top three defects and next geometry correction

| Priority | Observation in actual images | Proposed correction after human direction |
|---|---|---|
| 1 | Shoulder skin intersects the upper cloth; disconnected-looking slots and hard ridges at the sleeve join remain in front, 3/4 and isolated profile/back. The raised-arm pose exposes the same ridges. | Use a hand-authored shoulder/yoke panel with a real armhole edge, sew sleeve boundary to it, then transfer and locally smooth weights. Avoid moving a cylindrical torso neck ring inward without rebuilding the shoulder pattern. |
| 2 | V-neck contact and overlap are pinched/creased; the diagonal wrap edge reaches the torso but its join is jagged. The layered outer haori/inner crossed collar distinction is not reproduced convincingly. | Trace separate inner wrap and outer haori panels from concept, define the visible inner edge/hidden seam and overlap depth explicitly; weld or bridge appropriate boundaries rather than project a strip onto skin. |
| 3 | Torso is too cylindrical, sleeves are short bell forms, and medium folds are weak. This differs from the reference long sleeve and draped layered garment. | Build upper sleeve first from a small quad panel, add gravity-driven underarm slack and broad fold anchors at shoulder/obi; keep the lower sleeve outside this scoped experiment until the upper construction is approved. |

## Cycle evidence and baseline contrast

- Baseline: thick floating crossed strips, detached lapel ends and a mantle-like sleeve silhouette. Side view exposes the offset between strips and torso.
- Cycle 01: source skin extraction preserves weights but reproduces breast forms, jagged collar and pointed shoulders. Rejected by agent; changed construction method immediately.
- Cycle 02: sparse sewn torso/sleeve panel rings give readable hollow sleeves and less disconnected strip geometry. Neck opening remains too wide/off-shoulder and identity drifts toward a V-neck shirt.
- Cycle 03: attempted nape contact and an attached diagonal wrap edge. Shoulder and neckline intersections worsen. Some cloth volume exists, but this is not a reliable artistic improvement over baseline.
- Stop after cycle 03. Recommend manually constructed concept-traced garment panels, or a licensed compatible base garment only after source/license verification and user authorization for external acquisition. Do not increase subdivision or cover defects with ornament.

## Acceptance assessment

| Criterion | Observed result |
|---|---|
| Collar layers and plausible contacts | FAIL — pinching/intersection remains; no acceptable layer construction |
| Shoulder/sleeve and moderate raise | FAIL — mass exists but shoulder joins expose artifacts; no deformation certification |
| Cloth form without ornament | PARTIAL — sleeve volume present; torso/fold quality and reference identity insufficient |
| Traceable files, SHA, matched cameras | VERIFIED from manifests and actual file hashes |
| Preserved Face/morphs/Hair/rig | VERIFIED from independent saved-file reopen comparison |
| User form approval | NOT_APPROVED |
| Candidate VRM/Warudo/OBS readiness | NOT_TESTED |

## Construction and evidence limits

Front concept establishes outer cream haori, burgundy crossed inner collar and soft drape. Side/back cut, armhole and pattern are inferred; the concept is not a measured sewing pattern. Current gray material hides color deliberately. Existing ornaments are hidden consistently in both sets; textures and original Face/Hair material assignments are preserved. Diagnostic isolated images temporarily hide unmodified Face/Hair/bow to expose garments and are labelled in the manifest.
The candidate retains old garment objects hidden for recoverability and removes only source upper-jacket faces from Body. New mesh weights are normalized and no new subdivision modifier was added. Technical validity does not resolve visible intersections.

## Geometry cost (Blender viewport depsgraph, all scene meshes)

| Inventory | Baseline raw | Baseline evaluated | Candidate raw | Candidate evaluated |
|---|---:|---:|---:|---:|
| All scene, including hidden source | 50,587 | 134,067 | 56,489 | 147,433 |
| Objects with render enabled* | 34,679 | 116,599 | 36,741 | 96,941 |

*This is a filtered object inventory with viewport modifier levels, not a render/export pipeline or collection visibility simulation. The reduction comes from hiding superseded pieces and is not evidence of runtime performance improvement.
New structural meshes total 6,496 raw / 13,960 evaluated triangles. Growth is from sparse construction plus Solidify, not dense subdivision. Existing bow modifiers dominate expansion and were left intact under the protected scope.

| Object / modifier | Triangle increase |
|---|---:|
| Kagari_Silk_Bow_Tail_-1 / Fabric_Thickness (SOLIDIFY) | +6,656 |
| Kagari_Silk_Bow_Tail_1 / Fabric_Thickness (SOLIDIFY) | +6,656 |
| Kagari_Silk_Bow_Lobe_-1 / Fabric_Thickness (SOLIDIFY) | +6,592 |
| Kagari_Silk_Bow_Lobe_1 / Fabric_Thickness (SOLIDIFY) | +6,592 |
| Kagari_Silk_Bow_Lobe_-1 / Silk_Surface (SUBSURF) | +5,760 |
| Kagari_Silk_Bow_Lobe_1 / Silk_Surface (SUBSURF) | +5,760 |
| Kagari_Silk_Bow_Tail_-1 / Silk_Surface (SUBSURF) | +5,760 |
| Kagari_Silk_Bow_Tail_1 / Silk_Surface (SUBSURF) | +5,760 |

Full [geometry audit](geometry_audit.json) and [comparison](geometry_comparison.json) include topology, weights, shape keys, object costs and failures.
[Saved invariant check](saved_invariants.json); [render/camera/pose/image hashes](render_manifest.json); [construction plan before modeling](../v03_clay/construction_plan.md).
