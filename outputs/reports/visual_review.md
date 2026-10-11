# Kagari — Outfit and accessory detail revision

Reviewed on 2026-10-11. User selected **Trang phục và phụ kiện** as the priority.

Source: `outputs/wip/kagari_vroid_master.blend`.
Review candidate: `outputs/wip/kagari_outfit_detail_v1.blend`.
Reference: `outputs/design/concept_option2_kagari.jpg`.
Side-by-side page: `outputs/previews/outfit_detail_v1/review.html`.

Previous Gate B report: `visual_review_legacy_gate_b.md`. Its numerical ratings and runtime claims do not certify this model.

## Three prioritized defects

| Region | Before evidence | Defect and cause | Revision | After evidence |
|---|---|---|---|---|
| Upper outfit | `before_front.png`, `before_outfit_close.png` | Collar and coarse gold dots were painted on the skin texture; little depth and visible shoulder logos. | Cream shell and inner robe, raised overlapping burgundy collar, outer borders, thin piping and floral relief. Clean covered torso and neckline materials. | `after_front.png`, `after_three_quarter.png`, `after_outfit_close.png` |
| Hair bow | `before_side.png`, `before_three_quarter.png` | Broad flat patches and box knot were especially apparent in side view. | Convex ribbon surfaces, gathered knot, curved fishtail ribbons, gold edging and flower charm. | `after_three_quarter.png`, `after_side.png` |
| Necklace | `before_outfit_close.png` | Oversized bright pendant; necklace was non-rendering bare edges. | Smaller faceted eight-point star, alternating facets, bail, connector and two round chains. | `after_outfit_close.png` |

Images are in `outputs/previews/outfit_detail_v1/`.

## Actual visual checks

Inspected actual Blender renders: front, three-quarter, side, back, face close-up, outfit close-up and 320 × 426 stream crop. Before/after use identical cameras, lighting and color management. New materials use modest normal-based toon shading.

Qualitative judgments:

- Neckline and borders read as separate layers in front and three-quarter views.
- Gold floral motifs remain recognizable in the portrait crop; brocade detail is subtle.
- Pendant scale and faceting are clearer, with visible chains.
- Bow has more depth and a softer silhouette, but still looks thin from the exact side angle.
- Existing hair/scalp gaps and angular hair tips remain visible in side/back views; hair is outside the selected revision scope.

## Repair history

1. Initial revision rejected: torso ray samples caused collar discontinuities/intersections, and Principled materials read too bright in the existing lights.
2. Replaced discontinuous placement with measured continuous garment sections, repaired overlap and added controlled toon shading; rerendered all views.
3. Hid the under-collar below the crossing, added filled petal/leaf relief and softened cream/neck shading; rerendered all views.

A subsequent technical reduction removes redundant piping samples without changing authored silhouettes; the same views are rerendered and inspected.

## Remaining work and limits

- Visual revision candidate; human aesthetic approval pending. No numerical final quality score.
- Sleeve construction and natural cloth folds still need refinement. The simplified shell and shoulder/neck transitions have small edge discontinuities in close-up and side views.
- Outer embroidery is improved but does not reproduce every reference branch and fabric pattern.
- Added garments use a single chest-bone preview attachment. Cloth deformation, arm motion, head-turn collisions and secondary motion are not validated.
- Custom preview toon materials are not yet configured as VRM MToon export materials.
- VRM export/re-import, Warudo tracking and OBS performance were not tested.

`kagari_outfit_detail_verification.json` separately records comparisons of face geometry, every facial shape key, hair geometry, original bone hierarchy/rest positions, packed images and evaluated geometry counts.
